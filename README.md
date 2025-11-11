# Bitcoin Visualization Project

Inspired by 3Blue1Brown, this project creates educational animations explaining how Bitcoin works by peeling back layers of abstraction.

## Concept

Using a synthwave/cyberpunk visual style with neon colors on dark backgrounds, we explore Bitcoin's technical internals through smooth, engaging animations. Starting with the transaction lifecycle, we'll progressively dive deeper into consensus, networking, and cryptographic mechanisms.

## Structure

```
bitcoin-viz/
├── animations/          # Manim scene files
│   ├── common.py                   # Shared color palette and utilities
│   ├── transaction_lifecycle.py    # Intro scene + legacy Act scenes
│   ├── act1_creation.py           # Wallet & transaction construction
│   ├── act2_propagation.py        # Network broadcast & validation
│   ├── act3_mempool.py            # Mempool waiting area
│   ├── act4_mining.py             # Block template & mining
│   └── act5_confirmation.py       # Block propagation & chain extension
├── assets/             # Visual assets (SVGs, images)
├── bitcoin_hooks/      # Python utilities for Bitcoin Core integration
├── scripts/            # Helper scripts
├── docs/               # Storyboards and documentation
└── media/              # Rendered videos (git-ignored)
    └── videos/
        ├── act1_creation/          # Act 1 scene outputs
        ├── act2_propagation/       # Act 2 scene outputs
        ├── act3_mempool/           # Act 3 scene outputs
        ├── act4_mining/            # Act 4 scene outputs
        ├── act5_confirmation/      # Act 5 scene outputs
        └── full_lifecycle/         # Complete joined video
```

## Animation Organization

Each "Act" is separated into its own file for easier iteration:

- **Act 1: Creation** (`act1_creation.py`) - Wallet UTXO selection and transaction construction
- **Act 2: Propagation** (`act2_propagation.py`) - P2P network broadcast and node validation
- **Act 3: Mempool** (`act3_mempool.py`) - Fee-sorted waiting area
- **Act 4: Mining** (`act4_mining.py`) - Block template assembly and mining process
- **Act 5: Confirmation** (`act5_confirmation.py`) - Block propagation and chain extension

All acts share a common synthwave/cyberpunk color palette defined in `common.py`.

## Requirements

Before you begin, ensure you have the following installed:

- **Python 3.11+** - For running manim and animations
- **[just](https://github.com/casey/just)** - Command runner (optional but recommended)
  - macOS: `brew install just`
  - Ubuntu/Debian: `sudo snap install --edge --classic just`
  - Other: See [just installation docs](https://github.com/casey/just#installation)
- **ffmpeg** - Required for joining lifecycle videos into complete animations
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

Note: Manim and other Python dependencies are installed automatically via `just setup` into a virtual environment.

## Quick Start

This project uses [just](https://github.com/casey/just) as a command runner and a Python virtual environment to keep dependencies isolated.

```bash
# First time setup - creates venv and installs dependencies
just setup

# Render the POC animations at preview quality
just preview-all

# See all available commands
just --list
```

## Common Commands

```bash
# Setup and installation
just setup              # Create venv and install dependencies
just install            # Update dependencies (venv must exist)

# Rendering individual scenes
just preview SceneName [file]     # Quick preview (480p)
just render SceneName [file]      # Medium quality (720p)
just render-hq SceneName [file]   # High quality (1080p)
just render-4k SceneName [file]   # 4K quality (2160p)

# Rendering complete transaction lifecycle
just render-lifecycle [quality]   # Render all lifecycle scenes (default: ql)
just join-lifecycle [quality]     # Join scenes into single video (default: 480p15)

# Utilities
just preview-all        # Render all POC scenes at preview quality
just list-scenes [file] # List available scenes in a file
just stats              # Show project statistics
just clean              # Remove rendered media files
just clean-all          # Remove media + venv

# Examples - Individual scenes
just preview TheWallet act1_creation
just preview TransactionConstruction act1_creation
just preview MempoolWaiting act3_mempool
just list-scenes act1_creation

# Examples - Complete lifecycle video
just render-lifecycle ql          # Render all scenes at low quality
just join-lifecycle 480p15        # Join into single video
just render-lifecycle qm          # Render all at medium quality (720p)
just join-lifecycle 720p30        # Join medium quality videos
```

## Manual Usage (if you prefer not to use just)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Render an animation
manim -ql animations/act1_creation.py TheWallet
```

## Quality Flags (for manual manim usage)

- `-ql`: Low quality (480p) - fast preview
- `-qm`: Medium quality (720p)
- `-qh`: High quality (1080p)
- `-qk`: 4K quality (2160p)
- `-p`: Preview after rendering

## Vision

Create a video series that explains:
- Transaction journey through the network
- Validation engine internals
- Consensus mechanisms
- UTXO model
- P2P network dynamics
- Mempool processing
