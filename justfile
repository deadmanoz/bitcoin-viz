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
preview scene_name file="act1_creation":
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
render scene_name file="transaction_lifecycle":
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
render-hq scene_name file="transaction_lifecycle":
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
render-4k scene_name file="transaction_lifecycle":
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
    @just preview TransactionLifecycleIntro transaction_lifecycle
    @just preview TheWallet act1_creation
    @just preview TransactionConstruction act1_creation
    @just preview InitialBroadcast act2_propagation
    @just preview NodeValidation act2_propagation
    @just preview MempoolWaiting act3_mempool
    @just preview BlockTemplate act4_mining
    @just preview Mining act4_mining
    @just preview BlockPropagation act5_confirmation
    @just preview ChainExtension act5_confirmation

# Render all incoming transaction scenes at preview quality
preview-incoming:
    @just preview IncomingTransactionIntro incoming_transaction
    @just preview NetworkLayer incoming_transaction
    @just preview DownloadManagement incoming_transaction
    @just preview ValidationPipeline incoming_transaction
    @just preview PreChecks incoming_transaction
    @just preview MempoolAdmission incoming_transaction

# Render complete incoming transaction sequence
render-incoming quality="ql":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    export PATH="./venv/bin:$PATH"
    echo "Rendering incoming transaction processing at {{quality}}..."
    manim -{{quality}} animations/incoming_transaction.py IncomingTransactionIntro
    manim -{{quality}} animations/incoming_transaction.py NetworkLayer
    manim -{{quality}} animations/incoming_transaction.py DownloadManagement
    manim -{{quality}} animations/incoming_transaction.py ValidationPipeline
    manim -{{quality}} animations/incoming_transaction.py PreChecks
    manim -{{quality}} animations/incoming_transaction.py MempoolAdmission
    echo "✓ All incoming transaction scenes rendered"

# Render complete transaction lifecycle (all acts)
render-lifecycle quality="ql":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    export PATH="./venv/bin:$PATH"
    echo "Rendering complete transaction lifecycle at {{quality}}..."
    manim -{{quality}} animations/act1_creation.py TheWallet
    manim -{{quality}} animations/act1_creation.py TransactionConstruction
    manim -{{quality}} animations/act2_propagation.py InitialBroadcast
    manim -{{quality}} animations/act2_propagation.py NodeValidation
    manim -{{quality}} animations/act3_mempool.py MempoolWaiting
    manim -{{quality}} animations/act4_mining.py BlockTemplate
    manim -{{quality}} animations/act4_mining.py Mining
    manim -{{quality}} animations/act5_confirmation.py BlockPropagation
    manim -{{quality}} animations/act5_confirmation.py ChainExtension
    echo "✓ All lifecycle scenes rendered"

# Join rendered lifecycle videos into single video
join-lifecycle quality="480p15":
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Joining transaction lifecycle videos at {{quality}} quality..."

    # Define the video files in order
    videos=(
        "media/videos/act1_creation/{{quality}}/TheWallet.mp4"
        "media/videos/act1_creation/{{quality}}/TransactionConstruction.mp4"
        "media/videos/act2_propagation/{{quality}}/InitialBroadcast.mp4"
        "media/videos/act2_propagation/{{quality}}/NodeValidation.mp4"
        "media/videos/act3_mempool/{{quality}}/MempoolWaiting.mp4"
        "media/videos/act4_mining/{{quality}}/BlockTemplate.mp4"
        "media/videos/act4_mining/{{quality}}/Mining.mp4"
        "media/videos/act5_confirmation/{{quality}}/BlockPropagation.mp4"
        "media/videos/act5_confirmation/{{quality}}/ChainExtension.mp4"
    )

    # Check if all videos exist
    for video in "${videos[@]}"; do
        if [ ! -f "$video" ]; then
            echo "Error: $video not found. Run 'just render-lifecycle' first."
            exit 1
        fi
    done

    # Create temporary file list for ffmpeg
    temp_list=$(mktemp)
    for video in "${videos[@]}"; do
        echo "file '$PWD/$video'" >> "$temp_list"
    done

    # Create output directory if needed
    mkdir -p media/videos/full_lifecycle/{{quality}}

    # Join videos using ffmpeg
    output="media/videos/full_lifecycle/{{quality}}/TransactionLifecycle_Complete.mp4"
    ffmpeg -f concat -safe 0 -i "$temp_list" -c copy "$output" -y

    # Cleanup
    rm "$temp_list"

    echo "✓ Complete lifecycle video created:"
    echo "  $output"
    du -h "$output"

# List all available scenes in a file - usage: just list-scenes [file]
list-scenes file="act1_creation":
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
