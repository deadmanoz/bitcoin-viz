"""
ACT 5: CONFIRMATION - Bitcoin Transaction Lifecycle
====================================================

Shows block propagation through the network and chain extension.
Runtime: ~1 minute
"""

from manim import *
import numpy as np
import sys
sys.path.append("..")
from common import *


class BlockPropagation(Scene):
    """
    Block Relay (0:00-0:30)
    Shows the block propagating through the network.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
        title = Text("Block Propagation", font_size=38, color=SYNTH_GREEN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Block as a large cube
        block_cube = Cube(
            side_length=1.5,
            fill_color=SYNTH_GREEN,
            fill_opacity=0.2,
            stroke_color=SYNTH_GREEN,
            stroke_width=3
        )
        block_cube.rotate(PI/6, axis=UP).rotate(PI/6, axis=RIGHT)
        block_cube.shift(LEFT * 4)

        block_label = Text("Block 870,000", font_size=20, color=SYNTH_GREEN, weight=BOLD)
        block_label.next_to(block_cube, DOWN, buff=0.5)

        self.play(
            FadeIn(block_cube, scale=0.3),
            Write(block_label)
        )

        # Rotate block slightly for effect
        self.play(
            Rotate(block_cube, angle=PI/4, axis=UP),
            run_time=1
        )

        self.wait(0.5)

        # Network nodes
        network_nodes = VGroup()
        for i in range(12):
            angle = i * TAU / 12
            node = Dot(
                radius=0.15,
                color=SYNTH_CYAN,
                point=np.array([np.cos(angle) * 3, np.sin(angle) * 2, 0.0]) + RIGHT * 2
            )
            network_nodes.add(node)

        self.play(
            *[GrowFromCenter(node) for node in network_nodes],
            run_time=0.8
        )

        # Block propagates (compact block announcements)
        explain = Text(
            "Optimized block relay (compact blocks)",
            font_size=20,
            color=SYNTH_ORANGE
        )
        explain.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(explain))

        # Send block to all nodes (waves)
        for wave in range(3):
            wave_nodes = network_nodes[wave*4:(wave+1)*4]

            # Compact messages
            messages = VGroup()
            for node in wave_nodes:
                msg = RegularPolygon(n=6, radius=0.12, color=SYNTH_ORANGE, stroke_width=2)
                msg.move_to(block_cube.get_center())
                messages.add(msg)

            # Animate messages traveling
            self.play(
                *[FadeIn(msg, scale=0.5) for msg in messages],
                run_time=0.2
            )

            travel_anims = []
            for msg, node in zip(messages, wave_nodes):
                travel_anims.append(msg.animate.move_to(node.get_center()))

            self.play(*travel_anims, run_time=0.5)

            # Nodes turn green (validated)
            self.play(
                *[node.animate.set_color(SYNTH_GREEN).scale(1.2) for node in wave_nodes],
                *[FadeOut(msg) for msg in messages],
                run_time=0.3
            )

            self.wait(0.2)

        # Node Charlie validates
        charlie_text = Text(
            "Node Charlie validates block",
            font_size=20,
            color=SYNTH_GREEN
        )
        charlie_text.move_to(explain)

        self.play(Transform(explain, charlie_text))

        # Validation checklist (quick version)
        checks = [
            "✓ Valid proof-of-work",
            "✓ Valid previous hash",
            "✓ All transactions valid",
            "✓ Block size limits met",
            "✓ Coinbase correct",
        ]

        checklist = VGroup()
        for check in checks:
            item = Text(check, font_size=14, color=SYNTH_GREEN)
            checklist.add(item)

        checklist.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        checklist.to_edge(RIGHT).shift(LEFT * 0.5)

        for item in checklist:
            self.play(FadeIn(item, shift=LEFT * 0.2), run_time=0.15)

        self.wait(1.5)


class ChainExtension(Scene):
    """
    Chain Extension (0:30-1:00)
    Shows the block being added to the chain and confirmations accumulating.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
        title = Text("Chain Extension", font_size=38, color=SYNTH_GREEN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create blockchain perspective view
        # Show blocks extending into the distance
        blocks = VGroup()
        for i in range(7):
            z_scale = 0.8 ** i  # Perspective scaling
            opacity = 1 - i * 0.12

            block = Cube(
                side_length=1 * z_scale,
                fill_color=SYNTH_CYAN if i < 6 else SYNTH_GREEN,
                fill_opacity=0.15 * opacity,
                stroke_color=SYNTH_CYAN if i < 6 else SYNTH_GREEN,
                stroke_width=2
            )

            # Position with perspective
            x_pos = -3 + i * 1.2 * z_scale
            y_pos = -0.5 - i * 0.15
            block.move_to(np.array([x_pos, y_pos, 0.0]))

            # Rotate for 3D effect
            block.rotate(PI/6, axis=UP).rotate(PI/8, axis=RIGHT)

            # Block number
            block_num = Text(
                f"{869994 + i}",
                font_size=int(12 * z_scale),
                color=SYNTH_CYAN if i < 6 else SYNTH_GREEN
            )
            block_num.next_to(block, DOWN, buff=0.1 * z_scale)

            blocks.add(VGroup(block, block_num))

        # Draw existing chain
        for i, block_group in enumerate(blocks[:-1]):
            self.play(
                FadeIn(block_group, shift=RIGHT * 0.3),
                run_time=0.2
            )

        self.wait(0.5)

        # New block (870000) appears
        new_block = blocks[-1]

        explain = Text(
            "Block 870,000 extends the chain",
            font_size=22,
            color=SYNTH_GREEN
        )
        explain.to_edge(DOWN).shift(UP * 0.5)

        self.play(
            Write(explain),
            FadeIn(new_block, scale=0.5, shift=LEFT * 0.5),
            run_time=1
        )

        # Highlight Alice's transaction
        tx_indicator = Text(
            "← Alice's TX",
            font_size=16,
            color=SYNTH_ORANGE
        )
        tx_indicator.next_to(new_block, RIGHT, buff=0.3)

        self.play(
            Write(tx_indicator),
            new_block[0].animate.set_fill(opacity=0.3),
            run_time=0.6
        )

        self.wait(1)

        # Show confirmations accumulating
        conf_text = Text(
            "1 confirmation",
            font_size=24,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        conf_text.move_to(explain)

        self.play(Transform(explain, conf_text))
        self.wait(0.5)

        # Add more blocks on top
        additional_blocks = []
        for i in range(5):
            block_num = 870001 + i
            z_scale = 0.8 ** 7

            block = Cube(
                side_length=1 * z_scale,
                fill_color=SYNTH_CYAN,
                fill_opacity=0.08,
                stroke_color=SYNTH_CYAN,
                stroke_width=2
            )

            x_pos = -3 + 7 * 1.2 * z_scale + (i + 1) * 1.2 * z_scale
            y_pos = -0.5 - 7 * 0.15 - (i + 1) * 0.15
            block.move_to(np.array([x_pos, y_pos, 0.0]))
            block.rotate(PI/6, axis=UP).rotate(PI/8, axis=RIGHT)

            num = Text(
                str(block_num),
                font_size=int(10 * z_scale),
                color=SYNTH_CYAN
            )
            num.next_to(block, DOWN, buff=0.1 * z_scale)

            additional_blocks.append(VGroup(block, num))

        # Animate new blocks appearing
        for i, block_group in enumerate(additional_blocks):
            self.play(
                FadeIn(block_group, shift=LEFT * 0.3),
                run_time=0.3
            )

            # Update confirmation count
            new_conf = Text(
                f"{i + 2} confirmations",
                font_size=24,
                color=SYNTH_GREEN,
                weight=BOLD
            )
            new_conf.move_to(explain)

            self.play(
                Transform(explain, new_conf),
                new_block[0].animate.set_fill(opacity=0.25 + i * 0.03),
                run_time=0.2
            )

            self.wait(0.2)

        # 6 confirmations reached
        final_text = Text(
            "6 confirmations - Transaction final!",
            font_size=26,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        final_text.move_to(explain)

        self.play(
            Transform(explain, final_text),
            new_block[0].animate.set_stroke(width=4),
            run_time=0.8
        )

        self.wait(1)

        # Zoom out - show full journey
        journey_text = Text(
            "Journey complete: Wallet → Network → Mempool → Mining → Blockchain",
            font_size=18,
            color=SYNTH_CYAN
        )
        journey_text.to_edge(UP).shift(DOWN * 0.8)

        self.play(
            FadeOut(title),
            Write(journey_text)
        )

        self.wait(2)

        # Final fade
        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
