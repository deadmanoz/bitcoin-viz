# Bitcoin Core: Incoming Transaction Processing Flow

**Research Document for Bitcoin Visualization Project**
**Bitcoin Core Version:** v30.0
**Last Updated:** 2025-11-11

This document traces the complete journey of a transaction from the moment it arrives from a P2P network peer until it's safely stored in the mempool, ready for mining.

---

## Table of Contents

1. [Overview](#overview)
2. [Network Layer: Receiving the Transaction](#network-layer-receiving-the-transaction)
3. [Transaction Download Management](#transaction-download-management)
4. [Mempool Acceptance Pipeline](#mempool-acceptance-pipeline)
5. [Validation Steps Deep Dive](#validation-steps-deep-dive)
6. [Key Data Structures](#key-data-structures)
7. [Complete Flow Diagram](#complete-flow-diagram)
8. [Code Reference Map](#code-reference-map)

---

## Overview

When a Bitcoin node receives a transaction from a peer on the P2P network, it undergoes a rigorous multi-stage validation process before being admitted to the mempool. This process ensures:

- **Consensus validity**: Transaction follows Bitcoin's consensus rules
- **Policy compliance**: Transaction meets local node policies
- **Network protection**: Guards against DoS attacks and spam
- **Economic rationality**: Transaction pays sufficient fees

The entire flow can be summarized in five major stages:

1. **Network Reception** - P2P message handling
2. **Download Management** - Orphan detection and package coordination
3. **Pre-validation Checks** - Quick structural and policy checks
4. **Script Validation** - Cryptographic signature verification
5. **Mempool Admission** - Final acceptance and relay

---

## Network Layer: Receiving the Transaction

### Entry Point: P2P Message Dispatcher

**Location:** `src/net_processing.cpp:3415`

Every message from a peer passes through `PeerManagerImpl::ProcessMessage()`:

```cpp
void ProcessMessage(CNode& pfrom, const std::string& msg_type, DataStream& vRecv,
                    const std::chrono::microseconds time_received,
                    const std::atomic<bool>& interruptMsgProc)
```

This function acts as the central dispatcher for all P2P protocol messages, including:
- `tx` - Individual transaction
- `block` - Block data
- `inv` - Inventory announcements
- `getdata` - Data requests
- And many more...

### The "tx" Message Handler

**Location:** `src/net_processing.cpp:4248-4316`

When `msg_type == "tx"`, the handler executes the following sequence:

#### Step 1: Protocol Validation (Line 4249)
```cpp
if (RejectIncomingTxs(pfrom)) {
    LogPrint(BCLog::NET, "transaction sent in violation of protocol peer=%d\n", pfrom.GetId());
    return;
}
```
Ensures the peer is allowed to send transactions (not blocksonly mode).

#### Step 2: Initial Block Download Check (Line 4258)
```cpp
if (m_chainman.IsInitialBlockDownload()) {
    return; // Defer transaction validation during IBD
}
```
Transactions aren't validated during initial sync - node focuses on catching up with the blockchain first.

#### Step 3: Deserialization (Line 4261)
```cpp
CTransactionRef ptx;
vRecv >> TX_WITH_WITNESS(ptx);
```
Parses the raw network bytes into a `CTransaction` object, including witness data.

#### Step 4: Hash Extraction (Lines 4263-4264)
```cpp
const uint256& hash = ptx->GetHash();      // Standard txid
const uint256& wtxid = ptx->GetWitnessHash(); // Witness txid
```
Two identifiers are computed:
- **txid**: Hash of transaction without witness data (pre-SegWit compatibility)
- **wtxid**: Hash including witness data (used for relay post-SegWit)

#### Step 5: Mark Transaction as Known (Line 4267)
```cpp
AddKnownTx(*peer, hash);
```
Records that this peer has seen this transaction (prevents re-announcing back to them).

---

## Transaction Download Management

**Location:** `src/node/txdownloadman.h:158` & `src/net_processing.cpp:4271`

Before validation, the `TxDownloadManager` makes a crucial decision:

```cpp
auto [should_validate, package_to_validate] =
    m_txdownloadman.ReceivedTx(pfrom.GetId(), ptx);
```

This component handles three scenarios:

### Scenario 1: Normal Transaction
- All parent transactions already in mempool or confirmed
- Returns `{true, std::nullopt}` - proceed to validation

### Scenario 2: Orphan Transaction
- One or more parents are missing
- Transaction stored in `TxOrphanage` (temporary storage)
- Returns `{false, std::nullopt}` - validation deferred

### Scenario 3: Package Validation (CPFP)
- Orphan's parent arrives, completing a 1-parent-1-child package
- Returns `{true, PackageToValidate}` - validate as package
- Enables Child-Pays-For-Parent (CPFP) fee bumping

**Key Class:** `TxOrphanage`
- Temporary storage for orphaned transactions
- Limited size (default: 100 transactions)
- Automatic expiry (20 minutes default)
- Enables out-of-order transaction receipt

---

## Mempool Acceptance Pipeline

### Main Entry Point

**Location:** `src/validation.cpp:4547`

```cpp
MempoolAcceptResult ChainstateManager::ProcessTransaction(
    const CTransactionRef& tx, bool test_accept = false)
{
    return AcceptToMemoryPool(m_active_chainstate, tx, GetTime(),
                              /*bypass_limits=*/false, test_accept);
}
```

This lightweight wrapper delegates to the core acceptance function.

### Core Acceptance Function

**Location:** `src/validation.cpp:1860`

```cpp
MempoolAcceptResult AcceptToMemoryPool(
    Chainstate& active_chainstate,
    const CTransactionRef& tx,
    int64_t accept_time,
    bool bypass_limits,
    bool test_accept)
```

**Key Steps:**

1. **Create validation context** (Lines 1865-1869)
   - Builds `ATMPArgs` with configuration
   - Sets up fee calculation parameters
   - Configures validation flags

2. **Instantiate validator** (Line 1870)
   ```cpp
   MemPoolAccept mem_pool_accept(pool, active_chainstate);
   ```

3. **Run validation** (Line 1871)
   ```cpp
   auto result = mem_pool_accept.AcceptSingleTransaction(tx, args);
   ```

4. **Cleanup on failure** (Lines 1877-1878)
   ```cpp
   if (!result.m_result_type == MempoolAcceptResult::ResultType::VALID) {
       active_chainstate.CoinsTip().Uncache(tx->vin);
   }
   ```
   Removes any cached coin data if transaction rejected (prevents memory bloat).

---

## Validation Steps Deep Dive

The `MemPoolAccept` class orchestrates all validation through its `AcceptSingleTransaction()` method.

**Location:** `src/validation.cpp:1429-1519`

### Validation Stage 1: PreChecks

**Location:** `src/validation.cpp:786-1085`

This stage performs fast, fail-early checks before expensive script validation:

| # | Check | Code Location | Purpose |
|---|-------|---------------|---------|
| 1 | **Basic Structure** | 802 | `CheckTransaction()` - valid inputs/outputs |
| 2 | **Coinbase Reject** | 807 | Coinbase only valid in blocks |
| 3 | **Standard Format** | 812 | `IsStandardTx()` - policy compliance |
| 4 | **Size Limits** | 817 | Min 65 bytes (non-witness) |
| 5 | **Finality** | 823 | `CheckFinalTxAtTip()` - locktime satisfied |
| 6 | **Mempool Duplicates** | 827-834 | Detect identical transaction |
| 7 | **Input Conflicts** | 837-847 | Check for double-spends in mempool |
| 8 | **UTXO Availability** | 853-872 | All inputs exist and unspent |
| 9 | **Sequence Locks** | 890-893 | BIP68 relative locktime |
| 10 | **Input Values** | 896 | `Consensus::CheckTxInputs()` |
| 11 | **Standard Inputs** | 900 | `AreInputsStandard()` - known types |
| 12 | **Witness Format** | 905 | `IsWitnessStandard()` |
| 13 | **Sigop Cost** | 909 | `GetTransactionSigOpCost()` ≤ 4000 |
| 14 | **Minimum Fee** | 952 | Meets relay fee (1 sat/vByte default) |
| 15 | **Mempool Fee** | 961 | Meets mempool minimum (dynamic) |
| 16 | **Ancestor Limits** | 969-1003 | Max 25 ancestors, 101 KB total |

**Important Data Computed Here:**

**Lines 928-933:**
```cpp
ws.m_vsize = tx.GetVirtualTransactionSize();
ws.m_base_fees = GetTransactionFee(tx);
ws.m_modified_fees = ws.m_base_fees + m_pool.GetModifiedFee(tx);
```

### Validation Stage 2: ReplacementChecks (RBF)

**Location:** `src/validation.cpp:1087-1245`

If transaction conflicts with existing mempool entries, this validates Replace-By-Fee rules:

- **Absolute Fee Rule**: New tx pays more total fees
- **Feerate Rule**: New tx has higher feerate
- **No New Unconfirmed Inputs**: Prevents certain pinning attacks
- **Incentive Compatibility**: Miners profit from replacement

**BIP 125** governs the RBF policy.

### Validation Stage 3: PolicyScriptChecks

**Location:** `src/validation.cpp:1247-1268`

First pass of script validation with **policy-level flags**:

```cpp
constexpr unsigned int scriptVerifyFlags = STANDARD_SCRIPT_VERIFY_FLAGS;

if (!CheckInputScripts(tx, state, m_view, scriptVerifyFlags,
                       true, false, ws.m_precomputed_txdata,
                       GetValidationCache())) {
    return error("PolicyScriptChecks failed");
}
```

**Why policy checks first?**
- **DoS Protection**: Fail fast on invalid scripts before expensive consensus checks
- **Stricter Rules**: Policy flags are more restrictive than consensus
- **Network Health**: Prevents relay of non-standard transactions

### Validation Stage 4: ConsensusScriptChecks

**Location:** `src/validation.cpp:1270-1301`

Second pass with **consensus-level flags** (current block rules):

```cpp
unsigned int currentBlockScriptVerifyFlags =
    GetBlockScriptFlags(*m_active_chainstate.m_chain.Tip(), m_active_chainstate.m_chainman);

if (!CheckInputsFromMempoolAndCache(tx, state, m_view, m_pool,
                                    currentBlockScriptVerifyFlags,
                                    ws.m_precomputed_txdata,
                                    m_active_chainstate.CoinsTip())) {
    return error("ConsensusScriptChecks failed");
}
```

**Key Differences:**
- Uses current block height's activation rules
- Caches successful script execution (parallel validation cache)
- Ensures transaction valid for inclusion in next block

**What's Checked in Script Validation?**

For each input:
1. **Signature Verification**: ECDSA/Schnorr signatures validate
2. **Script Execution**: scriptSig + scriptPubKey execute successfully
3. **Witness Validation**: SegWit witness data is valid
4. **Timelock Verification**: CHECKLOCKTIMEVERIFY, CHECKSEQUENCEVERIFY
5. **Stack Constraints**: Final stack has single TRUE value

---

## Key Data Structures

### CTransaction: The Transaction Object

**Location:** `src/primitives/transaction.h:295-374`

```cpp
class CTransaction {
public:
    const std::vector<CTxIn> vin;        // Inputs (references to UTXOs)
    const std::vector<CTxOut> vout;      // Outputs (new UTXOs created)
    const uint32_t version;              // Transaction version (1 or 2)
    const uint32_t nLockTime;            // Earliest time/height for inclusion

    // Cached computed values
    const Txid hash;                     // Transaction ID (no witness)
    const Wtxid m_witness_hash;          // Witness transaction ID

    // Key methods
    const Txid& GetHash() const;
    const Wtxid& GetWitnessHash() const;
    CAmount GetValueOut() const;         // Sum of all outputs
    unsigned int GetTotalSize() const;   // Serialized size
    bool IsCoinBase() const;
    bool HasWitness() const;
};
```

### CTxIn: Transaction Input

```cpp
class CTxIn {
public:
    COutPoint prevout;           // Reference to UTXO (txid + output index)
    CScript scriptSig;           // Unlocking script (pre-SegWit)
    uint32_t nSequence;          // Sequence number (RBF, timelocks)
    CScriptWitness scriptWitness; // Witness data (SegWit)
};
```

### CTxOut: Transaction Output

```cpp
class CTxOut {
public:
    CAmount nValue;              // Amount in satoshis
    CScript scriptPubKey;        // Locking script (spending condition)
};
```

### MemPoolAccept::Workspace

**Location:** `src/validation.cpp:628-664`

Temporary state during validation:

```cpp
struct Workspace {
    std::set<Txid> m_conflicts;              // Conflicting transactions
    CTxMemPool::setEntries m_ancestors;      // In-mempool ancestors

    int64_t m_vsize;                         // Virtual size (weight/4)
    CAmount m_base_fees;                     // Actual fees paid
    CAmount m_modified_fees;                 // Fees + priority adjustments

    const CTransactionRef& m_ptx;            // Transaction being validated
    TxValidationState m_state;               // Current validation state
    PrecomputedTransactionData m_precomputed_txdata; // Cached sighashes
};
```

### CTxMemPool: The Memory Pool

**Location:** `src/txmempool.h`

Multi-indexed container storing pending transactions:

**Indexes:**
- By txid (fast lookup)
- By wtxid (witness-aware lookup)
- By ancestor score (mining optimization)
- By entry time (eviction policy)

**Key Features:**
- Tracks ancestor/descendant relationships
- Maintains aggregate fees and sizes
- Supports efficient mining block template creation
- Implements size-based eviction (lowest feerate first)

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     PEER SENDS "tx" MESSAGE                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ net_processing.cpp:4248                                          │
│ PeerManagerImpl::ProcessMessage() - "tx" handler                 │
│   • RejectIncomingTxs() check                                   │
│   • IBD check (skip if syncing)                                 │
│   • Deserialize: vRecv >> TX_WITH_WITNESS(ptx)                  │
│   • Extract txid and wtxid                                      │
│   • AddKnownTx(peer, hash)                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ node/txdownloadman.h:158                                         │
│ TxDownloadManager::ReceivedTx()                                  │
│   • Check for orphan (missing parents)                          │
│   • Check for package opportunities (CPFP)                      │
│   • Returns: [should_validate, optional_package]                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
              ┌───────────────┴───────────────┐
              ↓                               ↓
    ┌─────────────────┐           ┌─────────────────┐
    │ Orphan?         │           │ Ready to         │
    │ Store in        │           │ Validate         │
    │ TxOrphanage     │           └─────────────────┘
    │ (wait for       │                     ↓
    │  parents)       │
    └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ validation.cpp:4547                                              │
│ ChainstateManager::ProcessTransaction()                          │
│   ↓                                                              │
│ validation.cpp:1860                                              │
│ AcceptToMemoryPool()                                             │
│   ↓                                                              │
│ validation.cpp:1870                                              │
│ MemPoolAccept::AcceptSingleTransaction()                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 1: PreChecks (validation.cpp:786-1085)                    │
│                                                                  │
│ ✓ Basic structure (CheckTransaction)                            │
│ ✓ Standard format (IsStandardTx)                                │
│ ✓ Size limits                                                   │
│ ✓ Finality (locktime, sequence)                                 │
│ ✓ No mempool duplicates                                         │
│ ✓ No input conflicts                                            │
│ ✓ All inputs exist in UTXO set                                  │
│ ✓ Input values valid (CheckTxInputs)                            │
│ ✓ Standard input types                                          │
│ ✓ Witness format                                                │
│ ✓ Sigop cost ≤ 4000                                             │
│ ✓ Meets minimum relay fee                                       │
│ ✓ Meets mempool minimum fee                                     │
│ ✓ Ancestor/descendant limits                                    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 2: ReplacementChecks (validation.cpp:1087-1245)           │
│                                                                  │
│ IF conflicts exist:                                              │
│   ✓ Signaling RBF (BIP 125)                                     │
│   ✓ Higher absolute fee                                         │
│   ✓ Higher feerate                                              │
│   ✓ No new unconfirmed inputs                                   │
│   ✓ Incentive compatible                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 3: PolicyScriptChecks (validation.cpp:1247-1268)          │
│                                                                  │
│ CheckInputScripts() with STANDARD_SCRIPT_VERIFY_FLAGS           │
│   ✓ All signatures valid                                        │
│   ✓ All scripts execute successfully                            │
│   ✓ Witness data valid                                          │
│   ✓ Timelock constraints satisfied                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ STAGE 4: ConsensusScriptChecks (validation.cpp:1270-1301)       │
│                                                                  │
│ CheckInputsFromMempoolAndCache() with block script flags        │
│   ✓ Re-validate with consensus rules                            │
│   ✓ Cache successful execution                                  │
│   ✓ Ensure valid for next block                                 │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ FINALIZATION (validation.cpp:1303-1327)                          │
│                                                                  │
│ • FinalizeSubpackage() - Remove conflicting txs (RBF)           │
│ • LimitMempoolSize() - Evict lowest feerate if full             │
│ • TransactionAddedToMempool signal - Notify subsystems          │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ SUCCESS! Return MempoolAcceptResult                              │
│   • Virtual size                                                 │
│   • Fees paid                                                    │
│   • Effective feerate                                            │
│   • Replaced transactions (if RBF)                               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│ net_processing.cpp:3007                                          │
│ PeerManagerImpl::ProcessValidTx()                                │
│   • Update peer's last tx time                                  │
│   • Relay transaction to other peers                            │
│   • Update peer reputation                                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌──────────────────┐
                    │ TX IN MEMPOOL ✓  │
                    │ Ready for mining │
                    └──────────────────┘
```

---

## Code Reference Map

Quick reference for key components and their locations in Bitcoin Core v30.0:

### Network Layer
| Component | File | Lines |
|-----------|------|-------|
| Message dispatcher | `src/net_processing.cpp` | 3415 |
| TX message handler | `src/net_processing.cpp` | 4248-4316 |
| ProcessValidTx | `src/net_processing.cpp` | 3007 |
| ProcessInvalidTx | `src/net_processing.cpp` | 2980 |

### Transaction Download
| Component | File | Lines |
|-----------|------|-------|
| TxDownloadManager | `src/node/txdownloadman.h` | 117-174 |
| TxOrphanage | `src/node/txdownloadman.h` | 98+ |

### Validation Pipeline
| Component | File | Lines |
|-----------|------|-------|
| ProcessTransaction | `src/validation.cpp` | 4547-4559 |
| AcceptToMemoryPool | `src/validation.cpp` | 1860-1888 |
| MemPoolAccept class | `src/validation.cpp` | 439-750 |
| AcceptSingleTransaction | `src/validation.cpp` | 1429-1519 |
| PreChecks | `src/validation.cpp` | 786-1085 |
| ReplacementChecks | `src/validation.cpp` | 1087-1245 |
| PolicyScriptChecks | `src/validation.cpp` | 1247-1268 |
| ConsensusScriptChecks | `src/validation.cpp` | 1270-1301 |
| FinalizeSubpackage | `src/validation.cpp` | 1303-1327 |

### Consensus Checks
| Component | File | Lines |
|-----------|------|-------|
| CheckTransaction | `src/consensus/tx_check.cpp` | 11-60 |
| CheckTxInputs | `src/consensus/tx_verify.cpp` | 164-205 |

### Policy Checks
| Component | File | Lines |
|-----------|------|-------|
| IsStandardTx | `src/policy/policy.cpp` | 99+ |
| AreInputsStandard | `src/policy/policy.cpp` | - |

### Data Structures
| Component | File | Lines |
|-----------|------|-------|
| CTransaction | `src/primitives/transaction.h` | 295-374 |
| CTxIn | `src/primitives/transaction.h` | - |
| CTxOut | `src/primitives/transaction.h` | - |
| CTxMemPool | `src/txmempool.h` | - |

---

## Key Takeaways for Video Content

1. **Five Clear Stages**: Network → Download Management → PreChecks → Script Validation → Mempool
2. **Defense in Depth**: Multiple validation layers protect against attacks
3. **Performance Optimization**: Fast checks first, expensive checks last
4. **Economic Incentives**: Fee-based admission and eviction
5. **Network Efficiency**: Orphan handling and package validation (CPFP)
6. **Standards vs Consensus**: Two-pass script validation ensures both policy compliance and consensus validity

---

## Next Research Topics

- **Orphan Transaction Management**: Deep dive into TxOrphanage
- **Replace-By-Fee (RBF)**: Full BIP 125 implementation details
- **Package Relay**: CPFP and package validation mechanics
- **Script Validation**: Script engine internals and caching
- **Mempool Eviction**: Fee-based eviction algorithm
- **Transaction Relay**: INV/GETDATA protocol and bandwidth optimization

---

*This document is part of the Bitcoin Visualization Project. For questions or corrections, please refer to the Bitcoin Core source code in `bitcoin-core/` directory.*
