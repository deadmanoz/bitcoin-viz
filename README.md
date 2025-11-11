# Bitcoin Visualization Project

Inspired by 3Blue1Brown, this project creates educational animations explaining how Bitcoin works by peeling back layers of abstraction.

## Concept

Using a synthwave/cyberpunk visual style with neon colors on dark backgrounds, we explore Bitcoin's technical internals through smooth, engaging animations. Starting with the transaction lifecycle, we'll progressively dive deeper into consensus, networking, and cryptographic mechanisms.

## Structure

```
bitcoin-viz/
├── animations/          # Manim scene files
├── assets/             # Visual assets (SVGs, images)
├── bitcoin_hooks/      # Python utilities for Bitcoin Core integration
├── scripts/            # Helper scripts
├── docs/               # Storyboards and documentation
└── media/              # Rendered videos (git-ignored)
```

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

# Rendering animations
just preview SceneName [file]     # Quick preview (480p)
just render SceneName [file]      # Medium quality (720p)
just render-hq SceneName [file]   # High quality (1080p)
just render-4k SceneName [file]   # 4K quality (2160p)

# Utilities
just preview-all        # Render all POC scenes
just list-scenes [file] # List available scenes in a file
just stats              # Show project statistics
just clean              # Remove rendered media files
just clean-all          # Remove media + venv

# Examples
just preview TransactionLifecycleIntro transaction_lifecycle
just preview Act1_TheWallet transaction_lifecycle
just list-scenes transaction_lifecycle
```

## Manual Usage (if you prefer not to use just)

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Render an animation
manim -ql animations/transaction_lifecycle.py TransactionLifecycleIntro
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
