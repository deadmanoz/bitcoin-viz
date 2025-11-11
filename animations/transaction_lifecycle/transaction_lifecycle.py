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
            hex.move_to(center.get_center() + np.array([np.cos(angle), np.sin(angle), 0.0]) * 1.2)
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
                np.array([np.cos(angle) * 0.4, np.sin(angle) * 0.4, 0.0]),
                np.array([np.cos(angle) * 0.7 + 0.1, np.sin(angle) * 0.7 - 0.1, 0.0]),
                np.array([np.cos(angle) * 1.0, np.sin(angle) * 1.0, 0.0]),
            ]

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

        # Create nodes in a deterministic but varied layout
        # Pre-computed offsets for natural-looking positioning
        x_offsets = [0.2, -0.15, 0.1, -0.25, 0.18, -0.1, 0.22, 0.05, -0.2, 0.15, -0.18, 0.08, -0.12, 0.25, -0.05]
        y_offsets = [0.15, -0.1, 0.18, 0.05, -0.15, 0.12, -0.08, 0.2, 0.1, -0.18, 0.08, -0.12, 0.15, -0.05, 0.1]

        node_positions = []
        for i in range(15):
            # Arrange in rough layers
            layer = i // 5
            pos_in_layer = i % 5

            x = (pos_in_layer - 2) * 2 + x_offsets[i]
            y = 1 - layer * 1.5 + y_offsets[i]

            node_positions.append(np.array([x, y, 0.0]))

        # Create nodes
        for pos in node_positions:
            node = Dot(pos, radius=0.15, color=SYNTH_CYAN)
            node.set_sheen(-0.3, UP)  # Add 3D-like sheen
            nodes.add(node)

        # Create connections (deterministic pattern based on distance)
        connect_pattern = [True, False, True, True, False, True, False, True]  # Varied connection pattern
        for i, pos1 in enumerate(node_positions):
            for j, pos2 in enumerate(node_positions[i+1:], start=i+1):
                distance = np.linalg.norm(pos1 - pos2)
                # Only connect nearby nodes with deterministic pattern
                if distance < 2.5 and connect_pattern[(i + j) % len(connect_pattern)]:
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


class Act2_NodeValidation(Scene):
    """
    ACT 2: PROPAGATION - Node Validation (1:20-2:15)
    Shows Node Charlie validating the transaction through a checklist.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
        title = Text("Node Validation", font_size=38, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Show Node Charlie as a hexagonal structure
        node = RegularPolygon(n=6, radius=1.5, color=SYNTH_CYAN, stroke_width=3)
        node.set_fill(color=SYNTH_CYAN, opacity=0.15)
        node.shift(LEFT * 3)

        node_label = Text("Node Charlie", font_size=24, color=SYNTH_CYAN)
        node_label.next_to(node, DOWN, buff=0.3)

        self.play(
            DrawBorderThenFill(node),
            Write(node_label)
        )
        self.wait(0.5)

        # Transaction packet arriving
        tx_packet = Dot(radius=0.2, color=SYNTH_GREEN)
        tx_packet.move_to(LEFT * 7 + UP)

        arrival_text = Text(
            "Transaction packet arriving...",
            font_size=22,
            color=SYNTH_GREEN
        )
        arrival_text.to_edge(DOWN).shift(UP * 0.5)

        self.play(
            FadeIn(tx_packet, scale=0.3),
            Write(arrival_text)
        )

        # Packet moves to node
        self.play(
            tx_packet.animate.move_to(node.get_center()),
            run_time=1
        )
        self.wait(0.3)

        # Validation gauntlet text
        gauntlet_text = Text(
            "Validation Gauntlet",
            font_size=24,
            color=SYNTH_ORANGE,
            weight=BOLD
        )
        gauntlet_text.move_to(arrival_text)

        self.play(Transform(arrival_text, gauntlet_text))
        self.wait(0.5)

        # Create holographic checklist
        checks = [
            "Format & size limits",
            "Inputs reference valid UTXOs",
            "Signatures valid",
            "Input amounts ≥ outputs",
            "No double-spending",
            "Meets dust threshold",
            "Replace-By-Fee rules",
            "Local policy rules",
        ]

        checklist = VGroup()
        for i, check in enumerate(checks):
            # Checkbox
            box = Square(side_length=0.25, color=SYNTH_ORANGE, stroke_width=2)
            box.set_fill(color=SYNTH_ORANGE, opacity=0.1)

            # Check text
            text = Text(check, font_size=16, color=SYNTH_ORANGE)
            text.next_to(box, RIGHT, buff=0.2)

            check_item = VGroup(box, text)
            checklist.add(check_item)

        checklist.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        checklist.scale(0.9)
        checklist.next_to(node, RIGHT, buff=1)

        # Show checklist appearing
        for check_item in checklist:
            self.play(
                FadeIn(check_item, shift=LEFT * 0.3),
                run_time=0.3
            )

        self.wait(0.5)

        # Validate each item
        for i, check_item in enumerate(checklist):
            box = check_item[0]

            # Flash orange
            self.play(
                box.animate.set_fill(opacity=0.5),
                run_time=0.15
            )

            # Add checkmark
            checkmark = Text("✓", font_size=20, color=SYNTH_GREEN, weight=BOLD)
            checkmark.move_to(box)

            self.play(
                box.animate.set_stroke(color=SYNTH_GREEN).set_fill(color=SYNTH_GREEN, opacity=0.3),
                FadeIn(checkmark, scale=0.5),
                run_time=0.25
            )

            # Particle effect
            particles = VGroup(*[
                Dot(radius=0.05, color=SYNTH_GREEN).move_to(box.get_center())
                for _ in range(6)
            ])

            particle_anims = []
            for j, particle in enumerate(particles):
                angle = j * TAU / 6
                target = box.get_center() + np.array([np.cos(angle), np.sin(angle), 0.0]) * 0.5
                particle_anims.append(
                    particle.animate.move_to(target).set_opacity(0)
                )

            if i < len(checklist) - 1:
                self.play(*particle_anims, run_time=0.3)
            else:
                self.play(*particle_anims, run_time=0.5)

            self.wait(0.1)

        # All checks passed - barrier opens
        passed_text = Text(
            "All checks passed!",
            font_size=26,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        passed_text.move_to(arrival_text)

        self.play(
            Transform(arrival_text, passed_text),
            node.animate.set_stroke(color=SYNTH_GREEN, width=4),
            run_time=0.8
        )

        # Packet passes through with cyan flash
        flash = Circle(radius=2, color=SYNTH_CYAN, stroke_width=5)
        flash.move_to(node)

        self.play(
            FadeIn(flash, scale=0.5),
            flash.animate.scale(2).set_opacity(0),
            run_time=0.6
        )

        self.wait(1)

        # Packet exits to next stage
        self.play(
            tx_packet.animate.move_to(RIGHT * 7),
            run_time=1
        )

        self.wait(1)


class Act3_MempoolWaiting(Scene):
    """
    ACT 3: THE MEMPOOL (2:15-3:00)
    Shows the transaction entering the mempool and waiting for mining.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
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


class Act4_BlockTemplate(Scene):
    """
    ACT 4: MINING - Block Template (3:00-3:30)
    Shows a miner in Iceland assembling a block template.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
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
            color="#FFD700",
            weight=BOLD
        )
        coinbase_text.move_to(explain)

        coinbase = RegularPolygon(n=6, radius=0.35, color="#FFD700", stroke_width=3)
        coinbase.set_fill(color="#FFD700", opacity=0.3)
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
            color="#FFD700"
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


class Act4_Mining(Scene):
    """
    ACT 4: MINING - Mining Process (3:30-4:00)
    Shows the mining process with hash attempts.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
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


class Act5_BlockPropagation(Scene):
    """
    ACT 5: CONFIRMATION - Block Relay (4:00-4:30)
    Shows the block propagating through the network.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
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


class Act5_ChainExtension(Scene):
    """
    ACT 5: CONFIRMATION - Chain Extension (4:30-5:00)
    Shows the block being added to the chain and confirmations accumulating.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
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
            block.move_to(np.array([x_pos, y_pos, 0]))

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
            block.move_to(np.array([x_pos, y_pos, 0]))
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
