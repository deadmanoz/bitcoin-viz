"""
SIGNING & INPUT CONSTRUCTION - Bitcoin Transaction Lifecycle
===========================================================

Shows the cryptographic signing process and input creation.
Runtime: ~90-120 seconds
"""

from manim import *
import numpy as np
import sys
import os
# Add parent directories to path to import common module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from common import *


class SigningAndInputConstruction(Scene):
    """
    Signing & Input Construction
    Shows the cryptographic signing process and input creation.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title
        title = Text("Signing & Input Construction", font_size=38, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Show the 2 selected UTXOs
        description = Text(
            "To spend these UTXOs, Alice must prove ownership",
            font_size=26,
            color=SYNTH_PEACH,
            weight=BOLD
        )
        description.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(description, shift=DOWN))
        self.wait(1.5)

        # Create the 2 UTXOs as simple rectangles
        utxo1 = self.create_simple_utxo("0.5 BTC", "abc123...def456", "#0")
        utxo1.move_to(LEFT * 3 + UP * 0.8)

        utxo2 = self.create_simple_utxo("0.35 BTC", "789ghi...jkl012", "#1")
        utxo2.move_to(RIGHT * 3 + UP * 0.8)

        self.play(
            FadeIn(utxo1, scale=0.8),
            FadeIn(utxo2, scale=0.8),
            run_time=1
        )
        self.wait(1)

        # === SHOW KEYS (BOTH AT ONCE) ===
        keys_explanation = Text(
            "Each UTXO has corresponding private and public keys",
            font_size=24,
            color=SYNTH_CYAN
        )
        keys_explanation.to_edge(DOWN).shift(UP * 0.5)

        self.play(
            FadeOut(description),
            FadeIn(keys_explanation),
            run_time=0.8
        )
        self.wait(1)

        # Show both keys from the start
        private_key = self.create_private_key_visual()
        private_key.scale(1.2).move_to(LEFT * 5 + DOWN * 0.5)

        public_key = self.create_public_key_visual()
        public_key.scale(1.2).move_to(LEFT * 2.5 + DOWN * 0.5)

        self.play(
            FadeIn(private_key, scale=0.5),
            FadeIn(public_key, scale=0.5),
            run_time=1
        )
        self.wait(1.5)

        # === SIGNATURE CREATION ===
        signing_text = Text(
            "Signing Process",
            font_size=28,
            color=SYNTH_GOLD,
            weight=BOLD
        )
        signing_text.move_to(keys_explanation)

        self.play(Transform(keys_explanation, signing_text), run_time=0.8)
        self.wait(0.5)

        # Store the explanation text object for reuse
        explanation = keys_explanation

        # Move keys to the side for more space
        keys_group = VGroup(private_key, public_key)
        self.play(
            keys_group.animate.scale(0.7).to_edge(LEFT).shift(DOWN * 1.5),
            run_time=1
        )
        self.wait(0.5)

        # Process first UTXO with detailed explanations
        input1 = self.sign_utxo_and_create_input(
            utxo1, "abc123...def456", "0", private_key, explanation, 1
        )
        self.wait(1)

        # Process second UTXO (can be faster since pattern is established)
        input2 = self.sign_utxo_and_create_input(
            utxo2, "789ghi...jkl012", "1", private_key, explanation, 2
        )
        self.wait(1)

        # === INPUT ASSEMBLY ===
        assembly_text = Text(
            "Two signed inputs ready — they unlock 0.85 BTC total",
            font_size=26,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        assembly_text.move_to(explanation)

        self.play(Transform(explanation, assembly_text))

        # Highlight both inputs
        self.play(
            input1[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            input2[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            run_time=1
        )
        self.wait(1.5)

        # Final caption
        ready_text = Text(
            "Ready to assemble the complete transaction",
            font_size=26,
            color=SYNTH_CYAN,
            weight=BOLD
        )
        ready_text.move_to(explanation)

        self.play(Transform(explanation, ready_text))
        self.wait(2)

    def create_simple_utxo(self, amount, txid, output):
        """Create a simple rectangular UTXO"""
        amount_text = Text(amount, font_size=20, color=SYNTH_GREEN, weight=BOLD)
        txid_text = Text(txid, font_size=12, color=SYNTH_CYAN)
        output_text = Text(f"output {output}", font_size=12, color=SYNTH_CYAN)

        details = VGroup(txid_text, output_text).arrange(DOWN, buff=0.05)
        labels = VGroup(amount_text, details).arrange(DOWN, buff=0.15)

        box = SurroundingRectangle(
            labels,
            color=SYNTH_GREEN,
            stroke_width=2,
            buff=0.25,
            corner_radius=0.1
        )
        box.set_fill(color=SYNTH_GREEN, opacity=0.15)

        return VGroup(box, labels)

    def create_private_key_visual(self):
        """Create a visual representation of a private key - using PINK color"""
        key_circle = Circle(radius=0.4, color=SYNTH_PINK, stroke_width=4)
        key_circle.set_fill(color=SYNTH_PINK, opacity=0.4)

        key_shaft = Rectangle(
            width=0.8, height=0.2,
            color=SYNTH_PINK,
            stroke_width=4
        )
        key_shaft.set_fill(color=SYNTH_PINK, opacity=0.4)
        key_shaft.next_to(key_circle, RIGHT, buff=0)

        key_icon = VGroup(key_circle, key_shaft)

        key_label = Text("Private Key", font_size=18, color=SYNTH_PINK, weight=BOLD)
        key_label.next_to(key_icon, DOWN, buff=0.3)

        hex_text = Text("5Kb8...3Qm", font_size=14, color=SYNTH_PINK)
        hex_text.set_opacity(0.9)
        hex_text.next_to(key_label, DOWN, buff=0.15)

        return VGroup(key_icon, key_label, hex_text)

    def create_public_key_visual(self):
        """Create a visual representation of a public key"""
        pub_circle = Circle(radius=0.45, color=SYNTH_CYAN, stroke_width=4)
        pub_circle.set_fill(color=SYNTH_CYAN, opacity=0.3)

        pub_label = Text("Public Key", font_size=18, color=SYNTH_CYAN, weight=BOLD)
        pub_label.next_to(pub_circle, DOWN, buff=0.3)

        hex_text = Text("02a1b2...c3d4", font_size=14, color=SYNTH_CYAN)
        hex_text.set_opacity(0.9)
        hex_text.next_to(pub_label, DOWN, buff=0.15)

        return VGroup(pub_circle, pub_label, hex_text)

    def sign_utxo_and_create_input(self, utxo, txid, vout, private_key, explanation, utxo_num):
        """Sign a UTXO and create the corresponding input with detailed explanations"""

        # STEP 1: Show the locking script from the UTXO
        step1_text = Text(
            f"UTXO #{utxo_num}: The locking script (scriptPubKey) requires Alice's signature",
            font_size=22,
            color=SYNTH_ORANGE
        )
        step1_text.move_to(explanation)

        self.play(Transform(explanation, step1_text), run_time=0.8)
        self.wait(1.5)

        script_pubkey = self.create_script_box(
            "scriptPubKey (locking script)",
            "OP_DUP OP_HASH160 <pubKeyHash>\nOP_EQUALVERIFY OP_CHECKSIG",
            SYNTH_ORANGE
        )
        script_pubkey.scale(0.8).next_to(utxo, DOWN, buff=0.5)

        self.play(FadeIn(script_pubkey, shift=UP * 0.2), run_time=1)
        self.wait(2)

        # STEP 2: Explain signature creation
        step2_text = Text(
            "Alice signs the transaction data with her private key (ECDSA)",
            font_size=22,
            color=SYNTH_GOLD
        )
        step2_text.move_to(explanation)

        self.play(Transform(explanation, step2_text), run_time=0.8)
        self.wait(1.5)

        # Signature creation effect - radial glow from private key
        glow = self.create_signature_glow()
        glow.move_to(private_key.get_center())

        self.play(Create(glow), run_time=1.2)
        self.wait(0.8)

        # Create signature
        signature = self.create_signature_visual()
        signature.scale(1.1).move_to(ORIGIN + DOWN * 0.3)

        self.play(
            FadeOut(glow),
            FadeIn(signature, scale=0.5),
            run_time=1
        )
        self.wait(2)

        # STEP 3: Explain scriptSig creation
        step3_text = Text(
            "The unlocking script (scriptSig) combines signature + public key",
            font_size=22,
            color=SYNTH_GREEN
        )
        step3_text.move_to(explanation)

        self.play(Transform(explanation, step3_text), run_time=0.8)
        self.wait(1.5)

        # Create the unlocking script (scriptSig)
        script_sig = self.create_script_box(
            "scriptSig (unlocking script)",
            "<signature> <publicKey>",
            SYNTH_GOLD
        )
        script_sig.scale(0.8).next_to(signature, DOWN, buff=0.4)

        self.play(
            FadeIn(script_sig, shift=UP * 0.2),
            run_time=1
        )
        self.wait(2)

        # STEP 4: Build the complete input
        step4_text = Text(
            "Assembling the transaction input with all required fields",
            font_size=22,
            color=SYNTH_GREEN
        )
        step4_text.move_to(explanation)

        self.play(Transform(explanation, step4_text), run_time=0.8)
        self.wait(1)

        # Build the input component
        input_component = self.create_input_box(txid, vout)
        input_component.move_to(utxo)

        self.play(
            FadeOut(script_pubkey),
            FadeOut(signature),
            FadeOut(script_sig),
            Transform(utxo, input_component),
            run_time=1.2
        )
        self.wait(1.5)

        return utxo

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

    def create_signature_glow(self):
        """Create a pulsing radial glow effect for signature generation"""
        # Create concentric circles that pulse outward from the private key
        circles = VGroup()
        for i in range(3):
            radius = 0.4 + i * 0.25
            circle = Circle(
                radius=radius,
                color=SYNTH_GOLD,
                stroke_width=3 - i,
                stroke_opacity=0.7 - i * 0.2
            )
            circles.add(circle)
        
        return circles

    def create_signature_visual(self):
        """Create a visual representation of a digital signature"""
        sig_text = Text("Signature", font_size=20, color=SYNTH_GOLD, weight=BOLD)
        hex_text = Text("304402...", font_size=16, color=SYNTH_GOLD, font="Courier New")

        sig_group = VGroup(sig_text, hex_text).arrange(DOWN, buff=0.1)

        box = SurroundingRectangle(
            sig_group,
            color=SYNTH_GOLD,
            stroke_width=3,
            buff=0.2,
            corner_radius=0.08
        )
        box.set_fill(color=SYNTH_GOLD, opacity=0.3)

        return VGroup(box, sig_group)

    def create_input_box(self, txid, vout):
        """Create a transaction input box"""
        txid_label = Text(f"txid: {txid}", font_size=12, color=SYNTH_GREEN)
        vout_label = Text(f"vout: {vout}", font_size=12, color=SYNTH_GREEN)
        scriptsig_label = Text("scriptSig: <sig> <pubKey>", font_size=10, color=SYNTH_GOLD)
        scriptsig_label.set_opacity(0.8)
        sequence_label = Text("sequence: 0xffffffff", font_size=10, color=SYNTH_GREEN)
        sequence_label.set_opacity(0.7)

        input_data = VGroup(
            txid_label, vout_label, scriptsig_label, sequence_label
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)

        box = SurroundingRectangle(
            input_data,
            color=SYNTH_GREEN,
            stroke_width=2,
            buff=0.2,
            corner_radius=0.1
        )
        box.set_fill(color=SYNTH_GREEN, opacity=0.15)

        return VGroup(box, input_data)
