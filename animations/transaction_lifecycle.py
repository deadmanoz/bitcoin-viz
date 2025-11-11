"""
Bitcoin Transaction Lifecycle - Synthwave/Cyberpunk Style
==========================================================

A 5-minute visual journey through a Bitcoin transaction's lifecycle,
from creation in a wallet to confirmation in the blockchain.

Visual Theme: Synthwave/Cyberpunk - Neon colors on dark backgrounds
Runtime: ~5 minutes

Color Palette:
- Background: #000221 (dark blue)
- Packet/Data: #20E516 (neon green)
- Nodes: #00A0D0 (cyan)
- Validation/Success: #FF6C11 (neon orange)
- Signatures/Crypto: #261447 (purple)
- Accents: #FF8664 (peach)
"""

from manim import *
import numpy as np

# Synthwave Color Palette
SYNTH_BG = "#000221"
SYNTH_GREEN = "#20E516"
SYNTH_CYAN = "#00A0D0"
SYNTH_ORANGE = "#FF6C11"
SYNTH_PURPLE = "#261447"
SYNTH_PEACH = "#FF8664"


class Act1_TheWallet(Scene):
    """
    ACT 1: CREATION - The Wallet (0:00-0:30)
    Shows Alice's wallet with multiple UTXOs and UTXO selection.
    """

    def construct(self):
        # Set synthwave background
        self.camera.background_color = SYNTH_BG

        # Title sequence
        title = Text("Bitcoin Transaction Lifecycle", font_size=52, color=SYNTH_GREEN)
        subtitle = Text(
            "Act 1: Creation",
            font_size=32,
            color=SYNTH_CYAN,
            weight=BOLD
        )
        subtitle.next_to(title, DOWN, buff=0.3)

        self.play(
            Write(title, run_time=1.5),
            FadeIn(subtitle, shift=UP, run_time=1)
        )
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # Scene title
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

        # Create UTXOs as hexagonal shapes
        utxos_data = [
            {"amount": "0.5 BTC", "txid": "abc123...def456", "output": "#0", "pos": LEFT * 3 + UP * 1},
            {"amount": "0.3 BTC", "txid": "789ghi...jkl012", "output": "#1", "pos": ORIGIN + UP * 1},
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
            "Wallet selects: 0.5 + 0.3 = 0.8 BTC",
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
        """Create a hexagonal UTXO with data labels"""
        # Hexagon shape
        hexagon = RegularPolygon(n=6, radius=0.8, color=SYNTH_GREEN, stroke_width=2)
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


class Act1_TransactionConstruction(Scene):
    """
    ACT 1: CREATION - Transaction Construction (0:30-1:00)
    Shows the transaction being built as a data packet.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
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
        components = [
            {"label": "Header", "sublabel": "version, locktime", "color": SYNTH_CYAN, "pos": UP * 2.5},
            {"label": "Inputs", "sublabel": "0.5 + 0.3 BTC UTXOs", "color": SYNTH_GREEN, "pos": UP * 1},
            {"label": "Outputs", "sublabel": "0.7 → Bob, 0.095 → change", "color": SYNTH_ORANGE, "pos": DOWN * 0.5},
            {"label": "Fee", "sublabel": "0.005 BTC to miners", "color": SYNTH_PEACH, "pos": DOWN * 2},
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

        # Packet sealed and ready
        seal_text = Text(
            "Transaction sealed and ready to broadcast",
            font_size=24,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        seal_text.move_to(script_text)

        self.play(
            Transform(script_text, seal_text),
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

        # Create jagged lightning paths
        for i in range(3):
            angle = i * TAU / 3
            points = [ORIGIN]
            current = np.array([0, 0, 0])

            for _ in range(5):
                current += np.array([
                    np.cos(angle) * 0.3 + np.random.uniform(-0.1, 0.1),
                    np.sin(angle) * 0.3 + np.random.uniform(-0.1, 0.1),
                    0
                ])
                points.append(current.copy())

            bolt = VMobject(color=SYNTH_PURPLE, stroke_width=3)
            bolt.set_points_as_corners(points)
            bolt.set_stroke(opacity=0.8)
            lightning.add(bolt)

        return lightning


class Act2_InitialBroadcast(Scene):
    """
    ACT 2: PROPAGATION - Initial Broadcast (1:00-1:20)
    Shows the transaction broadcasting through the P2P network.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
        title = Text("Network Propagation", font_size=38, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Create network graph
        network = self.create_network_graph()
        self.play(Create(network), run_time=2)
        self.wait(0.5)

        # Highlight Alice's node
        alice_node = network[0][0]  # First node
        alice_label = Text("Alice's Node", font_size=18, color=SYNTH_PEACH)
        alice_label.next_to(alice_node, DOWN, buff=0.3)

        self.play(
            alice_node.animate.set_color(SYNTH_PEACH).scale(1.3),
            Write(alice_label)
        )
        self.wait(0.5)

        # Create transaction packet
        tx_packet = Dot(color=SYNTH_GREEN, radius=0.15)
        tx_packet.move_to(alice_node)

        self.play(FadeIn(tx_packet, scale=0.3))
        self.wait(0.3)

        # Broadcast explanation
        broadcast_text = Text(
            "Broadcasting to connected peers...",
            font_size=22,
            color=SYNTH_GREEN
        )
        broadcast_text.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(broadcast_text))

        # Animate packet propagating through network
        # Create multiple packet copies that travel to different nodes
        visited_nodes = {alice_node}
        packets_to_animate = [(tx_packet, alice_node, network[0][:4])]  # Start from Alice to first 4 nodes

        for wave in range(3):  # 3 waves of propagation
            animations = []
            new_packets = []

            for packet, source, targets in packets_to_animate:
                for target in targets:
                    if target not in visited_nodes:
                        # Create new packet
                        new_packet = Dot(color=SYNTH_GREEN, radius=0.12)
                        new_packet.move_to(source)

                        # Create pulse trail
                        trail = Line(source.get_center(), target.get_center(), color=SYNTH_GREEN, stroke_width=2)
                        trail.set_opacity(0.5)

                        animations.append(FadeIn(new_packet, scale=0.5))
                        animations.append(Create(trail, run_time=0.5))
                        animations.append(new_packet.animate.move_to(target))
                        animations.append(FadeOut(trail))

                        visited_nodes.add(target)
                        new_packets.append(new_packet)

            if animations:
                self.play(*animations, run_time=0.8)
                self.wait(0.2)

            # Prepare next wave
            packets_to_animate = []

        # Network-wide acceptance
        self.play(
            *[node.animate.set_color(SYNTH_GREEN).scale(1.1) for node in network[0] if node in visited_nodes],
            run_time=1
        )

        success_text = Text(
            "Propagated to thousands of nodes worldwide",
            font_size=22,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        success_text.move_to(broadcast_text)

        self.play(Transform(broadcast_text, success_text))
        self.wait(2)

    def create_network_graph(self):
        """Create a 3D-looking network graph of nodes"""
        nodes = VGroup()
        connections = VGroup()

        # Create nodes in a semi-random but structured layout
        node_positions = []
        for i in range(15):
            # Arrange in rough layers
            layer = i // 5
            pos_in_layer = i % 5

            x = (pos_in_layer - 2) * 2 + np.random.uniform(-0.3, 0.3)
            y = 1 - layer * 1.5 + np.random.uniform(-0.2, 0.2)

            node_positions.append(np.array([x, y, 0]))

        # Create nodes
        for pos in node_positions:
            node = Dot(pos, radius=0.15, color=SYNTH_CYAN)
            node.set_sheen(-0.3, UP)  # Add 3D-like sheen
            nodes.add(node)

        # Create connections (not all nodes connected to all)
        for i, pos1 in enumerate(node_positions):
            for j, pos2 in enumerate(node_positions[i+1:], start=i+1):
                distance = np.linalg.norm(pos1 - pos2)
                # Only connect nearby nodes
                if distance < 2.5 and np.random.random() > 0.3:
                    line = Line(pos1, pos2, color=SYNTH_PURPLE, stroke_width=1.5, stroke_opacity=0.4)
                    connections.add(line)

        return VGroup(nodes, connections)


# Quick intro scene combining key moments
class TransactionLifecycleIntro(Scene):
    """
    Quick intro showing the full lifecycle in under 60 seconds.
    Perfect for preview/teaser.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Main title
        title = Text("Bitcoin Transaction", font_size=56, color=SYNTH_GREEN, weight=BOLD)
        subtitle = Text("From Creation to Confirmation", font_size=32, color=SYNTH_CYAN)
        subtitle.next_to(title, DOWN)

        title_group = VGroup(title, subtitle)

        self.play(
            Write(title, run_time=1.5),
            FadeIn(subtitle, shift=UP, run_time=1)
        )
        self.wait(1.5)

        self.play(title_group.animate.scale(0.4).to_corner(UL))

        # Quick montage of key visuals
        stages = [
            ("Wallet", SYNTH_GREEN, "UTXOs selected"),
            ("Signed", SYNTH_PURPLE, "Cryptographic proof"),
            ("Broadcast", SYNTH_CYAN, "P2P propagation"),
            ("Validated", SYNTH_ORANGE, "Node verification"),
            ("Mempool", SYNTH_PEACH, "Awaiting mining"),
            ("Mined", SYNTH_GREEN, "Block inclusion"),
            ("Confirmed", SYNTH_GREEN, "Immutable"),
        ]

        stage_dots = VGroup()
        for i, (stage, color, desc) in enumerate(stages):
            dot = Dot(radius=0.3, color=color)
            label = Text(stage, font_size=18, color=color)
            label.next_to(dot, DOWN, buff=0.2)

            stage_group = VGroup(dot, label)
            stage_dots.add(stage_group)

        # Arrange in a horizontal line
        stage_dots.arrange(RIGHT, buff=0.8)
        stage_dots.move_to(ORIGIN)

        # Animate each stage
        for i, stage_group in enumerate(stage_dots):
            self.play(
                FadeIn(stage_group, scale=0.5),
                run_time=0.4
            )

            # Draw connecting line to next stage
            if i < len(stage_dots) - 1:
                line = Arrow(
                    stage_group[0].get_right(),
                    stage_dots[i+1][0].get_left(),
                    buff=0.1,
                    color=stages[i][1],
                    stroke_width=2,
                    max_tip_length_to_length_ratio=0.15
                )
                self.play(GrowArrow(line), run_time=0.3)

        self.wait(1)

        # Final message
        final = Text(
            "Let's explore each step in detail",
            font_size=28,
            color=SYNTH_CYAN
        )
        final.to_edge(DOWN).shift(UP)

        self.play(Write(final))
        self.wait(2)

        self.play(
            *[FadeOut(mob) for mob in self.mobjects]
        )
