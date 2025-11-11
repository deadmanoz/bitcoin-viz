"""
ACT 4: MINING - Bitcoin Transaction Lifecycle
==============================================

Shows a miner assembling a block template and mining.
Runtime: ~1 minute
"""

from manim import *
import numpy as np
from common import *


class BlockTemplate(Scene):
    """
    Block Template Assembly (0:00-0:30)
    Shows a miner in Iceland assembling a block template.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
        title = Text("Block Template Assembly", font_size=38, color=SYNTH_GREEN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Miner node (larger, special)
        miner = RegularPolygon(n=6, radius=2, color=SYNTH_CYAN, stroke_width=4)
        miner.set_fill(color=SYNTH_CYAN, opacity=0.1)
        miner.shift(LEFT * 4)

        # Orange corona effect
        corona = RegularPolygon(n=6, radius=2.3, color=SYNTH_ORANGE, stroke_width=2, stroke_opacity=0.6)
        corona.move_to(miner)

        miner_label = Text("Miner (Iceland)", font_size=22, color=SYNTH_CYAN)
        miner_label.next_to(miner, DOWN, buff=0.4)

        self.play(
            Create(corona),
            DrawBorderThenFill(miner),
            Write(miner_label)
        )
        self.wait(0.5)

        # Block template container (empty initially)
        block_template = Rectangle(
            width=4,
            height=5,
            color=SYNTH_GREEN,
            stroke_width=3
        )
        block_template.set_fill(color=SYNTH_GREEN, opacity=0.05)
        block_template.shift(RIGHT * 3)

        block_label = Text("Block Template", font_size=20, color=SYNTH_GREEN)
        block_label.next_to(block_template, UP, buff=0.2)

        self.play(
            Create(block_template),
            Write(block_label)
        )
        self.wait(0.5)

        # Show transactions flying from mempool to block
        explain = Text(
            "Selecting highest fee transactions...",
            font_size=22,
            color=SYNTH_GREEN
        )
        explain.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(explain))

        # Create small transaction hexagons
        tx_positions = [
            UP * 1.8,
            UP * 1.2,
            UP * 0.6,
            UP * 0,
            DOWN * 0.6,
            DOWN * 1.2,
        ]

        transactions = VGroup()
        for pos in tx_positions:
            tx = RegularPolygon(n=6, radius=0.25, color=SYNTH_PEACH, stroke_width=2)
            tx.set_fill(color=SYNTH_PEACH, opacity=0.2)
            tx.move_to(miner.get_center() + LEFT * 3 + pos)
            transactions.add(tx)

        # Animate transactions appearing and flying into block
        for i, tx in enumerate(transactions):
            self.play(FadeIn(tx, scale=0.3), run_time=0.15)

        self.wait(0.3)

        # Move transactions to block template
        for i, tx in enumerate(transactions):
            target = block_template.get_center() + tx_positions[i] * 0.6
            self.play(
                tx.animate.move_to(target).set_color(SYNTH_GREEN),
                run_time=0.3
            )

        self.wait(0.5)

        # Add coinbase transaction (special, gold)
        coinbase_text = Text(
            "Coinbase Transaction",
            font_size=18,
            color=SYNTH_GOLD,
            weight=BOLD
        )
        coinbase_text.move_to(explain)

        coinbase = RegularPolygon(n=6, radius=0.35, color=SYNTH_GOLD, stroke_width=3)
        coinbase.set_fill(color=SYNTH_GOLD, opacity=0.3)
        coinbase.move_to(block_template.get_top() + DOWN * 0.5)

        self.play(
            Transform(explain, coinbase_text),
            FadeIn(coinbase, scale=0.3, shift=DOWN * 0.5),
            run_time=0.8
        )
        self.wait(0.5)

        # Show reward text
        reward = Text(
            "6.25 BTC + fees",
            font_size=14,
            color=SYNTH_GOLD
        )
        reward.move_to(coinbase)

        self.play(Write(reward))
        self.wait(1)

        # Block filled indicator
        filled_text = Text(
            "Block nearly full: ~3.9M weight units",
            font_size=20,
            color=SYNTH_GREEN
        )
        filled_text.move_to(explain)

        self.play(Transform(explain, filled_text))

        # Fill indicator
        self.play(
            block_template.animate.set_fill(opacity=0.15),
            run_time=0.8
        )

        self.wait(2)


class Mining(Scene):
    """
    Mining Process (0:30-1:00)
    Shows the mining process with hash attempts.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
        title = Text("Mining", font_size=38, color=SYNTH_PURPLE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Block header structure
        header_data = [
            ("Previous Block Hash", "000000000000..."),
            ("Merkle Root", "a1b2c3d4..."),
            ("Timestamp", "2025-11-11 14:23:07"),
            ("Nonce", "???"),
        ]

        header_display = VGroup()
        for label, value in header_data:
            label_text = Text(label + ":", font_size=18, color=SYNTH_CYAN)
            value_text = Text(value, font_size=18, color=SYNTH_GREEN)

            row = VGroup(label_text, value_text).arrange(RIGHT, buff=0.3)
            header_display.add(row)

        header_display.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        header_display.to_edge(LEFT).shift(RIGHT * 0.5)

        for row in header_display:
            self.play(FadeIn(row, shift=RIGHT * 0.3), run_time=0.3)

        self.wait(0.5)

        # Mining explanation
        mining_text = Text(
            "Trying trillions of hash combinations...",
            font_size=22,
            color=SYNTH_PURPLE
        )
        mining_text.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(mining_text))

        # Hash attempt visualization - rapid lightning flashes
        hash_area = Rectangle(
            width=5,
            height=4,
            color=SYNTH_PURPLE,
            stroke_width=2
        )
        hash_area.shift(RIGHT * 2.5)

        self.play(Create(hash_area))

        # Rapid hash attempts (purple lightning)
        # Pre-computed deterministic positions for reliable rendering
        bolt_configs = [
            [(0.5, 0.3), (-0.4, -0.5)],
            [(-0.3, 0.6), (0.6, -0.2)],
            [(0.2, -0.4), (-0.5, 0.4)],
        ]

        for cycle in range(20):
            # Deterministic lightning bolts
            bolts = VGroup()
            config_idx = cycle % len(bolt_configs)
            for i in range(3):
                offset = (cycle + i) % len(bolt_configs)
                start_offset, end_offset = bolt_configs[(config_idx + i) % len(bolt_configs)]

                start = hash_area.get_center() + np.array([start_offset[0], start_offset[1], 0.0])
                end = hash_area.get_center() + np.array([end_offset[0], end_offset[1], 0.0])

                bolt = Line(start, end, color=SYNTH_PURPLE, stroke_width=2)
                bolts.add(bolt)

            self.play(
                *[Create(bolt) for bolt in bolts],
                run_time=0.05
            )
            self.play(
                *[FadeOut(bolt) for bolt in bolts],
                run_time=0.05
            )

        # Update nonce display rapidly
        nonce_row = header_display[3][1]  # The nonce value
        for nonce in [12847, 847291, 2847183647]:
            new_nonce = Text(str(nonce), font_size=18, color=SYNTH_GREEN)
            new_nonce.move_to(nonce_row)
            self.play(Transform(nonce_row, new_nonce), run_time=0.3)

        self.wait(0.3)

        # SUCCESS! - massive green explosion
        success_text = Text(
            "Block Found!",
            font_size=48,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        success_text.move_to(ORIGIN)

        # Particle explosion (deterministic pattern)
        particles = VGroup()
        for i in range(30):
            particle = Dot(
                radius=0.1,
                color=SYNTH_GREEN,
                point=ORIGIN
            )
            particles.add(particle)

        explosion_anims = []
        for i, particle in enumerate(particles):
            angle = i * TAU / 30
            # Vary distance based on position for visual interest
            distance = 2.5 + (i % 3) * 0.5
            target = np.array([np.cos(angle) * distance, np.sin(angle) * distance, 0.0])
            explosion_anims.append(
                particle.animate.move_to(target).set_opacity(0)
            )

        self.play(
            FadeIn(success_text, scale=0.5),
            *[FadeIn(p, scale=0.5) for p in particles],
            run_time=0.3
        )
        self.play(
            *explosion_anims,
            run_time=1.5
        )

        # Block number
        block_num = Text(
            "Block 870,000",
            font_size=32,
            color=SYNTH_GREEN
        )
        block_num.next_to(success_text, DOWN, buff=0.4)

        self.play(Write(block_num))

        self.wait(2)
