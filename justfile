# Bitcoin Visualization Project - Common Operations
# Run `just` or `just --list` to see available commands

# Default recipe - show available commands
default:
    @just --list

# Set up virtual environment and install dependencies
setup:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "Installing dependencies..."
    ./venv/bin/pip install --upgrade pip wheel
    ./venv/bin/pip install -r requirements.txt
    echo ""
    echo "✓ Setup complete!"
    echo "To activate: source venv/bin/activate"

# Install or update dependencies (venv must exist)
install:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    echo "Installing dependencies..."
    ./venv/bin/pip install -r requirements.txt
    echo "✓ Dependencies installed"

# Render animation at low quality (preview) - usage: just preview SceneName [file]
preview scene_name file="bitcoin_vehicle_intro":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    export PATH="./venv/bin:$PATH"
    echo "Rendering {{scene_name}} at low quality (480p)..."
    manim -ql animations/{{file}}.py {{scene_name}}

# Render animation at medium quality (720p) - usage: just render SceneName [file]
render scene_name file="bitcoin_vehicle_intro":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    export PATH="./venv/bin:$PATH"
    echo "Rendering {{scene_name}} at medium quality (720p)..."
    manim -qm animations/{{file}}.py {{scene_name}}

# Render animation at high quality (1080p) - usage: just render-hq SceneName [file]
render-hq scene_name file="bitcoin_vehicle_intro":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    export PATH="./venv/bin:$PATH"
    echo "Rendering {{scene_name}} at high quality (1080p)..."
    manim -qh animations/{{file}}.py {{scene_name}}

# Render animation at 4K quality - usage: just render-4k SceneName [file]
render-4k scene_name file="bitcoin_vehicle_intro":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    export PATH="./venv/bin:$PATH"
    echo "Rendering {{scene_name}} at 4K quality (2160p)..."
    manim -qk animations/{{file}}.py {{scene_name}}

# Render all POC scenes at preview quality
preview-all:
    @just preview BitcoinVehicleIntro
    @just preview TransactionJourney

# List all available scenes in a file - usage: just list-scenes [file]
list-scenes file="bitcoin_vehicle_intro":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    export PATH="./venv/bin:$PATH"
    echo "Available scenes in animations/{{file}}.py:"
    grep "^class.*Scene):" animations/{{file}}.py | sed 's/class /  - /' | sed 's/(Scene):.*//'

# Clean rendered media files
clean:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Cleaning media files..."
    rm -rf media/
    echo "✓ Media files removed"

# Clean everything (media + venv)
clean-all:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Cleaning media files and virtual environment..."
    rm -rf media/ venv/
    echo "✓ All cleaned"

# Show project statistics
stats:
    #!/usr/bin/env bash
    set -euo pipefail
    echo "📊 Bitcoin Visualization Project Stats"
    echo ""
    echo "Animation files:"
    find animations -name "*.py" -type f | wc -l | xargs echo "  "
    echo ""
    echo "Documentation files:"
    find docs -name "*.md" -type f | wc -l | xargs echo "  "
    echo ""
    if [ -d "media" ]; then
        echo "Rendered videos:"
        find media -name "*.mp4" -type f | wc -l | xargs echo "  "
        echo ""
        echo "Total media size:"
        du -sh media/ | cut -f1 | xargs echo "  "
    else
        echo "Rendered videos:"
        echo "   0 (run 'just preview-all' to render POC scenes)"
    fi

# Open rendered video directory
open-media:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -d "media/videos" ]; then
        echo "Media directory: $(pwd)/media/videos"
        ls -lh media/videos/*/480p15/*.mp4 2>/dev/null || echo "No preview quality videos found"
    else
        echo "No media files yet. Run 'just preview-all' to render POC scenes."
    fi

# Run Python in the venv (useful for testing)
python *args:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    ./venv/bin/python {{args}}
