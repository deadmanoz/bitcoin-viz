"""
TRANSACTION CONSTRUCTION - Bitcoin Transaction Lifecycle
=======================================================

Shows the complete transaction being assembled.
Runtime: ~30-45 seconds
"""

from manim import *
import numpy as np
import sys
import os
# Add parent directories to path to import common module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common import *


class TransactionConstruction(Scene):
    """
    Transaction Construction
    Shows the transaction being built as a data packet.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
        title = Text("Transaction Construction", font_size=38, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Continuity description
        description = Text(
            "Alice's wallet constructs a transaction to broadcast to the Bitcoin network",
            font_size=24,
            color=SYNTH_PEACH
        )
        description.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(description, shift=DOWN))
        self.wait(1)

        # Fade out description before showing blocks
        self.play(FadeOut(description))
        self.wait(0.3)

        # Define transaction components (in order from top to bottom when stacked)
        # Reflecting actual Bitcoin transaction structure
        components_data = [
            {"label": "Version", "sublabel": "version: 2", "color": SYNTH_CYAN, "height": 0.6},
            {"label": "Input Count", "sublabel": "2 inputs", "color": SYNTH_CYAN, "height": 0.5},
            {"label": "Inputs", "sublabel": "2 signed UTXOs", "color": SYNTH_GREEN, "height": 1.3},
            {"label": "Output Count", "sublabel": "2 outputs", "color": SYNTH_CYAN, "height": 0.5},
            {"label": "Outputs", "sublabel": "0.7 BTC (Bob), 0.14 BTC (change)", "color": SYNTH_ORANGE, "height": 1.3},
            {"label": "Locktime", "sublabel": "0 (immediate)", "color": SYNTH_CYAN, "height": 0.6},
        ]

        # Build transaction by animating blocks rising from bottom
        transaction_blocks = VGroup()
        block_objects = []

        # Calculate total height to center the final structure
        total_height = sum(comp["height"] for comp in components_data) + 0.2 * (len(components_data) - 1)
        start_y = total_height / 2

        current_y = start_y

        for i, comp in enumerate(components_data):
            # Create block below screen
            block = self.create_transaction_block(
                comp["label"],
                comp["sublabel"],
                comp["color"],
                height=comp["height"]
            )

            # Position for final stacked structure
            final_y = current_y - comp["height"] / 2

            # Start position (below screen)
            block.move_to(DOWN * 5)

            # Add to scene and store
            transaction_blocks.add(block)
            block_objects.append({"block": block, "data": comp, "y": final_y})

            # Animate block rising from bottom
            self.play(
                block.animate.move_to(UP * final_y).rotate(0),
                rate_func=rate_functions.ease_out_bounce,
                run_time=0.8
            )

            # Play a subtle "snap" effect
            self.play(
                block.animate.scale(1.05),
                run_time=0.1
            )
            self.play(
                block.animate.scale(1/1.05),
                run_time=0.1
            )

            self.wait(0.2)

            # Update position for next block
            current_y -= (comp["height"] + 0.2)

        self.wait(0.5)

        # Add arrows and labels pointing to each block
        annotations = VGroup()
        for i, block_obj in enumerate(block_objects):
            block = block_obj["block"]
            comp = block_obj["data"]

            # Create detailed label
            label_group = self.create_component_label(
                comp["label"],
                comp["sublabel"],
                comp["color"]
            )
            label_group.next_to(block, RIGHT, buff=1.5)

            # Arrow from block to label
            arrow = Arrow(
                block.get_right(),
                label_group.get_left(),
                color=comp["color"],
                buff=0.1,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )

            annotations.add(VGroup(arrow, label_group))

            # Animate label appearing
            self.play(
                GrowArrow(arrow),
                FadeIn(label_group, shift=LEFT * 0.3),
                run_time=0.5
            )
            self.wait(0.2)

        self.wait(0.8)

        # Explain the fee calculation
        fee_text = Text(
            "Fee = Inputs (0.85 BTC) - Outputs (0.84 BTC) = 0.01 BTC",
            font_size=20,
            color=SYNTH_GOLD
        )
        fee_text.to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(fee_text))
        self.wait(1.2)

        # Highlight inputs block
        inputs_block = block_objects[2]["block"]  # Inputs is the 3rd block (index 2)
        self.play(
            inputs_block[0].animate.set_stroke(color=SYNTH_GOLD, width=3),
            run_time=0.5
        )
        self.wait(0.3)

        # Highlight outputs block
        outputs_block = block_objects[4]["block"]  # Outputs is the 5th block (index 4)
        self.play(
            inputs_block[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            outputs_block[0].animate.set_stroke(color=SYNTH_GOLD, width=3),
            run_time=0.5
        )
        self.wait(0.8)

        # Transaction ready
        ready_text = Text(
            "Transaction complete and ready to broadcast!",
            font_size=24,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        ready_text.move_to(fee_text)

        self.play(
            Transform(fee_text, ready_text),
            outputs_block[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            run_time=1
        )

        # Highlight entire transaction structure with glow
        for block_obj in block_objects:
            block = block_obj["block"]
            self.play(
                block[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
                run_time=0.3
            )

        # Final glow effect on all blocks
        self.play(
            *[block_obj["block"][0].animate.set_fill(opacity=0.3) for block_obj in block_objects],
            run_time=0.5
        )
        self.play(
            *[block_obj["block"][0].animate.set_fill(opacity=0.15) for block_obj in block_objects],
            run_time=0.5
        )

        self.wait(2)

    def create_transaction_block(self, label, sublabel, color, height=1.0):
        """Create a simple rectangular block for transaction components"""
        width = 3.5

        # Main rectangular block with rounded corners
        block_rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            color=color,
            stroke_width=3
        )
        block_rect.set_fill(color=color, opacity=0.15)

        # Label text inside block
        label_text = Text(label, font_size=28, color=color, weight=BOLD)
        sublabel_text = Text(sublabel, font_size=16, color=color)
        sublabel_text.set_opacity(0.8)

        text_group = VGroup(label_text, sublabel_text).arrange(DOWN, buff=0.1)
        text_group.move_to(block_rect)

        return VGroup(block_rect, text_group)

    def create_component_label(self, label, sublabel, color):
        """Create a label with sublabel for transaction components"""
        main = Text(label, font_size=22, color=color, weight=BOLD)
        sub = Text(sublabel, font_size=14, color=color)
        sub.set_opacity(0.7)

        group = VGroup(main, sub).arrange(DOWN, buff=0.1, aligned_edge=LEFT)

        # Background box
        box = SurroundingRectangle(
            group,
            color=color,
            stroke_width=1,
            buff=0.15,
            corner_radius=0.05
        )
        box.set_fill(color=color, opacity=0.1)

        return VGroup(box, group)
