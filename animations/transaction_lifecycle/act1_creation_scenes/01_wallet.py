"""
THE WALLET - Bitcoin Transaction Lifecycle
==========================================

Shows Alice's wallet with multiple UTXOs and UTXO selection.
Runtime: ~30 seconds
"""

from manim import *
import numpy as np
import sys
import os
# Add parent directories to path to import common module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common import *


class TheWallet(Scene):
    """
    The Wallet (0:00-0:30)
    Shows Alice's wallet with multiple UTXOs and UTXO selection.
    """

    def construct(self):
        # Set synthwave background
        self.camera.background_color = SYNTH_BG

        # Scene title
        scene_title = Text("The Wallet", font_size=38, color=SYNTH_CYAN)
        scene_title.to_edge(UP)
        self.play(Write(scene_title))
        self.wait(0.5)

        # Create synthwave grid background
        grid = self.create_synthwave_grid()
        self.play(Create(grid), run_time=1.5)

        # Create wallet label
        wallet_label = Text("Alice's Available Funds: 0.95 BTC across 3 UTXOs", font_size=24, color=SYNTH_PEACH)
        wallet_label.to_edge(UP).shift(DOWN * 0.8)
        self.play(FadeIn(wallet_label, shift=DOWN))

        # Create UTXOs as hexagonal shapes
        utxos_data = [
            {"amount": "0.5 BTC", "txid": "abc123...def456", "output": "#0", "pos": LEFT * 3 + UP * 1},
            {"amount": "0.35 BTC", "txid": "789ghi...jkl012", "output": "#1", "pos": ORIGIN + UP * 1},
            {"amount": "0.1 BTC", "txid": "mno345...pqr678", "output": "#2", "pos": RIGHT * 3 + UP * 1},
        ]

        utxos = VGroup()
        for data in utxos_data:
            utxo = self.create_utxo_hexagon(data)
            utxo.move_to(data["pos"])
            utxos.add(utxo)

        # Animate UTXOs appearing
        for utxo in utxos:
            self.play(
                FadeIn(utxo, scale=0.3),
                run_time=0.6
            )
            self.wait(0.2)

        self.wait(1)

        # Explanation text
        explain = Text(
            "Alice wants to send 0.7 BTC to Bob",
            font_size=24,
            color=SYNTH_GREEN
        )
        explain.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(explain))
        self.wait(1.5)

        # Show coin selection label
        coin_selection_label = Text(
            "Coin Selection",
            font_size=20,
            color=SYNTH_CYAN,
            weight=BOLD
        )
        coin_selection_label.to_edge(DOWN).shift(UP * 2.2)
        self.play(FadeIn(coin_selection_label, shift=UP * 0.2))
        self.wait(0.5)

        # Show UTXO selection
        selection_text = Text(
            "Wallet selects: 0.5 + 0.35 = 0.85 BTC",
            font_size=24,
            color=SYNTH_ORANGE
        )
        selection_text.move_to(explain)

        self.play(
            Transform(explain, selection_text),
            utxos[0].animate.set_stroke(color=SYNTH_ORANGE, width=2),
            utxos[1].animate.set_stroke(color=SYNTH_ORANGE, width=2),
            run_time=1.5
        )

        # Pulse effect on selected UTXOs
        for _ in range(2):
            self.play(
                utxos[0].animate.scale(1.1),
                utxos[1].animate.scale(1.1),
                run_time=0.4
            )
            self.play(
                utxos[0].animate.scale(1/1.1),
                utxos[1].animate.scale(1/1.1),
                run_time=0.4
            )

        self.wait(0.5)

        # Add change distribution note
        change_text = Text(
            "Bob will receive 0.7 BTC and Alice will receive 0.14 BTC as change (0.01 BTC fee)",
            font_size=22,
            color=SYNTH_GREEN
        )
        change_text.next_to(explain, DOWN, buff=0.3)

        self.play(
            FadeIn(change_text, shift=UP * 0.2),
            run_time=1
        )

        self.wait(2)

    def create_particles(self, center_pos, count):
        """Create small particle dots for flow animation"""
        particles = VGroup()
        for _ in range(count):
            dot = Dot(
                point=center_pos + np.array([
                    np.random.uniform(-0.3, 0.3),
                    np.random.uniform(-0.3, 0.3),
                    0
                ]),
                radius=0.05,
                color=SYNTH_CYAN
            )
            dot.set_fill(color=SYNTH_CYAN, opacity=0.8)
            particles.add(dot)
            self.add(dot)
        return particles

    def create_output_box(self, amount, label, color):
        """Create an output box with amount and label"""
        amount_text = Text(amount, font_size=20, color=color, weight=BOLD)
        label_text = Text(label, font_size=14, color=color)
        label_text.set_opacity(0.8)

        text_group = VGroup(amount_text, label_text).arrange(DOWN, buff=0.1)

        box = SurroundingRectangle(
            text_group,
            color=color,
            stroke_width=2,
            buff=0.2,
            corner_radius=0.1
        )
        box.set_fill(color=color, opacity=0.15)

        return VGroup(box, text_group)

    def create_utxo_hexagon(self, data):
        """Create a hexagonal UTXO with data labels"""
        hexagon = RegularPolygon(n=6, radius=1.1, color=SYNTH_GREEN, stroke_width=2)
        hexagon.set_fill(color=SYNTH_GREEN, opacity=0.1)

        amount = Text(data["amount"], font_size=24, color=SYNTH_GREEN, weight=BOLD)

        txid = Text(data["txid"], font_size=12, color=SYNTH_CYAN)
        output = Text(f"output {data['output']}", font_size=12, color=SYNTH_CYAN)

        details = VGroup(txid, output).arrange(DOWN, buff=0.05)
        details.scale(0.8)

        labels = VGroup(amount, details).arrange(DOWN, buff=0.15)
        labels.move_to(hexagon)

        return VGroup(hexagon, labels)

    def create_synthwave_grid(self):
        """Create a synthwave-style perspective grid background"""
        grid = VGroup()

        # Horizontal lines
        for i in range(-5, 2):
            y = i * 0.8
            scale = 1 + (i + 5) * 0.1
            line = Line(
                LEFT * 7 * scale + UP * y,
                RIGHT * 7 * scale + UP * y,
                stroke_width=1,
                color=SYNTH_PURPLE,
                stroke_opacity=0.3
            )
            grid.add(line)

        # Vertical lines
        for i in range(-6, 7):
            line = Line(
                UP * 1.5 + RIGHT * i,
                DOWN * 4 + RIGHT * i * 1.5,
                stroke_width=1,
                color=SYNTH_PURPLE,
                stroke_opacity=0.3
            )
            grid.add(line)

        grid.shift(DOWN * 2)
        return grid
