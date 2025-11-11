"""
ACT 2: PROPAGATION - Bitcoin Transaction Lifecycle
===================================================

Shows P2P network broadcasting and node validation.
Runtime: ~1 minute
"""

from manim import *
import numpy as np
import sys
sys.path.append("..")
from common import *


class InitialBroadcast(Scene):
    """
    Initial Broadcast (0:00-0:20)
    Shows the transaction broadcasting through the P2P network.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
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


class NodeValidation(Scene):
    """
    Node Validation (0:20-1:15)
    Shows Node Charlie validating the transaction through a checklist.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
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
