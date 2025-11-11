"""
ACT 3: THE MEMPOOL - Bitcoin Transaction Lifecycle
===================================================

Shows the transaction entering the mempool and waiting for mining.
Runtime: ~45 seconds
"""

from manim import *
import numpy as np
import sys
import os
# Add parent directory to path to import common module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from common import *


class MempoolWaiting(Scene):
    """
    The Mempool (0:00-0:45)
    Shows the transaction entering the mempool and waiting for mining.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
        title = Text("The Mempool", font_size=38, color=SYNTH_ORANGE)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create mempool container
        mempool_container = RoundedRectangle(
            width=6,
            height=5,
            corner_radius=0.3,
            color=SYNTH_ORANGE,
            stroke_width=3
        )
        mempool_container.set_fill(color=SYNTH_ORANGE, opacity=0.05)

        mempool_label = Text("Mempool", font_size=24, color=SYNTH_ORANGE)
        mempool_label.next_to(mempool_container, UP, buff=0.2)

        self.play(
            Create(mempool_container),
            Write(mempool_label)
        )
        self.wait(0.5)

        # Create multiple transactions with different fee rates
        transactions = [
            {"fee": 25, "size": "225 vB", "y": 1.8, "color": SYNTH_GREEN, "brightness": 1.0},
            {"fee": 20, "size": "190 vB", "y": 1.2, "color": SYNTH_GREEN, "brightness": 0.8},
            {"fee": 15, "size": "280 vB", "y": 0.6, "color": SYNTH_PEACH, "brightness": 0.6},
            {"fee": 10, "size": "250 vB", "y": 0, "color": SYNTH_PEACH, "brightness": 0.5},  # Alice's tx
            {"fee": 8, "size": "320 vB", "y": -0.6, "color": SYNTH_CYAN, "brightness": 0.4},
            {"fee": 5, "size": "210 vB", "y": -1.2, "color": SYNTH_CYAN, "brightness": 0.3},
            {"fee": 2, "size": "195 vB", "y": -1.8, "color": SYNTH_PURPLE, "brightness": 0.2},
        ]

        tx_objects = VGroup()
        for tx in transactions:
            # Hexagonal transaction
            hex_tx = RegularPolygon(n=6, radius=0.35, color=tx["color"], stroke_width=2)
            hex_tx.set_fill(color=tx["color"], opacity=0.1 + tx["brightness"] * 0.15)

            # Fee rate label
            fee_label = Text(f"{tx['fee']} sat/vB", font_size=12, color=tx["color"])
            fee_label.move_to(hex_tx)

            tx_group = VGroup(hex_tx, fee_label)
            tx_group.shift(UP * tx["y"])
            tx_objects.add(tx_group)

        tx_objects.move_to(mempool_container.get_center())

        # Animate transactions appearing
        for tx_obj in tx_objects:
            self.play(
                FadeIn(tx_obj, scale=0.5),
                run_time=0.2
            )

        self.wait(0.5)

        # Highlight Alice's transaction (4th one, 10 sat/vB)
        alice_tx = tx_objects[3]

        highlight_box = SurroundingRectangle(
            alice_tx,
            color=SYNTH_ORANGE,
            stroke_width=3,
            buff=0.15
        )

        alice_label = Text("Alice's TX", font_size=16, color=SYNTH_ORANGE, weight=BOLD)
        alice_label.next_to(alice_tx, RIGHT, buff=0.5)

        self.play(
            Create(highlight_box),
            Write(alice_label)
        )
        self.wait(0.3)

        # Show transaction stats
        stats = VGroup(
            Text("Fee Rate: 10 sat/vB", font_size=18, color=SYNTH_PEACH),
            Text("Size: 250 vB", font_size=18, color=SYNTH_PEACH),
            Text("Total Fee: 0.005 BTC", font_size=18, color=SYNTH_PEACH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        stats_box = SurroundingRectangle(
            stats,
            color=SYNTH_PEACH,
            stroke_width=2,
            buff=0.2,
            corner_radius=0.1
        )
        stats_box.set_fill(color=SYNTH_BG, opacity=0.9)

        stats_group = VGroup(stats_box, stats)
        stats_group.next_to(alice_label, RIGHT, buff=0.5)

        self.play(
            FadeIn(stats_group, shift=LEFT * 0.3),
            run_time=0.6
        )
        self.wait(1)

        # Explanation text
        explain = Text(
            "Waiting for block inclusion...",
            font_size=22,
            color=SYNTH_ORANGE
        )
        explain.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(explain))
        self.wait(1)

        # Show replication across network (small animation)
        network_text = Text(
            "Meanwhile, propagating to thousands of nodes",
            font_size=20,
            color=SYNTH_CYAN
        )
        network_text.move_to(explain)

        # Small network visualization in corner
        mini_network = VGroup()
        for i in range(8):
            angle = i * TAU / 8
            dot = Dot(
                radius=0.08,
                color=SYNTH_CYAN,
                point=np.array([np.cos(angle), np.sin(angle), 0.0]) * 0.8
            )
            mini_network.add(dot)

        mini_network.scale(0.6).to_corner(DR).shift(LEFT * 0.5 + UP * 1)

        self.play(
            Transform(explain, network_text),
            *[GrowFromCenter(dot) for dot in mini_network],
            run_time=0.8
        )

        # Pulse effect on mini network
        self.play(
            *[dot.animate.set_color(SYNTH_GREEN).scale(1.3) for dot in mini_network],
            run_time=0.4
        )
        self.play(
            *[dot.animate.scale(1/1.3) for dot in mini_network],
            run_time=0.4
        )

        self.wait(2)
