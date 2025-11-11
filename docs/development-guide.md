# Development Guide

## Prerequisites

- Python 3.11+
- [just](https://github.com/casey/just) command runner
- System dependencies for manim (automatically installed on Linux)

## Getting Started

### 1. Initial Setup

Clone the repository and run the setup command:

```bash
git clone <repo-url>
cd bitcoin-viz
just setup
```

This will:
- Create a Python virtual environment in `venv/`
- Install all dependencies from `requirements.txt`
- Set up manim and its dependencies

### 2. Development Workflow

The `justfile` provides common commands for daily development:

```bash
# See all available commands
just --list

# Render a scene for quick preview
just preview BitcoinVehicleIntro

# Render at higher quality
just render BitcoinVehicleIntro        # 720p
just render-hq BitcoinVehicleIntro     # 1080p
just render-4k BitcoinVehicleIntro     # 4K

# List available scenes
just list-scenes

# Check project stats
just stats
```

### 3. Creating New Animations

1. Create a new Python file in `animations/`:
   ```bash
   touch animations/my_new_scene.py
   ```

2. Define your scene class:
   ```python
   from manim import *

   class MyNewScene(Scene):
       def construct(self):
           # Your animation code here
           text = Text("Hello Bitcoin!")
           self.play(Write(text))
           self.wait(1)
   ```

3. Render it:
   ```bash
   just preview MyNewScene my_new_scene
   ```

### 4. Working with the Virtual Environment

The justfile handles the venv automatically, but if you need direct access:

```bash
# Activate the venv (for manual operations)
source venv/bin/activate

# Deactivate when done
deactivate

# Run Python scripts in the venv (via just)
just python my_script.py

# Update dependencies after modifying requirements.txt
just install
```

### 5. File Organization

```
bitcoin-viz/
├── animations/              # Manim scene files
│   └── *.py                 # Scene definitions
├── assets/                  # Static assets
│   ├── images/              # Images and logos
│   ├── svgs/                # Vector graphics
│   └── audio/               # Sound effects, music
├── bitcoin_hooks/           # Bitcoin Core integration utilities
├── docs/                    # Documentation
├── media/                   # Rendered output (git-ignored)
│   └── videos/
│       └── scene_name/
│           ├── 480p15/      # Preview quality
│           ├── 720p30/      # Medium quality
│           ├── 1080p60/     # High quality
│           └── 2160p60/     # 4K quality
├── scripts/                 # Helper scripts
├── venv/                    # Virtual environment (git-ignored)
├── justfile                 # Command runner recipes
└── requirements.txt         # Python dependencies
```

## Manim Basics

### Scene Structure

A manim scene follows this pattern:

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # 1. Create objects
        circle = Circle()
        text = Text("Bitcoin")

        # 2. Animate them
        self.play(Create(circle))
        self.play(Write(text))

        # 3. Transform/manipulate
        self.play(circle.animate.scale(2))

        # 4. Wait (important for pacing)
        self.wait(2)
```

### Common Animations

```python
# Text
self.play(Write(text))              # Write text letter by letter
self.play(FadeIn(text))             # Fade in
self.play(FadeOut(text))            # Fade out

# Shapes
self.play(Create(circle))           # Draw shape
self.play(DrawBorderThenFill(rect)) # Draw border then fill

# Transformations
self.play(obj.animate.scale(2))     # Scale
self.play(obj.animate.shift(UP))    # Move
self.play(obj.animate.rotate(PI/4)) # Rotate

# Scene transitions
self.play(Transform(obj1, obj2))    # Morph one object into another
self.play(ReplacementTransform(obj1, obj2))  # Replace with new object
```

### Positioning

```python
# Absolute positioning
obj.to_edge(UP)           # Move to top edge
obj.to_corner(UL)         # Move to upper-left corner
obj.move_to(ORIGIN)       # Center

# Relative positioning
obj2.next_to(obj1, RIGHT) # Place to the right of obj1
obj2.align_to(obj1, UP)   # Align tops

# Directional vectors
UP, DOWN, LEFT, RIGHT
UL, UR, DL, DR           # Corners
ORIGIN                    # Center (0,0,0)
```

### Grouping Objects

```python
group = VGroup(obj1, obj2, obj3)
self.play(Create(group))             # Animate all together
group.arrange(RIGHT, buff=0.5)       # Arrange horizontally with spacing
```

## Quality Settings

| Quality | Resolution | FPS | Use Case | Render Time |
|---------|-----------|-----|----------|-------------|
| `-ql` (low) | 480p | 15 | Quick previews, iteration | Fastest (~10s) |
| `-qm` (medium) | 720p | 30 | Review, sharing drafts | Medium (~30s) |
| `-qh` (high) | 1080p | 60 | Production, YouTube | Slower (~2min) |
| `-qk` (4k) | 2160p | 60 | Final export, archival | Slowest (~5min) |

## Best Practices

### 1. Iterate Quickly
- Always start with `-ql` (preview quality) for fast iteration
- Only render higher quality when the animation is finalized

### 2. Use Wait Statements
```python
self.wait(1)  # Pause for 1 second
```
This gives viewers time to process information.

### 3. Consistent Timing
- Keep animations between 0.5-1.5 seconds
- Use `run_time` parameter for custom timing:
  ```python
  self.play(Create(circle), run_time=2)
  ```

### 4. Color Schemes
Use consistent colors for related concepts:
```python
# Bitcoin theme colors
BITCOIN_ORANGE = "#F7931A"
BITCOIN_GRAY = "#4D4D4D"

# Manim built-in colors
BLUE, RED, GREEN, YELLOW, PURPLE, ORANGE
DARK_GRAY, LIGHT_GRAY, WHITE, BLACK
```

### 5. Text Sizing
```python
title = Text("Title", font_size=48)
subtitle = Text("Subtitle", font_size=32)
body = Text("Body text", font_size=24)
caption = Text("Caption", font_size=18)
```

### 6. Organize Complex Scenes
Break complex animations into methods:
```python
class ComplexScene(Scene):
    def construct(self):
        self.show_intro()
        self.demonstrate_concept()
        self.show_conclusion()

    def show_intro(self):
        # Intro animation
        pass

    def demonstrate_concept(self):
        # Main content
        pass

    def show_conclusion(self):
        # Wrap up
        pass
```

## Debugging

### Preview Without Rendering
Use manim's interactive mode:
```bash
source venv/bin/activate
manim animations/my_scene.py MyScene -p --preview
```

### Check for Errors
```bash
# Verbose output
manim -ql animations/my_scene.py MyScene -v DEBUG
```

### Common Issues

**Problem:** "Scene not found"
- Check class name matches exactly (case-sensitive)
- Ensure class inherits from `Scene`

**Problem:** Objects not visible
- Check positioning (might be off-screen)
- Verify colors (white on white won't show)
- Use `self.add()` instead of `self.play()` for debugging

**Problem:** Animation too fast/slow
- Add `self.wait()` statements
- Adjust `run_time` parameter

## Resources

- [Manim Community Documentation](https://docs.manim.community/)
- [Manim Example Gallery](https://docs.manim.community/en/stable/examples.html)
- [3Blue1Brown's Videos](https://www.youtube.com/c/3blue1brown) - Inspiration
- [Bitcoin Core Documentation](https://bitcoincore.org/en/doc/)

## Contributing

1. Create animations in `animations/` directory
2. Add documentation for complex concepts in `docs/`
3. Use descriptive scene names
4. Comment complex animation logic
5. Test renders at multiple quality levels before finalizing
6. Keep rendered videos out of git (they're in `.gitignore`)

## Tips for Bitcoin Visualizations

1. **Start Simple**: Begin with high-level concepts, add complexity gradually
2. **Use Metaphors**: The vehicle metaphor helps non-technical viewers
3. **Show, Don't Tell**: Animate transformations rather than static diagrams
4. **Real Data**: Consider integrating real Bitcoin network data when possible
5. **Code Context**: Show relevant Bitcoin Core code snippets when appropriate
6. **Consistency**: Maintain visual language across episodes (colors, shapes, metaphors)

## Getting Help

- Check the [manim documentation](https://docs.manim.community/)
- Look at existing scenes in `animations/` for examples
- Review `docs/episode-ideas.md` for content inspiration
- Experiment! Manim makes it easy to try things quickly
