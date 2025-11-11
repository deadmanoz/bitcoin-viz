"""
INCOMING TRANSACTION PROCESSING - Bitcoin Core Deep Dive
=========================================================

Technical deep-dive showing how Bitcoin Core processes incoming transactions
from P2P network layer through validation to mempool admission.
Based on Bitcoin Core v30.0 source code.

Runtime: ~2-3 minutes (condensed version of 14-minute script)
"""

from manim import *
import numpy as np
from common import *


class IncomingTransactionIntro(Scene):
    """
    Title & Context (0:00 - 0:15)
    Introduces the transaction processing pipeline.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Main title with cyberpunk aesthetic
        title = Text(
            "Inside Bitcoin Core",
            font_size=48,
            color=SYNTH_CYAN,
            weight=BOLD
        )

        subtitle = Text(
            "Transaction Processing",
            font_size=36,
            color=SYNTH_PEACH
        )
        subtitle.next_to(title, DOWN, buff=0.5)

        version = Text(
            "Bitcoin Core v30.0",
            font_size=24,
            color=SYNTH_ORANGE
        )
        version.next_to(subtitle, DOWN, buff=0.8)

        # Animate title sequence
        self.play(
            Write(title),
            run_time=1
        )
        self.play(
            FadeIn(subtitle, shift=UP),
            run_time=0.8
        )
        self.play(
            FadeIn(version, scale=0.5),
            run_time=0.6
        )

        self.wait(1)

        # Stats overlay
        stats = VGroup(
            Text("~300,000 lines of C++ code", font_size=20, color=SYNTH_GREEN),
            Text("5 validation stages", font_size=20, color=SYNTH_GREEN),
            Text("16+ critical checks", font_size=20, color=SYNTH_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        stats.to_edge(DOWN).shift(UP * 0.5)

        self.play(
            LaggedStart(*[FadeIn(stat, shift=RIGHT) for stat in stats], lag_ratio=0.3),
            run_time=1.5
        )

        self.wait(1.5)

        # Fade out for next scene
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=0.8
        )


class NetworkLayer(Scene):
    """
    The Network Layer - Receiving the Message (0:15 - 0:45)
    Shows P2P message arrival and initial processing.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
        title = Text("Network Layer", font_size=36, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.3)

        # Create two nodes
        peer_node = Circle(radius=0.6, color=SYNTH_ORANGE, fill_opacity=0.3)
        peer_node.add(Text("Peer", font_size=18, color=SYNTH_ORANGE))
        peer_node.shift(LEFT * 4)

        our_node = Circle(radius=0.6, color=SYNTH_CYAN, fill_opacity=0.3)
        our_node.add(Text("Our Node", font_size=18, color=SYNTH_CYAN))
        our_node.shift(RIGHT * 4)

        # Connection line
        connection = Line(
            peer_node.get_right(),
            our_node.get_left(),
            color=SYNTH_PURPLE,
            stroke_width=2
        )

        self.play(
            FadeIn(peer_node, scale=0.5),
            FadeIn(our_node, scale=0.5),
            Create(connection),
            run_time=1.2
        )
        self.wait(0.5)

        # Transaction packet
        tx_packet = RoundedRectangle(
            width=1.2,
            height=0.8,
            corner_radius=0.15,
            color=SYNTH_GREEN,
            fill_opacity=0.4
        )
        tx_label = Text("tx", font_size=20, color=SYNTH_GREEN, weight=BOLD)
        tx_packet.add(tx_label)
        tx_packet.move_to(peer_node.get_center())

        self.play(FadeIn(tx_packet, scale=0.3))
        self.wait(0.3)

        # Animate packet traveling
        self.play(
            tx_packet.animate.move_to(our_node.get_center()),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_cubic
        )

        # Packet arrival flash
        self.play(
            Flash(our_node, color=SYNTH_GREEN, flash_radius=1.2),
            tx_packet.animate.set_fill(opacity=0.7),
            run_time=0.5
        )
        self.wait(0.5)

        # Show code overlay
        code_lines = [
            "// src/net_processing.cpp:3415",
            "void PeerManagerImpl::ProcessMessage(",
            "    CNode& pfrom,",
            "    const std::string& msg_type,  // \"tx\"",
            "    DataStream& vRecv",
            ") {"
        ]

        code_text = VGroup()
        for line in code_lines:
            line_text = Text(
                line,
                font="Monospace",
                font_size=16,
                color=SYNTH_CYAN
            )
            code_text.add(line_text)

        code_text.arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        # Background box
        code_bg = Rectangle(
            width=code_text.width + 0.6,
            height=code_text.height + 0.4,
            color=SYNTH_CYAN,
            fill_opacity=0.1,
            stroke_width=2
        )
        code_bg.move_to(code_text.get_center())

        code_group = VGroup(code_bg, code_text)
        code_group.to_edge(DOWN).shift(UP * 0.3)

        self.play(
            FadeIn(code_group, shift=UP),
            run_time=1
        )
        self.wait(2)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class DownloadManagement(Scene):
    """
    Download Management - Orphan Detection (0:45 - 1:15)
    Shows the three-way branch: normal tx, orphan, or package.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Title
        title = Text("Download Manager", font_size=36, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))

        # Transaction at center top
        tx_box = RoundedRectangle(
            width=2, height=1,
            corner_radius=0.2,
            color=SYNTH_GREEN,
            fill_opacity=0.3
        )
        tx_label = Text("Transaction", font_size=20, color=SYNTH_GREEN)
        tx_box.add(tx_label)
        tx_box.shift(UP * 2)

        self.play(FadeIn(tx_box, scale=0.5))
        self.wait(0.5)

        # Question text
        question = Text(
            "Do we have all parent transactions?",
            font_size=22,
            color=SYNTH_PEACH
        )
        question.next_to(tx_box, DOWN, buff=0.5)
        self.play(Write(question))
        self.wait(1)

        # Three paths
        paths = VGroup()

        # Left path: Normal
        normal_path = VGroup(
            Arrow(tx_box.get_bottom(), LEFT * 3 + DOWN * 1.5, color=SYNTH_GREEN),
            RoundedRectangle(
                width=2.5, height=1.2,
                corner_radius=0.15,
                color=SYNTH_GREEN,
                fill_opacity=0.2
            ),
            Text("All parents exist", font_size=18, color=SYNTH_GREEN)
        )
        normal_path[1].move_to(LEFT * 3 + DOWN * 2.5)
        normal_path[2].move_to(normal_path[1].get_center())

        # Middle path: Orphan
        orphan_path = VGroup(
            Arrow(tx_box.get_bottom(), DOWN * 2, color=SYNTH_ORANGE),
            RoundedRectangle(
                width=2.5, height=1.2,
                corner_radius=0.15,
                color=SYNTH_ORANGE,
                fill_opacity=0.2
            ),
            Text("Missing parent\n(orphan)", font_size=18, color=SYNTH_ORANGE)
        )
        orphan_path[1].move_to(DOWN * 2.5)
        orphan_path[2].move_to(orphan_path[1].get_center())

        # Right path: Package
        package_path = VGroup(
            Arrow(tx_box.get_bottom(), RIGHT * 3 + DOWN * 1.5, color=SYNTH_PURPLE),
            RoundedRectangle(
                width=2.5, height=1.2,
                corner_radius=0.15,
                color=SYNTH_PURPLE,
                fill_opacity=0.2
            ),
            Text("Parent arrives\n(package!)", font_size=18, color=SYNTH_PURPLE)
        )
        package_path[1].move_to(RIGHT * 3 + DOWN * 2.5)
        package_path[2].move_to(package_path[1].get_center())

        # Animate three paths
        self.play(
            FadeOut(question),
            LaggedStart(
                *[Create(path) for path in [normal_path, orphan_path, package_path]],
                lag_ratio=0.3
            ),
            run_time=2
        )
        self.wait(1.5)

        # Highlight normal path
        self.play(
            normal_path[0].animate.set_color(SYNTH_GREEN).set_stroke(width=6),
            normal_path[1].animate.set_stroke(width=3),
            run_time=0.8
        )

        validate_text = Text("→ VALIDATE", font_size=20, color=SYNTH_GREEN, weight=BOLD)
        validate_text.next_to(normal_path[1], DOWN, buff=0.3)
        self.play(Write(validate_text))
        self.wait(1.5)

        # Fade out
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class ValidationPipeline(Scene):
    """
    Validation Pipeline Entrance (1:15 - 1:45)
    Shows the 5-stage validation pipeline.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Title
        title = Text("Validation Pipeline", font_size=36, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))

        # Transaction entering
        tx = RoundedRectangle(
            width=1.5, height=1,
            corner_radius=0.2,
            color=SYNTH_GREEN,
            fill_opacity=0.4
        )
        tx_label = Text("TX", font_size=24, color=SYNTH_GREEN, weight=BOLD)
        tx.add(tx_label)
        tx.shift(LEFT * 6)

        self.play(FadeIn(tx, shift=RIGHT))

        # Create 5 pipeline stages
        stages = [
            {"name": "PreChecks", "color": SYNTH_GREEN},
            {"name": "RBF Checks", "color": SYNTH_ORANGE},
            {"name": "Policy Scripts", "color": SYNTH_CYAN},
            {"name": "Consensus Scripts", "color": SYNTH_PURPLE},
            {"name": "Finalization", "color": SYNTH_PEACH},
        ]

        stage_boxes = VGroup()
        for i, stage in enumerate(stages):
            box = VGroup(
                RoundedRectangle(
                    width=2.2,
                    height=1.5,
                    corner_radius=0.15,
                    color=stage["color"],
                    fill_opacity=0.2,
                    stroke_width=2
                ),
                Text(stage["name"], font_size=14, color=stage["color"])
            )
            box[1].move_to(box[0].get_center())
            # Arrange horizontally
            x_pos = -4.5 + (i * 2.3)
            box.move_to([x_pos, 0, 0])
            stage_boxes.add(box)

        # Create pipeline
        self.play(
            LaggedStart(
                *[FadeIn(box, scale=0.8) for box in stage_boxes],
                lag_ratio=0.15
            ),
            run_time=2
        )
        self.wait(0.5)

        # Animate transaction flowing through pipeline
        for i, box in enumerate(stage_boxes):
            self.play(
                tx.animate.move_to(box.get_center()),
                box[0].animate.set_fill(opacity=0.5).set_stroke(width=4),
                run_time=0.8
            )
            # Flash effect
            self.play(
                Flash(box, color=stages[i]["color"], flash_radius=1.5),
                run_time=0.3
            )
            # Reset stroke
            if i < len(stage_boxes) - 1:
                self.play(
                    box[0].animate.set_stroke(width=2).set_fill(opacity=0.2),
                    run_time=0.3
                )
            self.wait(0.2)

        # Success - transaction glows green
        self.play(
            tx.animate.set_fill(opacity=0.8).scale(1.3),
            Flash(tx, color=SYNTH_GREEN, flash_radius=2),
            run_time=1
        )

        success_text = Text("✓ ACCEPTED", font_size=28, color=SYNTH_GREEN, weight=BOLD)
        success_text.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(success_text))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class PreChecks(Scene):
    """
    PreChecks Stage - Fast Fail-Early Validation (1:45 - 2:15)
    Shows key validation checks with pass/fail indicators.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Title
        title = Text("Stage 1: PreChecks", font_size=36, color=SYNTH_GREEN)
        title.to_edge(UP)
        self.play(Write(title))

        subtitle = Text(
            "Fast Fail-Early Validation",
            font_size=22,
            color=SYNTH_PEACH
        )
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(0.5)

        # Transaction in center
        tx_box = RoundedRectangle(
            width=2, height=1.5,
            corner_radius=0.2,
            color=SYNTH_GREEN,
            fill_opacity=0.3
        )
        tx_label = Text("Transaction", font_size=18, color=SYNTH_GREEN)
        tx_box.add(tx_label)
        tx_box.shift(UP * 1.5)
        self.play(FadeIn(tx_box, scale=0.5))

        # Checks list
        checks = [
            "✓ Basic Structure",
            "✓ Standard Format",
            "✓ Finality",
            "✓ UTXO Availability",
            "✓ Input Values",
            "✓ Sigop Cost (< 16000)",
            "✓ Fee Rate (≥ 0.1 sat/vB)",
        ]

        check_items = VGroup()
        for check_text in checks:
            check = Text(check_text, font_size=18, color=SYNTH_GREEN)
            check_items.add(check)

        check_items.arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        check_items.next_to(tx_box, DOWN, buff=0.8)
        check_items.shift(LEFT * 0.5)

        # Animate checks appearing one by one
        for check in check_items:
            self.play(
                FadeIn(check, shift=RIGHT),
                Flash(check.get_left(), color=SYNTH_GREEN, flash_radius=0.3),
                run_time=0.4
            )
            self.wait(0.15)

        self.wait(1)

        # Summary
        summary = Text(
            "16 rapid checks passed ✓",
            font_size=24,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        summary.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(summary))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class MempoolAdmission(Scene):
    """
    Mempool Admission (2:15 - 2:45)
    Shows transaction entering the mempool.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Title
        title = Text("Mempool Admission", font_size=36, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))

        # Create mempool visualization (grid of transactions)
        mempool_box = Rectangle(
            width=8,
            height=4,
            color=SYNTH_CYAN,
            fill_opacity=0.1,
            stroke_width=3
        )
        mempool_label = Text("Mempool", font_size=28, color=SYNTH_CYAN)
        mempool_label.next_to(mempool_box, UP, buff=0.3)

        self.play(
            Create(mempool_box),
            Write(mempool_label),
            run_time=1.2
        )

        # Show existing transactions in mempool (small dots)
        existing_txs = VGroup()
        for _ in range(20):
            dot = Dot(
                radius=0.08,
                color=SYNTH_ORANGE,
                fill_opacity=0.6
            )
            dot.move_to([
                np.random.uniform(-3.5, 3.5),
                np.random.uniform(-1.5, 1.5),
                0
            ])
            existing_txs.add(dot)

        self.play(
            LaggedStart(
                *[FadeIn(dot, scale=0.3) for dot in existing_txs],
                lag_ratio=0.05
            ),
            run_time=1
        )
        self.wait(0.5)

        # Our transaction arriving
        our_tx = RoundedRectangle(
            width=1.5,
            height=0.8,
            corner_radius=0.15,
            color=SYNTH_GREEN,
            fill_opacity=0.6,
            stroke_width=3
        )
        our_tx_label = Text("Our TX", font_size=14, color=SYNTH_GREEN, weight=BOLD)
        our_tx.add(our_tx_label)
        our_tx.shift(UP * 4)

        self.play(FadeIn(our_tx, shift=DOWN))

        # Transaction enters mempool
        final_pos = [2, 1, 0]
        self.play(
            our_tx.animate.move_to(final_pos).scale(0.7),
            run_time=1.5,
            rate_func=rate_functions.ease_in_out_cubic
        )

        # Success flash
        self.play(
            Flash(our_tx, color=SYNTH_GREEN, flash_radius=1.5),
            our_tx.animate.set_fill(opacity=0.8),
            run_time=0.8
        )

        # Show transaction details
        details = VGroup(
            Text("txid: abc123...", font_size=14, color=SYNTH_CYAN),
            Text("Fee: 0.00025 BTC", font_size=14, color=SYNTH_PEACH),
            Text("Rate: 100 sat/vB", font_size=14, color=SYNTH_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)

        details_box = Rectangle(
            width=3,
            height=1.5,
            color=SYNTH_CYAN,
            fill_opacity=0.2
        )
        details.move_to(details_box.get_center())
        details_group = VGroup(details_box, details)
        details_group.to_edge(RIGHT).shift(LEFT * 0.5)

        self.play(FadeIn(details_group, shift=LEFT))
        self.wait(1.5)

        # Final message
        success = Text(
            "✓ Ready for Mining",
            font_size=28,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        success.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(success))

        self.wait(2)
        self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.8)


class IncomingTransactionComplete(Scene):
    """
    Complete sequence combining all scenes.
    This is the main scene to render.
    """

    def construct(self):
        # Play all scenes in sequence
        scenes = [
            IncomingTransactionIntro,
            NetworkLayer,
            DownloadManagement,
            ValidationPipeline,
            PreChecks,
            MempoolAdmission
        ]

        for scene_class in scenes:
            scene = scene_class()
            scene.construct()
