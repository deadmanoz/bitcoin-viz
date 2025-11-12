"""
OUTPUT CONSTRUCTION - Bitcoin Transaction Lifecycle
==================================================

Shows the creation of transaction outputs from Bitcoin addresses.
Runtime: ~60-75 seconds
"""

from manim import *
import numpy as np
import sys
import os
# Add parent directories to path to import common module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common import *


class OutputConstruction(Scene):
    """
    Output Construction (0:30-1:30)
    Shows creating transaction outputs: P2WPKH for Bob, P2PKH for Alice's change.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
        title = Text("Output Construction", font_size=38, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Setup
        description = Text(
            "Alice creates two outputs: one for Bob, one for herself (change)",
            font_size=26,
            color=SYNTH_PEACH,
            weight=BOLD
        )
        description.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(description, shift=DOWN))
        self.wait(1.5)

        # Show the amounts
        amounts_text = Text(
            "0.7 BTC → Bob  |  0.14 BTC → Alice (change)",
            font_size=24,
            color=SYNTH_GREEN
        )
        amounts_text.to_edge(DOWN).shift(UP * 0.5)
        self.play(Write(amounts_text))
        self.wait(1)

        # Store explanation object
        explanation = amounts_text

        # === BOB'S OUTPUT (P2WPKH) ===
        bob_title = Text(
            "Bob's Output (P2WPKH - SegWit)",
            font_size=28,
            color=SYNTH_ORANGE,
            weight=BOLD
        )
        bob_title.move_to(explanation)

        self.play(
            Transform(explanation, bob_title),
            FadeOut(description),
            run_time=0.8
        )
        self.wait(0.5)

        # Show Bob's address
        bob_address = Text(
            "bc1qbob7x3...xyz123",
            font_size=22,
            color=SYNTH_ORANGE,
            font="Courier New"
        )
        bob_address.move_to(UP * 1.5)

        bob_format = Text(
            "(bech32 format - Native SegWit)",
            font_size=16,
            color=SYNTH_ORANGE
        )
        bob_format.next_to(bob_address, DOWN, buff=0.2)

        self.play(
            Write(bob_address),
            FadeIn(bob_format, shift=UP * 0.1),
            run_time=1
        )
        self.wait(1.5)

        # Decode address
        decode_text = Text(
            "Decoding bech32 address → extract 20-byte witness program",
            font_size=20,
            color=SYNTH_CYAN
        )
        decode_text.move_to(explanation)

        self.play(Transform(explanation, decode_text), run_time=0.8)
        self.wait(1)

        # Show decoded hash
        pub_key_hash = Text(
            "witness program: a7f3...9c2d",
            font_size=18,
            color=SYNTH_CYAN,
            font="Courier New"
        )
        pub_key_hash.next_to(bob_address, DOWN, buff=1)

        arrow = Arrow(
            bob_address.get_bottom(),
            pub_key_hash.get_top(),
            color=SYNTH_CYAN,
            buff=0.1,
            stroke_width=2
        )

        self.play(
            FadeOut(bob_format),
            GrowArrow(arrow),
            FadeIn(pub_key_hash, scale=0.8),
            run_time=1
        )
        self.wait(1.5)

        # Build scriptPubKey
        script_text = Text(
            "Building P2WPKH scriptPubKey",
            font_size=20,
            color=SYNTH_ORANGE
        )
        script_text.move_to(explanation)

        self.play(Transform(explanation, script_text), run_time=0.8)
        self.wait(1)

        # Show P2WPKH script
        script_pubkey_bob = self.create_script_box(
            "scriptPubKey (P2WPKH)",
            "OP_0 <20-byte pubKeyHash>",
            SYNTH_ORANGE
        )
        script_pubkey_bob.next_to(pub_key_hash, DOWN, buff=0.5)

        self.play(
            FadeOut(arrow),
            FadeIn(script_pubkey_bob, scale=0.8),
            run_time=1
        )
        self.wait(1.5)

        # Create Bob's output
        output_text = Text(
            "Creating Bob's output",
            font_size=20,
            color=SYNTH_ORANGE
        )
        output_text.move_to(explanation)

        self.play(Transform(explanation, output_text), run_time=0.8)
        self.wait(0.8)

        bob_output = self.create_output_box(
            "70000000 sat (0.7 BTC)",
            "scriptPubKey: OP_0 <hash>",
            SYNTH_ORANGE
        )
        bob_output.scale(0.9).move_to(LEFT * 3.5 + UP * 0.5)

        self.play(
            FadeOut(bob_address),
            FadeOut(pub_key_hash),
            FadeOut(script_pubkey_bob),
            FadeIn(bob_output, scale=0.5),
            run_time=1.2
        )
        self.wait(1)

        # === ALICE'S CHANGE OUTPUT (P2PKH) ===
        alice_title = Text(
            "Alice's Change Output (P2PKH - Legacy)",
            font_size=28,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        alice_title.move_to(explanation)

        self.play(Transform(explanation, alice_title), run_time=0.8)
        self.wait(0.5)

        # Show Alice's address
        alice_address = Text(
            "1Alice3x...abc456",
            font_size=22,
            color=SYNTH_GREEN,
            font="Courier New"
        )
        alice_address.move_to(UP * 1.5)

        alice_format = Text(
            "(Base58Check format - Legacy)",
            font_size=16,
            color=SYNTH_GREEN
        )
        alice_format.next_to(alice_address, DOWN, buff=0.2)

        self.play(
            Write(alice_address),
            FadeIn(alice_format, shift=UP * 0.1),
            run_time=1
        )
        self.wait(1)

        # Decode Alice's address (faster)
        decode_alice = Text(
            "Decoding Base58Check → extract pubKeyHash",
            font_size=20,
            color=SYNTH_CYAN
        )
        decode_alice.move_to(explanation)

        self.play(Transform(explanation, decode_alice), run_time=0.8)
        self.wait(0.8)

        # Show Alice's hash
        alice_hash = Text(
            "pubKeyHash: b6f9...4e1a",
            font_size=18,
            color=SYNTH_CYAN,
            font="Courier New"
        )
        alice_hash.next_to(alice_address, DOWN, buff=1)

        arrow2 = Arrow(
            alice_address.get_bottom(),
            alice_hash.get_top(),
            color=SYNTH_CYAN,
            buff=0.1,
            stroke_width=2
        )

        self.play(
            FadeOut(alice_format),
            GrowArrow(arrow2),
            FadeIn(alice_hash, scale=0.8),
            run_time=0.8
        )
        self.wait(1)

        # Build P2PKH scriptPubKey
        script_alice = Text(
            "Building P2PKH scriptPubKey",
            font_size=20,
            color=SYNTH_GREEN
        )
        script_alice.move_to(explanation)

        self.play(Transform(explanation, script_alice), run_time=0.8)
        self.wait(0.8)

        # Show P2PKH script
        script_pubkey_alice = self.create_script_box(
            "scriptPubKey (P2PKH)",
            "OP_DUP OP_HASH160 <pubKeyHash>\nOP_EQUALVERIFY OP_CHECKSIG",
            SYNTH_GREEN
        )
        script_pubkey_alice.next_to(alice_hash, DOWN, buff=0.5)

        self.play(
            FadeOut(arrow2),
            FadeIn(script_pubkey_alice, scale=0.8),
            run_time=1
        )
        self.wait(1.2)

        # Create Alice's output
        output_alice_text = Text(
            "Creating Alice's change output",
            font_size=20,
            color=SYNTH_GREEN
        )
        output_alice_text.move_to(explanation)

        self.play(Transform(explanation, output_alice_text), run_time=0.8)
        self.wait(0.8)

        alice_output = self.create_output_box(
            "14000000 sat (0.14 BTC)",
            "scriptPubKey: OP_DUP OP_HASH160...",
            SYNTH_GREEN
        )
        alice_output.scale(0.9).move_to(RIGHT * 3.5 + UP * 0.5)

        self.play(
            FadeOut(alice_address),
            FadeOut(alice_hash),
            FadeOut(script_pubkey_alice),
            FadeIn(alice_output, scale=0.5),
            run_time=1.2
        )
        self.wait(1)

        # === OUTPUTS ASSEMBLY ===
        assembly_text = Text(
            "Two outputs created — these will be included in the transaction data",
            font_size=24,
            color=SYNTH_CYAN
        )
        assembly_text.move_to(explanation)

        self.play(Transform(explanation, assembly_text))
        self.wait(1)

        # Highlight both outputs
        self.play(
            bob_output[0].animate.set_stroke(color=SYNTH_ORANGE, width=3),
            alice_output[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            run_time=1
        )
        self.wait(1)

        # Show output structure
        structure_text = Text(
            "Output 1: 70M sat + P2WPKH  |  Output 2: 14M sat + P2PKH",
            font_size=18,
            color=SYNTH_CYAN
        )
        structure_text.move_to(explanation)

        self.play(Transform(explanation, structure_text), run_time=0.8)
        self.wait(1.5)

        # Final caption
        ready_text = Text(
            "These outputs will be included in the data Alice signs",
            font_size=26,
            color=SYNTH_GOLD,
            weight=BOLD
        )
        ready_text.move_to(explanation)

        self.play(Transform(explanation, ready_text))
        self.wait(2)

    def create_script_box(self, label, content, color):
        """Create a box showing a Bitcoin script"""
        label_text = Text(label, font_size=18, color=color, weight=BOLD)
        content_text = Text(content, font_size=14, color=color, font="Courier New")
        content_text.set_opacity(0.95)

        text_group = VGroup(label_text, content_text).arrange(DOWN, buff=0.15)

        box = SurroundingRectangle(
            text_group,
            color=color,
            stroke_width=2.5,
            buff=0.25,
            corner_radius=0.08
        )
        box.set_fill(color=color, opacity=0.15)

        return VGroup(box, text_group)

    def create_output_box(self, amount, script_info, color):
        """Create an output box with amount and script info"""
        amount_text = Text(amount, font_size=18, color=color, weight=BOLD)
        script_text = Text(script_info, font_size=14, color=color)
        script_text.set_opacity(0.9)

        text_group = VGroup(amount_text, script_text).arrange(DOWN, buff=0.15)

        box = SurroundingRectangle(
            text_group,
            color=color,
            stroke_width=3,
            buff=0.3,
            corner_radius=0.1
        )
        box.set_fill(color=color, opacity=0.2)

        return VGroup(box, text_group)
