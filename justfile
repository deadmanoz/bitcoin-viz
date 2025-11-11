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
preview scene_name file="transaction_lifecycle/act1_creation":
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
render scene_name file="transaction_lifecycle/transaction_lifecycle":
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
render-hq scene_name file="transaction_lifecycle/transaction_lifecycle":
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
render-4k scene_name file="transaction_lifecycle/transaction_lifecycle":
    #!/usr/bin/env bash
    set -euo pipefail
    if [ ! -d "venv" ]; then
        echo "Error: venv not found. Run 'just setup' first."
        exit 1
    fi
    export PATH="./venv/bin:$PATH"
    echo "Rendering {{scene_name}} at 4K quality (2160p)..."
    manim -qk animations/{{file}}.py {{scene_name}}

# Render all lifecycle scenes at preview quality
preview-lifecycle:
    @just preview TransactionLifecycleIntro transaction_lifecycle/transaction_lifecycle
    @just preview TheWallet transaction_lifecycle/act1_creation
    @just preview TransactionConstruction transaction_lifecycle/act1_creation
    @just preview InitialBroadcast transaction_lifecycle/act2_propagation
    @just preview NodeValidation transaction_lifecycle/act2_propagation
    @just preview MempoolWaiting transaction_lifecycle/act3_mempool
    @just preview BlockTemplate transaction_lifecycle/act4_mining
    @just preview Mining transaction_lifecycle/act4_mining
    @just preview BlockPropagation transaction_lifecycle/act5_confirmation
    @just preview ChainExtension transaction_lifecycle/act5_confirmation

# Render all incoming transaction scenes at preview quality
preview-incoming:
    @just preview IncomingTransactionIntro incoming_transaction/scenes
    @just preview NetworkLayer incoming_transaction/scenes
    @just preview DownloadManagement incoming_transaction/scenes
    @just preview ValidationPipeline incoming_transaction/scenes
    @just preview PreChecks incoming_transaction/scenes
    @just preview MempoolAdmission incoming_transaction/scenes

# Backward compatibility: preview-all renders all lifecycle scenes
preview-all:
    @just preview-lifecycle

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
    manim -{{quality}} animations/incoming_transaction/scenes.py IncomingTransactionIntro
    manim -{{quality}} animations/incoming_transaction/scenes.py NetworkLayer
    manim -{{quality}} animations/incoming_transaction/scenes.py DownloadManagement
    manim -{{quality}} animations/incoming_transaction/scenes.py ValidationPipeline
    manim -{{quality}} animations/incoming_transaction/scenes.py PreChecks
    manim -{{quality}} animations/incoming_transaction/scenes.py MempoolAdmission
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
    manim -{{quality}} animations/transaction_lifecycle/act1_creation.py TheWallet
    manim -{{quality}} animations/transaction_lifecycle/act1_creation.py TransactionConstruction
    manim -{{quality}} animations/transaction_lifecycle/act2_propagation.py InitialBroadcast
    manim -{{quality}} animations/transaction_lifecycle/act2_propagation.py NodeValidation
    manim -{{quality}} animations/transaction_lifecycle/act3_mempool.py MempoolWaiting
    manim -{{quality}} animations/transaction_lifecycle/act4_mining.py BlockTemplate
    manim -{{quality}} animations/transaction_lifecycle/act4_mining.py Mining
    manim -{{quality}} animations/transaction_lifecycle/act5_confirmation.py BlockPropagation
    manim -{{quality}} animations/transaction_lifecycle/act5_confirmation.py ChainExtension
    echo "✓ All lifecycle scenes rendered"

# Join rendered lifecycle videos into single video
join-lifecycle quality="480p15":
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Joining transaction lifecycle videos at {{quality}} quality..."

    # Define the video files in order
    videos=(
        "media/videos/transaction_lifecycle/act1_creation/{{quality}}/TheWallet.mp4"
        "media/videos/transaction_lifecycle/act1_creation/{{quality}}/TransactionConstruction.mp4"
        "media/videos/transaction_lifecycle/act2_propagation/{{quality}}/InitialBroadcast.mp4"
        "media/videos/transaction_lifecycle/act2_propagation/{{quality}}/NodeValidation.mp4"
        "media/videos/transaction_lifecycle/act3_mempool/{{quality}}/MempoolWaiting.mp4"
        "media/videos/transaction_lifecycle/act4_mining/{{quality}}/BlockTemplate.mp4"
        "media/videos/transaction_lifecycle/act4_mining/{{quality}}/Mining.mp4"
        "media/videos/transaction_lifecycle/act5_confirmation/{{quality}}/BlockPropagation.mp4"
        "media/videos/transaction_lifecycle/act5_confirmation/{{quality}}/ChainExtension.mp4"
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
    mkdir -p media/videos/transaction_lifecycle/{{quality}}

    # Join videos using ffmpeg
    output="media/videos/transaction_lifecycle/{{quality}}/transaction_lifecycle_complete.mp4"
    ffmpeg -f concat -safe 0 -i "$temp_list" -c copy "$output" -y

    # Cleanup
    rm "$temp_list"

    echo "✓ Complete lifecycle video created:"
    echo "  $output"
    du -h "$output"

# Join rendered incoming transaction videos into single video
join-incoming quality="480p15":
    #!/usr/bin/env bash
    set -euo pipefail
    echo "Joining incoming transaction videos at {{quality}} quality..."

    # Define the video files in order
    videos=(
        "media/videos/incoming_transaction/scenes/{{quality}}/IncomingTransactionIntro.mp4"
        "media/videos/incoming_transaction/scenes/{{quality}}/NetworkLayer.mp4"
        "media/videos/incoming_transaction/scenes/{{quality}}/DownloadManagement.mp4"
        "media/videos/incoming_transaction/scenes/{{quality}}/ValidationPipeline.mp4"
        "media/videos/incoming_transaction/scenes/{{quality}}/PreChecks.mp4"
        "media/videos/incoming_transaction/scenes/{{quality}}/MempoolAdmission.mp4"
    )

    # Check if all videos exist
    for video in "${videos[@]}"; do
        if [ ! -f "$video" ]; then
            echo "Error: $video not found. Run 'just render-incoming' first."
            exit 1
        fi
    done

    # Create temporary file list for ffmpeg
    temp_list=$(mktemp)
    for video in "${videos[@]}"; do
        echo "file '$PWD/$video'" >> "$temp_list"
    done

    # Create output directory if needed
    mkdir -p media/videos/incoming_transaction/{{quality}}

    # Join videos using ffmpeg
    output="media/videos/incoming_transaction/{{quality}}/incoming_transaction_complete.mp4"
    ffmpeg -f concat -safe 0 -i "$temp_list" -c copy "$output" -y

    # Cleanup
    rm "$temp_list"

    echo "✓ Complete incoming transaction video created:"
    echo "  $output"
    du -h "$output"

# List all available scenes in a file - usage: just list-scenes [file]
list-scenes file="transaction_lifecycle/act1_creation":
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
    find animations -name "*.py" -type f -not -name "__init__.py" | wc -l | xargs echo "  "
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
        echo "   0 (run 'just preview-lifecycle' to render lifecycle scenes)"
    fi

# Open rendered video directory
open-media:
    #!/usr/bin/env bash
    set -euo pipefail
    if [ -d "media/videos" ]; then
        echo "Media directory: $(pwd)/media/videos"
        echo ""
        echo "Transaction Lifecycle videos:"
        ls -lh media/videos/transaction_lifecycle/*/480p15/*.mp4 2>/dev/null || echo "  None found"
        echo ""
        echo "Incoming Transaction videos:"
        ls -lh media/videos/incoming_transaction/*/480p15/*.mp4 2>/dev/null || echo "  None found"
    else
        echo "No media files yet. Run 'just preview-lifecycle' or 'just preview-incoming' to render."
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
