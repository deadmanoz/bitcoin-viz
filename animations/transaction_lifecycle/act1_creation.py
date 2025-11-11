"""
ACT 1: CREATION - Bitcoin Transaction Lifecycle
================================================

Shows wallet UTXO selection and transaction construction.
Runtime: ~1 minute
"""

from manim import *
import numpy as np
import sys
sys.path.append("..")
from common import *


class TheWallet(Scene):
    """
    The Wallet (0:00-0:30)
    Shows Alice's wallet with multiple UTXOs and UTXO selection.
    """

    def construct(self):
        # Set synthwave background
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
        scene_title = Text("The Wallet", font_size=38, color=SYNTH_CYAN)
        scene_title.to_edge(UP)
        self.play(Write(scene_title))
        self.wait(0.5)

        # Create synthwave grid background
        grid = self.create_synthwave_grid()
        self.play(Create(grid), run_time=1.5)

        # Create wallet label
        wallet_label = Text("Alice's Wallet", font_size=28, color=SYNTH_PEACH)
        wallet_label.to_edge(UP).shift(DOWN * 0.8)
        self.play(FadeIn(wallet_label, shift=DOWN))

        # Create UTXOs as hexagonal shapes (larger radius for more space)
        utxos_data = [
            {"amount": "0.5 BTC", "txid": "abc123...def456", "output": "#0", "pos": LEFT * 3 + UP * 1},
            {"amount": "0.35 BTC", "txid": "789ghi...jkl012", "output": "#1", "pos": ORIGIN + UP * 1},
            {"amount": "0.15 BTC", "txid": "mno345...pqr678", "output": "#2", "pos": RIGHT * 3 + UP * 1},
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

        # Show UTXO selection - highlight selected ones
        selection_text = Text(
            "Wallet selects: 0.5 + 0.35 = 0.85 BTC",
            font_size=24,
            color=SYNTH_ORANGE
        )
        selection_text.move_to(explain)

        self.play(
            Transform(explain, selection_text),
            utxos[0].animate.set_stroke(color=SYNTH_ORANGE, width=4),
            utxos[1].animate.set_stroke(color=SYNTH_ORANGE, width=4),
            utxos[0][0].animate.set_fill(color=SYNTH_ORANGE, opacity=0.3),
            utxos[1][0].animate.set_fill(color=SYNTH_ORANGE, opacity=0.3),
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

        self.wait(1)

        # Fade unselected UTXO
        self.play(
            utxos[2].animate.set_opacity(0.3),
            run_time=0.8
        )

        self.wait(2)

    def create_utxo_hexagon(self, data):
        """Create a hexagonal UTXO with data labels (larger size)"""
        # Hexagon shape (increased radius from 0.8 to 1.1 for more space)
        hexagon = RegularPolygon(n=6, radius=1.1, color=SYNTH_GREEN, stroke_width=2)
        hexagon.set_fill(color=SYNTH_GREEN, opacity=0.1)

        # Amount label (large, centered)
        amount = Text(data["amount"], font_size=24, color=SYNTH_GREEN, weight=BOLD)

        # Transaction details (smaller, below)
        txid = Text(data["txid"], font_size=12, color=SYNTH_CYAN)
        output = Text(f"output {data['output']}", font_size=12, color=SYNTH_CYAN)

        details = VGroup(txid, output).arrange(DOWN, buff=0.05)
        details.scale(0.8)

        # Arrange everything
        labels = VGroup(amount, details).arrange(DOWN, buff=0.15)
        labels.move_to(hexagon)

        return VGroup(hexagon, labels)

    def create_synthwave_grid(self):
        """Create a synthwave-style perspective grid background"""
        grid = VGroup()

        # Horizontal lines (perspective)
        for i in range(-5, 2):
            y = i * 0.8
            scale = 1 + (i + 5) * 0.1  # Perspective effect
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


class TransactionConstruction(Scene):
    """
    Transaction Construction (0:30-1:00)
    Shows the transaction being built as a data packet.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
        title = Text("Transaction Construction", font_size=38, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create central transaction packet - crystalline hexagonal structure
        packet_center = self.create_transaction_packet()
        packet_center.scale(0.3)

        self.play(
            FadeIn(packet_center, scale=0.1),
            run_time=1.5
        )

        # Pulse and grow
        self.play(
            packet_center.animate.scale(2.5),
            run_time=1
        )

        self.wait(0.5)

        # Show packet components appearing in layers
        # Inputs: 0.5 + 0.35 = 0.85 BTC
        # Outputs: 0.7 to Bob + 0.1 change to Alice = 0.8 BTC
        # Fee: 0.85 - 0.8 = 0.05 BTC
        components = [
            {"label": "Header", "sublabel": "version, locktime", "color": SYNTH_CYAN, "pos": UP * 2.5},
            {"label": "Inputs", "sublabel": "0.5 + 0.35 BTC UTXOs", "color": SYNTH_GREEN, "pos": UP * 1},
            {"label": "Outputs", "sublabel": "0.7 → Bob, 0.1 → Alice", "color": SYNTH_ORANGE, "pos": DOWN * 0.5},
            {"label": "Fee", "sublabel": "0.05 BTC to miners", "color": SYNTH_PEACH, "pos": DOWN * 2},
        ]

        component_labels = VGroup()
        for comp in components:
            label_group = self.create_component_label(
                comp["label"],
                comp["sublabel"],
                comp["color"]
            )
            label_group.next_to(packet_center, RIGHT, buff=1.5).shift(comp["pos"] - UP * 0.5)

            # Arrow from packet to label
            arrow = Arrow(
                packet_center.get_right(),
                label_group.get_left(),
                color=comp["color"],
                buff=0.1,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.1
            )

            component_labels.add(VGroup(arrow, label_group))

        # Animate each component appearing
        for comp_group in component_labels:
            self.play(
                GrowArrow(comp_group[0]),
                FadeIn(comp_group[1], shift=LEFT * 0.3),
                run_time=0.7
            )
            self.wait(0.3)

        self.wait(1)

        # Highlight scriptPubKey (locking script)
        script_text = Text(
            "scriptPubKey: Locking scripts on outputs",
            font_size=20,
            color=SYNTH_ORANGE
        )
        script_text.to_edge(DOWN).shift(UP * 0.5)

        # Create circuit pattern effect
        circuit = self.create_circuit_pattern()
        circuit.scale(0.4).next_to(packet_center, DOWN, buff=0.3)

        self.play(Write(script_text))
        self.play(Create(circuit), run_time=1.5)
        self.wait(1)

        # Signature generation effect
        sig_text = Text(
            "scriptSig: Alice's signatures unlock inputs",
            font_size=20,
            color=SYNTH_PURPLE
        )
        sig_text.move_to(script_text)

        # Lightning effect for signature
        lightning = self.create_signature_lightning()
        lightning.move_to(packet_center)

        self.play(
            Transform(script_text, sig_text),
            FadeOut(circuit)
        )
        self.play(Create(lightning), run_time=0.8)
        self.wait(0.5)

        # Transaction ready (changed from "sealed")
        ready_text = Text(
            "Transaction signed and ready to broadcast",
            font_size=24,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        ready_text.move_to(script_text)

        self.play(
            Transform(script_text, ready_text),
            FadeOut(lightning),
            packet_center.animate.set_stroke(color=SYNTH_GREEN, width=4),
            run_time=1
        )

        # Intense glow effect
        self.play(
            packet_center.animate.set_fill(opacity=0.4),
            run_time=0.5
        )
        self.play(
            packet_center.animate.set_fill(opacity=0.2),
            run_time=0.5
        )

        self.wait(2)

    def create_transaction_packet(self):
        """Create a crystalline hexagonal packet structure"""
        # Central hexagon
        center = RegularPolygon(n=6, radius=1, color=SYNTH_GREEN, stroke_width=3)
        center.set_fill(color=SYNTH_GREEN, opacity=0.15)

        # Surrounding hexagons
        surrounding = VGroup()
        for i in range(6):
            angle = i * PI / 3
            hex = RegularPolygon(n=6, radius=0.5, color=SYNTH_CYAN, stroke_width=2)
            hex.set_fill(color=SYNTH_CYAN, opacity=0.1)
            hex.move_to(center.get_center() + np.array([np.cos(angle), np.sin(angle), 0]) * 1.2)
            surrounding.add(hex)

        # Connection lines
        connections = VGroup()
        for hex in surrounding:
            line = Line(
                center.get_center(),
                hex.get_center(),
                color=SYNTH_GREEN,
                stroke_width=1,
                stroke_opacity=0.5
            )
            connections.add(line)

        return VGroup(connections, center, surrounding)

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

    def create_circuit_pattern(self):
        """Create a circuit-like pattern for scriptPubKey visualization"""
        circuit = VGroup()

        # Create some circuit-like paths
        for i in range(3):
            path = VMobject(color=SYNTH_ORANGE, stroke_width=2)
            path.set_points_as_corners([
                LEFT * 2 + UP * (i - 1) * 0.3,
                LEFT * 1 + UP * (i - 1) * 0.3,
                LEFT * 1 + UP * ((i - 1) * 0.3 + 0.2),
                RIGHT * 1 + UP * ((i - 1) * 0.3 + 0.2),
                RIGHT * 1 + UP * (i - 1) * 0.3,
                RIGHT * 2 + UP * (i - 1) * 0.3,
            ])
            circuit.add(path)

            # Add small circles at corners
            for j in [1, 2, 3, 4]:
                dot = Dot(path.get_points()[j], radius=0.05, color=SYNTH_ORANGE)
                circuit.add(dot)

        return circuit

    def create_signature_lightning(self):
        """Create lightning effect for signature visualization"""
        lightning = VGroup()

        # Create jagged lightning paths (simple lines for reliability)
        for i in range(3):
            angle = i * TAU / 3

            # Create a jagged line from center outward
            points = [
                ORIGIN,
                np.array([np.cos(angle) * 0.4, np.sin(angle) * 0.4, 0]),
                np.array([np.cos(angle) * 0.7 + 0.1, np.sin(angle) * 0.7 - 0.1, 0]),
                np.array([np.cos(angle) * 1.0, np.sin(angle) * 1.0, 0]),
            ]

            bolt = VMobject(color=SYNTH_PURPLE, stroke_width=3)
            bolt.set_points_as_corners(points)
            bolt.set_stroke(opacity=0.8)
            lightning.add(bolt)

        return lightning
