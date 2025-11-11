# Script: Inside Bitcoin Core - Transaction Processing

**Video Type:** Technical Deep-Dive
**Topic:** How Bitcoin Core Processes Incoming Transactions
**Target Audience:** Developers, technical Bitcoin enthusiasts
**Estimated Duration:** 12-15 minutes
**Visual Style:** Synthwave/Cyberpunk with code overlays

---

## Visual Theme for This Video

**Code-Focused Aesthetic:**
- Actual Bitcoin Core source code snippets flowing across screen
- Function call stack visualization
- Data structure diagrams with real C++ types
- Neon "pipeline" showing transaction flowing through validation stages
- Terminal-style output showing validation checks passing/failing

**Color Coding:**
- **Cyan**: Network layer
- **Magenta**: Validation checks
- **Green**: Success/passing checks
- **Red**: Rejection/failure paths
- **Yellow**: Data structures
- **Purple**: Script execution

---

## Scene Breakdown

### SCENE 1: Title & Context (0:00 - 0:45)

**Visual:**
- Fade in: Bitcoin Core logo with v30.0 tag
- Background: Matrix-style falling code (actual Bitcoin Core source)
- Title: "Inside Bitcoin Core: Transaction Processing"

**Narration:**
> "When your Bitcoin node receives a transaction from a peer, what happens next? Let's follow a transaction's journey through Bitcoin Core's validation pipeline, from the P2P network layer all the way to mempool admission."

**Visual Transition:**
- Camera zooms into the falling code
- Code coalesces into a network connection visualization
- Two glowing nodes appear, connected by neon lines

**On-screen text:**
- "Bitcoin Core v30.0"
- "~300,000 lines of C++ code"
- "5 validation stages"
- "12+ critical checks"

---

### SCENE 2: The Network Layer - Receiving the Message (0:45 - 2:30)

**Visual Setup:**
- Split screen: Left = Network visualization, Right = Code overlay
- Peer node (glowing sphere) sending packet labeled "tx"
- Packet travels through neon "wire" to our node

**Animation Sequence:**

**Step 1: Message Arrival**
```
PEER NODE ──[tx message]──> OUR NODE
```

**Code Overlay (appears as packet arrives):**
```cpp
// src/net_processing.cpp:3415
void PeerManagerImpl::ProcessMessage(
    CNode& pfrom,
    const std::string& msg_type,  // "tx"
    DataStream& vRecv,
    ...
) {
```

**Narration:**
> "Every message from a peer enters through ProcessMessage - the central dispatcher for all P2P communication. When the message type is 'tx', a specialized handler takes over."

**Step 2: Protocol Checks**
- Highlight code section:
```cpp
// Line 4249: Protocol validation
if (RejectIncomingTxs(pfrom)) {
    return; // ❌ Peer violating protocol
}
```
- Visual: Shield icon appears, checks peer (✓ passes)

**Step 3: IBD Check**
- Highlight code section:
```cpp
// Line 4258: Initial Block Download check
if (m_chainman.IsInitialBlockDownload()) {
    return; // Node is syncing
}
```
- Visual: Progress bar showing "Sync: 100%" (✓ ready)

**Narration:**
> "First, quick checks: Is this peer allowed to send transactions? Are we done syncing the blockchain? If both pass, we proceed to deserialization."

**Step 4: Deserialization**
- Packet "explodes" into structured data
- Show transformation: Raw bytes → CTransaction object

**Code Overlay:**
```cpp
// Line 4261: Parse network bytes
CTransactionRef ptx;
vRecv >> TX_WITH_WITNESS(ptx);

// Lines 4263-4264: Compute identifiers
const uint256& txid = ptx->GetHash();      // Without witness
const uint256& wtxid = ptx->GetWitnessHash(); // With witness
```

**Visual:**
- Raw hex bytes stream in
- Transform into labeled structure:
  ```
  ┌─ CTransaction ─────────┐
  │ txid:   a1b2c3...       │
  │ wtxid:  d4e5f6...       │
  │ vin:    [2 inputs]      │
  │ vout:   [2 outputs]     │
  │ nLockTime: 0            │
  └─────────────────────────┘
  ```

**Narration:**
> "The raw bytes are parsed into a CTransaction object. Two identifiers are computed: txid, the traditional transaction ID, and wtxid, which includes witness data for SegWit transactions."

---

### SCENE 3: Download Management - Orphan Detection (2:30 - 3:45)

**Visual:**
- Transaction object now glowing, ready for next step
- Camera pans to "Download Manager" component (geometric structure)

**Code Overlay:**
```cpp
// src/net_processing.cpp - PeerManagerImpl::ProcessMessage
// src/node/txdownloadman.h:158 - TxDownloadManager::ReceivedTx
auto [should_validate, package_to_validate] =
    m_txdownloadman.ReceivedTx(pfrom.GetId(), ptx);
```

**Narration:**
> "Before validation, the Download Manager answers a critical question: Do we have all the parent transactions needed to validate this one?"

**Visual: Three-way branch visualization**

```
                    ReceivedTx()
                        |
          +-------------+-------------+
          |             |             |
    All parents    Missing parent   Parent arrives
      exist           (orphan)      (package!)
          |             |             |
       VALIDATE      STORE IN      VALIDATE
                   ORPHANAGE       AS PACKAGE
```

**Scenario 1: Normal Transaction (left path glows)**
- Parent UTXOs shown in UTXO set (database visual)
- ✓ All inputs found
- "should_validate = true"

**Scenario 2: Orphan (middle path glows)**
- One input's parent missing (shown as ???)
- Transaction placed in "TxOrphanage" (temporary holding area)
- Visual: Glowing cube labeled "Orphanage (weight & latency-limited)"

**Scenario 3: Package (right path glows)**
- Parent tx arrives from orphanage
- Both parent + child light up
- "package_to_validate = {parent, child}"
- Caption: "Child-Pays-For-Parent (CPFP)"

**Code Reference:**
```
src/node/txorphanage.h - TxOrphanage limits per peer and globally
```

**Narration:**
> "Normal transactions proceed to validation immediately. Orphans wait in temporary storage based on weight and latency limits. When an orphan's parent arrives, both can be validated together as a package, enabling Child-Pays-For-Parent fee bumping."

---

### SCENE 4: Validation Pipeline Entrance (3:45 - 4:30)

**Visual:**
- Transaction enters a massive neon "pipeline" structure
- Pipeline has 5 distinct chambers, each glowing differently
- Labels: "PreChecks", "RBF Checks", "Policy Scripts", "Consensus Scripts", "Finalization"

**Code Overlay:**
```cpp
// src/validation.cpp:4547 - Entry point from net_processing
MempoolAcceptResult ChainstateManager::ProcessTransaction(
    const CTransactionRef& tx, bool test_accept = false)
{
    return AcceptToMemoryPool(m_active_chainstate, tx, ...);
}

// src/validation.cpp:1860 - Main validation orchestrator
MempoolAcceptResult AcceptToMemoryPool(...) {
    MemPoolAccept mem_pool_accept(pool, active_chainstate);
    return mem_pool_accept.AcceptSingleTransaction(tx, args);
}
```

**Visual:**
- Transaction enters rotating "MemPoolAccept" object
- Internal state shown: Workspace, coin cache, validation state

**Narration:**
> "The transaction enters the validation pipeline. The MemPoolAccept class orchestrates all checks, maintaining a temporary workspace and coin cache throughout the process."

---

### SCENE 5: Stage 1 - PreChecks (4:30 - 7:00)

**Visual:**
- First chamber of pipeline activates
- 16 validation stations appear, each with a checkpoint icon
- Transaction data flows through each checkpoint sequentially

**Title Card:** "STAGE 1: PreChecks - Fast Fail-Early Validation"

**Animation: Checklist appearing one by one with visual indicators**

#### Check 1-3: Basic Structure
```cpp
// src/validation.cpp:802
// src/consensus/tx_check.cpp - CheckTransaction
CheckTransaction(tx)  ✓
```
**Visual:**
- Transaction structure diagram
- Inputs/outputs highlighted
- ✓ Not empty, valid sizes, no duplicates

#### Check 4: Standard Format
```cpp
// src/validation.cpp:812
// src/policy/policy.cpp - IsStandardTx
IsStandardTx(tx)  ✓
```
**Visual:**
- Script type badges: P2PKH, P2WPKH, P2SH, P2WSH, P2TR
- ✓ All outputs use standard types

#### Check 5: Finality
```cpp
// Line 823
CheckFinalTxAtTip(tx)  ✓
```
**Visual:**
- Clock showing current block height
- nLockTime value compared
- ✓ Locktime satisfied

#### Check 6-7: Mempool Conflicts
```cpp
// Lines 827-847
Check mempool for duplicates  ✓
Check for input conflicts     ✓
```
**Visual:**
- Mempool shown as grid of transactions
- Search animation: scanning for same txid
- Input check: scanning for same outpoints
- ✓ No conflicts found

#### Check 8: UTXO Availability
```cpp
// src/validation.cpp:853-872
// Checks the CCoinsViewCache for each input
for (const CTxIn& txin : tx.vin) {
    if (!m_view.HaveCoin(txin.prevout)) {
        return state.Invalid(TxValidationResult::TX_MISSING_INPUTS);
    }
}
```
**Visual:**
- UTXO database visualization (chainstate)
- Each input lights up as its UTXO is found
- Input 1: a7b8c9:0 → ✓ Found (0.5 BTC)
- Input 2: d1e2f3:1 → ✓ Found (0.3 BTC)

**Narration:**
> "Every input must reference a real, unspent output. The coin view checks the UTXO set - if any input is missing or already spent, validation fails immediately."

#### Check 9-10: Input Values
```cpp
// src/validation.cpp:896
// src/consensus/tx_verify.cpp - CheckTxInputs (validates no value overflow)
Consensus::CheckTxInputs(tx, state, m_view)  ✓
```
**Visual:**
- Math overlay:
  ```
  Inputs:  0.5 + 0.3 = 0.8 BTC
  Outputs: 0.4 + 0.3 = 0.7 BTC
  Fee:     0.8 - 0.7 = 0.1 BTC ✓
  ```
- ✓ Inputs ≥ Outputs

#### Check 11-13: Script & Witness Checks
```cpp
// Lines 900-905
AreInputsStandard(tx)  ✓
IsWitnessStandard(tx)  ✓
```
**Visual:**
- Script icons for each input
- Witness data structure
- ✓ All standard formats

#### Check 14: Sigop Cost
```cpp
// src/validation.cpp:942
// src/policy/policy.h:40
GetTransactionSigOpCost(tx) ≤ MAX_STANDARD_TX_SIGOPS_COST  ✓
// MAX_STANDARD_TX_SIGOPS_COST = 16000
```
**Visual:**
- Counter: "Sigops: 142 / 16000"
- ✓ Under limit

#### Check 15-16: Fee Checks
```cpp
// src/validation.cpp:952-961
// src/policy/policy.h:66 - DEFAULT_MIN_RELAY_TX_FEE = 100 sat/kvB (0.1 sat/vB)
Fee rate ≥ minRelayTxFee (0.1 sat/vB)  ✓ (100 sat/vB)
Fee rate ≥ mempool minimum              ✓ (5 sat/vB current - dynamic)
```
**Visual:**
- Fee rate bar chart
- Minimum relay fee line (0.1 sat/vB - policy floor)
- Mempool minimum line (5 sat/vB - dynamic, rises when full)
- Our tx fee (100 sat/vB)
- ✓ Exceeds both minimums

**Narration:**
> "Sixteen rapid checks ensure the transaction is well-formed, economically rational, and meets network standards. Only after passing all these do we proceed to the expensive cryptographic validation."

---

### SCENE 6: Stage 2 - RBF Checks (7:00 - 8:00)

**Visual:**
- Chamber 2 activates
- Conditional glow: "IF conflicts exist..."

**Title Card:** "STAGE 2: Replace-By-Fee Validation (BIP 125)"

**Visual: Two scenarios side-by-side**

**Left: No Conflicts**
- Empty conflict set: `m_conflicts = {}`
- Stage skipped (ghosted out)
- Fast-forward animation

**Right: RBF Scenario**
```cpp
// Lines 1087-1245
if (!m_conflicts.empty()) {
    ReplacementChecks(ws);
}
```

**Visual: Original tx vs Replacement tx comparison**
```
Original Transaction          Replacement Transaction
─────────────────────        ───────────────────────
Fee:     0.05 BTC             Fee:     0.08 BTC  ✓
Feerate: 50 sat/vB            Feerate: 80 sat/vB ✓
Size:    200 vB               Size:    250 vB
```

**Checks animated:**
1. ✓ BIP 125 signaling (sequence < 0xfffffffe)
2. ✓ Higher absolute fee (0.08 > 0.05)
3. ✓ Higher fee rate (80 > 50)
4. ✓ No new unconfirmed inputs
5. ✓ Pays for bandwidth (extra fee ≥ relay fee × size)

**Narration:**
> "If the transaction conflicts with existing mempool entries, Replace-By-Fee rules ensure the replacement is strictly better for miners and doesn't enable denial-of-service attacks."

---

### SCENE 7: Stage 3 - Policy Script Checks (8:00 - 9:00)

**Visual:**
- Chamber 3 glows cyan
- Script execution engine appears (virtual machine visualization)

**Title Card:** "STAGE 3: Policy Script Validation"

**Code Overlay:**
```cpp
// src/validation.cpp:1247-1268
// src/script/interpreter.h - STANDARD_SCRIPT_VERIFY_FLAGS
constexpr unsigned int scriptVerifyFlags = STANDARD_SCRIPT_VERIFY_FLAGS;

// src/validation.cpp - CheckInputScripts with policy flags
CheckInputScripts(tx, state, m_view, scriptVerifyFlags,
                  true, false, ws.m_precomputed_txdata,
                  GetValidationCache());
```

**Narration:**
> "Now the expensive part: cryptographic validation. Each input's script must execute successfully, and all signatures must verify."

**Visual: Script execution for one input**

**Input 0 execution:**
```
ScriptSig:  <signature> <pubkey>
ScriptPubKey: OP_DUP OP_HASH160 <hash> OP_EQUALVERIFY OP_CHECKSIG
```

**Animation: Stack-based execution**
1. `<signature>` → Push to stack
2. `<pubkey>` → Push to stack
3. `OP_DUP` → Duplicate pubkey
4. `OP_HASH160` → Hash pubkey
5. `<hash>` → Push expected hash
6. `OP_EQUALVERIFY` → Compare & verify
7. `OP_CHECKSIG` → Verify signature

**Visual:**
- Stack visualization showing each operation
- Signature verification: ECDSA curve math visualization (brief)
- ✓ Signature valid
- Cache icon: "Store result in script cache"

**For multiple inputs:**
- All inputs shown executing in parallel (animated simultaneously)
- Input 0: ✓ Verified
- Input 1: ✓ Verified

**Narration:**
> "Script validation uses stricter policy flags - more restrictive than consensus requires. This catches potentially problematic transactions early, before they waste network resources. Successful executions are cached to speed up future block validation."

---

### SCENE 8: Stage 4 - Consensus Script Checks (9:00 - 9:45)

**Visual:**
- Chamber 4 glows purple (different from cyan)
- Same script engine, but with different flags label

**Title Card:** "STAGE 4: Consensus Script Validation"

**Code Overlay:**
```cpp
// src/validation.cpp:1270-1301
// src/versionbits.cpp - GetBlockScriptFlags (consensus flags from chain tip)
unsigned int currentBlockScriptVerifyFlags =
    GetBlockScriptFlags(*m_active_chainstate.m_chain.Tip(), ...);

// Validates with consensus-level flags
CheckInputsFromMempoolAndCache(tx, state, m_view, m_pool,
                               currentBlockScriptVerifyFlags,
                               ws.m_precomputed_txdata,
                               m_active_chainstate.CoinsTip());
```

**Visual comparison:**
```
Policy Flags              Consensus Flags
─────────────────        ──────────────────
✓ STRICTENC              ✓ STRICTENC
✓ DERSIG                 ✓ DERSIG
✓ NULLDUMMY              ✓ NULLDUMMY
✓ WITNESS                ✓ WITNESS
✓ TAPROOT                ✓ TAPROOT
✓ MINIMALDATA            (not required)
✓ DISCOURAGE_UPGRADABLE  (not required)
```

**Animation:**
- Scripts re-execute with consensus flags
- Some checks skipped (shown ghosted)
- ✓ All inputs valid under consensus rules
- Cache updated

**Narration:**
> "Scripts are validated again with consensus-level flags - exactly what will be enforced when this transaction is included in a block. This ensures future block validation will succeed and caches the results for that eventual validation."

---

### SCENE 9: Stage 5 - Finalization & Mempool Admission (9:45 - 11:00)

**Visual:**
- Final chamber glows green
- Transaction approaching mempool (large, glowing pool structure)

**Title Card:** "STAGE 5: Finalization"

**Step 1: Remove Conflicts (if RBF)**
```cpp
// src/validation.cpp:1303-1327
void FinalizeSubpackage() {
    for (const auto& conflict : m_conflicts) {
        m_pool.removeRecursive(conflict);
    }
}
```

**Visual:**
- If RBF: Original transaction fades out of mempool
- New transaction takes its place

**Step 2: Mempool Size Management**
```cpp
// src/validation.cpp:1485-1496
// src/kernel/mempool_options.h:19 - DEFAULT_MAX_MEMPOOL_SIZE_MB = 300
if (!bypass_limits) {
    LimitMempoolSize(m_pool, m_active_chainstate.CoinsTip());
}
```

**Visual:**
- Mempool capacity meter: "Memory: 298 MB / 300 MB"
- If full: Eviction animation
  - Lowest feerate transactions highlighted (red glow)
  - Ejected from mempool (fall out of visualization)
- Our transaction: Safe (high feerate)

**Step 3: Signal Emission**
```cpp
// src/validation.cpp:1498-1508
// src/validationinterface.h - CValidationInterface signals
GetMainSignals().TransactionAddedToMempool(
    tx, m_pool.GetInfo(tx_handle), entry_height
);
```

**Visual:**
- Signal pulse emanates from transaction
- Multiple recipients shown:
  - Wallet: "Update balance" ✓
  - Fee Estimator: "Record fee rate" ✓
  - RPC Server: "Notify subscribers" ✓

**Step 4: Mempool Entry**
**Visual:**
- Transaction settles into mempool
- Mempool shown as grid sorted by fee rate
- Our transaction positioned by fee rate (descending order)
- Transaction data shown:
  ```
  ┌─ Mempool Entry ────────┐
  │ txid:   a1b2c3...       │
  │ Fee:    0.1 BTC         │
  │ Size:   250 vB          │
  │ Rate:   100 sat/vB      │
  │ Time:   14:23:15 UTC    │
  │ Ancestors: 2            │
  │ Descendants: 0          │
  └─────────────────────────┘
  ```

**Narration:**
> "The transaction is officially in the mempool! Signals notify other subsystems - the wallet updates balances, fee estimation records the data point, and RPC subscribers are informed. The transaction is now ready for mining."

---

### SCENE 10: Relay to Network (11:00 - 12:00)

**Visual:**
- Return to network view from Scene 2
- Our node now glowing (has the tx)
- Connected peers shown (8 peers)

**Code Overlay:**
```cpp
// src/net_processing.cpp - After successful mempool admission
void PeerManagerImpl::ProcessValidTx(NodeId nodeid,
                                      const CTransactionRef& ptx,
                                      ...) {
    // Relay to other peers using INV announcements
    for (CNode* pnode : m_nodes) {
        if (pnode->ShouldRelayTx(ptx)) {
            RelayTransaction(ptx, pnode);
        }
    }
}
```

**Animation:**
- Transaction announcement (INV message) sent to peers
- Messages propagate outward:
  ```
  OUR NODE ──[INV(wtxid)]──> Peer 1, 2, 3, 4, 5, 6, 7, 8
  ```
- Some peers request full tx (GETDATA)
- Our node sends full transaction to requesting peers

**Visual: Network propagation visualization**
- Ripple effect across global map
- Nodes lighting up as they receive the transaction
- Within seconds: Thousands of nodes

**Narration:**
> "Finally, the transaction is relayed to connected peers. They'll perform the same validation, and if successful, relay it further. Within seconds, the transaction has propagated across the entire Bitcoin network, waiting in mempools worldwide for a miner to include it in a block."

---

### SCENE 11: Rejection Path (Alternative Flow) (12:00 - 13:00)

**Visual:**
- Rewind animation to validation pipeline
- This time, show a transaction failing

**Title Card:** "Alternative Path: Rejection"

**Scenario: Invalid Signature**

**Visual:**
- Enter PolicyScriptChecks stage
- Script execution begins
- Signature verification: ❌ FAILS
- Red X appears

**Code Overlay:**
```cpp
// Validation state
TxValidationResult::TX_INPUTS_NOT_STANDARD
state.SetRejectReason("mandatory-script-verify-flag-failed");
```

**Animation: Cleanup & Orphan Check**
```cpp
// src/net_processing.cpp:2980
std::optional<PackageToValidate> ProcessInvalidTx(...) {
    // Could this be valid as part of a package?
    if (state.GetResult() == TxValidationResult::TX_MISSING_INPUTS) {
        // Try 1-parent-1-child package validation
        return TryPackageValidation(...);
    }

    // Permanent failure - add to bloom filter
    m_recent_rejects.insert(tx.GetHash());
    return std::nullopt;
}
```

**Visual:**
- Transaction ejected from pipeline
- Two outcomes:
  1. **Temporary failure** (missing inputs): → TxOrphanage
  2. **Permanent failure** (invalid): → Bloom filter (reject cache)

**Bloom filter visualization:**
- Rejected txid added to filter
- Future attempts: Instant rejection (cache hit)

**Narration:**
> "Not all transactions succeed. Failures are categorized: temporary failures like missing inputs result in orphan storage, while permanent failures like invalid signatures are cached to prevent reprocessing."

---

### SCENE 12: Summary & Key Insights (13:00 - 14:00)

**Visual:**
- Zoom out to show entire pipeline end-to-end
- All 5 stages highlighted sequentially

**Title Card:** "Key Insights"

**Insight 1: Defense in Depth**
```
Network Layer    → Protocol validation
Download Mgmt    → Orphan detection
PreChecks        → Fast structural validation
Script Checks    → Cryptographic security (2 passes)
Finalization     → Economic policy
```
**Visual:** Shield icons stacking to form fortress

**Insight 2: Performance Optimization**
```
Fast Checks First    → CPU DoS protection
Cache Everything     → Script cache, coin cache
Fail Early          → Don't waste resources
```
**Visual:** Speed meter and cache icons

**Insight 3: Economic Incentives**
```
Fee-based admission  → Must pay to play
Fee-based eviction   → Lowest feerate goes first
RBF support          → Can bid higher
```
**Visual:** Fee rate chart

**Insight 4: Network Efficiency**
```
Orphan handling      → Out-of-order receipt OK
Package validation   → CPFP support
Relay optimization   → BIP 152 compact blocks
```
**Visual:** Network topology

**Narration:**
> "Bitcoin Core's transaction validation is a masterclass in defensive programming: multiple layers of protection, performance-first design, and economic rationality. Every check serves a purpose - protecting against attacks while enabling a thriving fee market."

---

### SCENE 13: Closing & Resources (14:00 - 14:30)

**Visual:**
- Code rain returns (like opening)
- File paths appear:

```
Key Files:
  src/net_processing.cpp      (P2P handling)
  src/validation.cpp          (Validation pipeline)
  src/txmempool.h             (Mempool data structure)
  src/consensus/tx_check.cpp  (Consensus checks)
  src/policy/policy.cpp       (Policy rules)
```

**Title Card:**
```
Explore More:
  - RBF Deep Dive
  - Script Validation Engine
  - Orphan Transaction Management
  - Package Relay (BIP 331)
```

**Narration:**
> "This is just one piece of Bitcoin Core's architecture. In future videos, we'll dive deeper into RBF mechanics, the script validation engine, and the emerging package relay protocol. The complete source code is available at github.com/bitcoin/bitcoin."

**Visual:**
- Fade to Bitcoin Core logo
- Credits roll with contributor count: "600+ contributors since 2009"

---

## Technical Animation Notes

### Code Display System
- Use syntax-highlighted C++ (VS Code Dark+ theme)
- Monospace font: JetBrains Mono or Fira Code
- File paths in top-right corner
- Line numbers in gray
- Active lines highlighted with neon glow

### Data Flow Visualization
- Use particle systems for data movement
- Color-coded by stage (cyan → magenta → yellow → purple → green)
- Speed varies by validation stage (fast checks = fast particles)

### Performance Metrics Overlay
- Optional timing overlay: "PreChecks: 0.8ms, ScriptChecks: 12.3ms"
- Validation cache hit rate: "Cache hits: 87%"

---

## Assets Needed

### 3D Models
- Network node (sphere with antenna)
- Pipeline chambers (cylindrical segments)
- Mempool pool (contained liquid simulation)
- UTXO database (grid/matrix visualization)

### Icons
- Checkmark (validation passed)
- X (validation failed)
- Shield (security check)
- Clock (timelock)
- Key (signature verification)
- Cache (script cache, coin cache)

### Sound Design
- Network packet arrival: Digital "ping"
- Validation check pass: Soft "ding"
- Validation check fail: Low "buzz"
- Script execution: Keyboard typing sounds
- Mempool admission: Satisfying "splash"
- Relay propagation: Ascending tone

---

## Production Notes

**Manim Implementation:**
- Create `IncomingTransactionFlow` scene class
- Reusable components:
  - `CodeOverlay(code, file, lines)` - syntax highlighted code display
  - `ValidationCheck(name, result)` - animated checkbox
  - `DataFlow(from_obj, to_obj, data_label)` - particle stream
  - `PipelineStage(name, color)` - validation chamber
  - `NetworkRelay(nodes, tx)` - network propagation

**Render Strategy:**
- Render each scene separately at high quality
- Scene 5 (PreChecks) will be longest to render (16 individual animations)
- Use scene caching for repeated elements
- Target 4K output for future-proofing

**Accessibility:**
- Closed captions with technical terms defined
- Audio descriptions for complex visuals
- Companion blog post with static diagrams
- Code snippets available in text format

---

This script provides a comprehensive, code-accurate visualization of Bitcoin Core's transaction processing, suitable for developers and technical audiences wanting to understand the implementation details.
