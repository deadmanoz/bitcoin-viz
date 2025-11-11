# Bitcoin Visualization Project

Inspired by 3Blue1Brown, this project creates educational animations explaining how Bitcoin Core works by peeling back layers of abstraction.

## Concept

Using the metaphor of a vehicle/car to represent Bitcoin Core, we visually transform between high-level concepts and technical implementation details.

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

## Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Render an animation
manim -pql animations/scene_name.py SceneName
```

## Quality Flags

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
