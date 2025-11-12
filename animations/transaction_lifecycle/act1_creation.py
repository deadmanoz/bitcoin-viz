"""
ACT 1: CREATION - Bitcoin Transaction Lifecycle
================================================

Shows wallet UTXO selection and transaction construction.
Runtime: ~1 minute
"""

from manim import *
import numpy as np
import sys
import os
# Add parent directory to path to import common module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
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
        wallet_label = Text("Alice's Available Funds: 0.95 BTC across 3 UTXOs", font_size=24, color=SYNTH_PEACH)
        wallet_label.to_edge(UP).shift(DOWN * 0.8)
        self.play(FadeIn(wallet_label, shift=DOWN))

        # Create UTXOs as hexagonal shapes (larger radius for more space)
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

        # Show UTXO selection - highlight selected ones
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

        self.wait(1.5)

        # Fade out unselected UTXO and other elements
        self.play(
            FadeOut(utxos[2]),
            FadeOut(grid),
            FadeOut(wallet_label),
            FadeOut(coin_selection_label),
            run_time=1
        )
        self.wait(0.5)

        # === Transaction Structure Visualization ===
        # Transform the text to show we're consuming the UTXOs
        consuming_text = Text(
            "Alice's 2 UTXOs are completely consumed",
            font_size=22,
            color=SYNTH_CYAN
        )
        consuming_text.to_edge(DOWN).shift(UP * 0.5)

        self.play(
            Transform(explain, consuming_text),
            FadeOut(change_text),
            run_time=0.8
        )
        self.wait(0.5)

        # Move selected UTXOs to the left side
        self.play(
            utxos[0].animate.move_to(LEFT * 4 + UP * 0.8).scale(0.7),
            utxos[1].animate.move_to(LEFT * 4 + DOWN * 0.8).scale(0.7),
            run_time=1
        )
        self.wait(0.3)

        # Create central pool (glowing circle)
        central_pool = Circle(radius=0.8, color=SYNTH_CYAN, stroke_width=3)
        central_pool.set_fill(color=SYNTH_CYAN, opacity=0.2)

        pool_label = Text("0.85 BTC", font_size=20, color=SYNTH_CYAN, weight=BOLD)
        pool_label.next_to(central_pool, UP, buff=0.3)

        pool_group = VGroup(central_pool, pool_label)

        self.play(
            FadeIn(central_pool, scale=0.3),
            run_time=0.8
        )

        # Break down UTXOs into particles
        particles1 = self.create_particles(utxos[0].get_center(), 15)
        particles2 = self.create_particles(utxos[1].get_center(), 15)

        # Animate particles flowing from UTXOs to center
        self.play(
            *[particle.animate.move_to(central_pool.get_center() +
                np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0]))
                for particle in particles1],
            *[particle.animate.move_to(central_pool.get_center() +
                np.array([np.random.uniform(-0.3, 0.3), np.random.uniform(-0.3, 0.3), 0]))
                for particle in particles2],
            FadeOut(utxos[0]),
            FadeOut(utxos[1]),
            run_time=1.5
        )

        # Show pool label with pulsing effect
        self.play(
            Write(pool_label),
            central_pool.animate.set_fill(opacity=0.3),
            run_time=0.5
        )
        self.play(
            central_pool.animate.set_fill(opacity=0.15),
            run_time=0.5
        )
        self.wait(0.5)

        # Create output boxes on the right
        output1_box = self.create_output_box("0.7 BTC", "(to Bob)", SYNTH_ORANGE)
        output1_box.move_to(RIGHT * 4 + UP * 1.2)

        output2_box = self.create_output_box("0.14 BTC", "(change)", SYNTH_ORANGE)
        output2_box.move_to(RIGHT * 4 + DOWN * 0.2)

        # Fee output box - more ephemeral looking with SYNTH_GOLD and lower opacity
        fee_box = self.create_output_box("0.01 BTC", "(fee to miners)", SYNTH_GOLD)
        fee_box.move_to(RIGHT * 4 + DOWN * 1.6)
        fee_box[0].set_stroke(opacity=0.6)  # More ephemeral border
        fee_box[1].set_opacity(0.7)  # More ephemeral text

        # Split particles and flow to outputs (proportional to value)
        # Total 30 particles: ~21 to Bob, ~4 to change, ~5 to fees
        particles_to_output1 = particles1[:11] + particles2[:10]  # 21 particles for 0.7 BTC
        particles_to_output2 = particles1[11:13] + particles2[10:12]  # 4 particles for 0.14 BTC
        particles_to_fee = particles1[13:] + particles2[12:]  # 5 particles for 0.01 BTC

        self.play(
            *[particle.animate.move_to(output1_box.get_center() +
                np.array([np.random.uniform(-0.4, 0.4), np.random.uniform(-0.3, 0.3), 0]))
                for particle in particles_to_output1],
            *[particle.animate.move_to(output2_box.get_center() +
                np.array([np.random.uniform(-0.4, 0.4), np.random.uniform(-0.3, 0.3), 0]))
                for particle in particles_to_output2],
            *[particle.animate.move_to(fee_box.get_center() +
                np.array([np.random.uniform(-0.4, 0.4), np.random.uniform(-0.3, 0.3), 0]))
                for particle in particles_to_fee],
            FadeOut(pool_label),
            central_pool.animate.set_fill(opacity=0.05),
            run_time=1.5
        )

        # Coalesce particles into output boxes
        self.play(
            FadeIn(output1_box, scale=0.5),
            FadeIn(output2_box, scale=0.5),
            FadeIn(fee_box, scale=0.5),
            *[FadeOut(particle) for particle in particles1 + particles2],
            run_time=1
        )

        # Show caption about creating new UTXOs and fees
        creating_line1 = Text(
            "...creating 2 new UTXOs: 0.7 BTC (for Bob) and 0.14 BTC (change)",
            font_size=20,
            color=SYNTH_GREEN
        )
        creating_line2 = Text(
            "and contributing 0.01 BTC in fees to the block reward",
            font_size=20,
            color=SYNTH_GREEN
        )

        creating_text = VGroup(creating_line1, creating_line2).arrange(DOWN, buff=0.2, center=True)
        creating_text.to_edge(DOWN).shift(UP * 0.5)

        self.play(
            Transform(explain, creating_text),
            run_time=1
        )
        self.wait(1.5)

        # Recreate input boxes to show final transaction structure
        input1_box = self.create_output_box("0.5 BTC", "", SYNTH_GREEN)
        input1_box.move_to(LEFT * 4 + UP * 1.2)

        input2_box = self.create_output_box("0.35 BTC", "", SYNTH_GREEN)
        input2_box.move_to(LEFT * 4 + DOWN * 0.2)

        self.play(
            FadeIn(input1_box, scale=0.5),
            FadeIn(input2_box, scale=0.5),
            FadeOut(central_pool),
            run_time=0.8
        )

        self.wait(0.3)

        # Add "Inputs", "Outputs", and "Fees" labels
        inputs_label = Text("Inputs", font_size=20, color=SYNTH_GREEN, weight=BOLD)
        inputs_label.move_to(LEFT * 4 + UP * 2.5)

        outputs_label = Text("Outputs", font_size=20, color=SYNTH_ORANGE, weight=BOLD)
        outputs_label.move_to(RIGHT * 4 + UP * 2.5)

        fees_label = Text("Fees", font_size=20, color=SYNTH_GOLD, weight=BOLD)
        fees_label.next_to(fee_box, LEFT, buff=0.5)

        self.play(
            Write(inputs_label),
            Write(outputs_label),
            Write(fees_label),
            run_time=0.8
        )

        self.wait(0.5)

        # Final summary
        final_text = Text(
            "Transaction: 0.85 BTC in → 0.84 BTC out + 0.01 BTC fee",
            font_size=22,
            color=SYNTH_GREEN
        )
        final_text.to_edge(DOWN).shift(UP * 0.5)

        self.play(
            Transform(explain, final_text),
            run_time=1
        )

        self.wait(2)

    def create_particles(self, center_pos, count):
        """Create small particle dots for flow animation"""
        particles = VGroup()
        for _ in range(count):
            # Create small glowing dots
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

        # Box around text
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


class SigningAndInputConstruction(Scene):
    """
    Signing & Input Construction (0:30-1:15)
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
            font_size=24,
            color=SYNTH_PEACH
        )
        description.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(description, shift=DOWN))
        self.wait(1)

        # Create the 2 UTXOs as simple rectangles
        utxo1 = self.create_simple_utxo("0.5 BTC", "abc123...def456", "#0")
        utxo1.move_to(LEFT * 3 + UP * 1)

        utxo2 = self.create_simple_utxo("0.35 BTC", "789ghi...jkl012", "#1")
        utxo2.move_to(RIGHT * 3 + UP * 1)

        self.play(
            FadeIn(utxo1, scale=0.8),
            FadeIn(utxo2, scale=0.8),
            run_time=0.8
        )
        self.wait(0.8)

        # === PRIVATE KEY INTRODUCTION ===
        private_key_text = Text(
            "Alice's private key proves she controls these funds",
            font_size=22,
            color=SYNTH_PURPLE
        )
        private_key_text.move_to(description)

        self.play(Transform(description, private_key_text))
        self.wait(0.3)

        # Show private key symbolically (glowing key with hex blur)
        private_key = self.create_private_key_visual()
        private_key.shift(DOWN * 0.5)

        self.play(FadeIn(private_key, scale=0.5), run_time=0.8)
        self.wait(0.5)

        # Derive public key
        public_key = self.create_public_key_visual()
        public_key.next_to(private_key, RIGHT, buff=2)

        derivation_arrow = Arrow(
            private_key.get_right(),
            public_key.get_left(),
            color=SYNTH_CYAN,
            buff=0.2,
            stroke_width=3
        )

        derivation_label = Text("ECDSA", font_size=16, color=SYNTH_CYAN)
        derivation_label.next_to(derivation_arrow, UP, buff=0.1)

        self.play(
            GrowArrow(derivation_arrow),
            FadeIn(derivation_label),
            run_time=0.6
        )
        self.play(FadeIn(public_key, scale=0.5), run_time=0.6)
        self.wait(0.8)

        # === SIGNATURE CREATION ===
        signing_text = Text(
            "Creating signatures to unlock each UTXO...",
            font_size=22,
            color=SYNTH_GOLD
        )
        signing_text.move_to(description)

        self.play(
            Transform(description, signing_text),
            FadeOut(derivation_arrow),
            FadeOut(derivation_label),
            run_time=0.8
        )
        self.wait(0.3)

        # Move keys to the side
        keys_group = VGroup(private_key, public_key)
        self.play(
            keys_group.animate.scale(0.6).to_edge(LEFT).shift(DOWN * 0.8),
            run_time=0.8
        )

        # Process first UTXO
        input1 = self.sign_utxo_and_create_input(utxo1, "abc123...def456", "0", keys_group)
        self.wait(0.5)

        # Process second UTXO
        input2 = self.sign_utxo_and_create_input(utxo2, "789ghi...jkl012", "1", keys_group)
        self.wait(0.5)

        # === INPUT ASSEMBLY ===
        assembly_text = Text(
            "These signed inputs will unlock 0.85 BTC",
            font_size=24,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        assembly_text.move_to(description)

        self.play(Transform(description, assembly_text))

        # Highlight both inputs
        self.play(
            input1[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            input2[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            run_time=0.8
        )
        self.wait(0.8)

        # Final caption
        ready_text = Text(
            "Now ready to construct the full transaction",
            font_size=22,
            color=SYNTH_CYAN
        )
        ready_text.to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(ready_text))
        self.wait(2)

    def create_simple_utxo(self, amount, txid, output):
        """Create a simple rectangular UTXO"""
        # Amount label
        amount_text = Text(amount, font_size=20, color=SYNTH_GREEN, weight=BOLD)

        # Transaction details
        txid_text = Text(txid, font_size=12, color=SYNTH_CYAN)
        output_text = Text(f"output {output}", font_size=12, color=SYNTH_CYAN)

        details = VGroup(txid_text, output_text).arrange(DOWN, buff=0.05)

        # Arrange everything
        labels = VGroup(amount_text, details).arrange(DOWN, buff=0.15)

        # Box around it
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
        """Create a visual representation of a private key"""
        # Key icon (simple key shape)
        key_circle = Circle(radius=0.3, color=SYNTH_PURPLE, stroke_width=3)
        key_circle.set_fill(color=SYNTH_PURPLE, opacity=0.3)

        key_shaft = Rectangle(
            width=0.6, height=0.15,
            color=SYNTH_PURPLE,
            stroke_width=3
        )
        key_shaft.set_fill(color=SYNTH_PURPLE, opacity=0.3)
        key_shaft.next_to(key_circle, RIGHT, buff=0)

        key_icon = VGroup(key_circle, key_shaft)

        # Label
        key_label = Text("Private Key", font_size=14, color=SYNTH_PURPLE, weight=BOLD)
        key_label.next_to(key_icon, DOWN, buff=0.2)

        # Hex representation (blurred for security)
        hex_text = Text("5Kb8...3Qm", font_size=10, color=SYNTH_PURPLE)
        hex_text.set_opacity(0.6)
        hex_text.next_to(key_label, DOWN, buff=0.1)

        return VGroup(key_icon, key_label, hex_text)

    def create_public_key_visual(self):
        """Create a visual representation of a public key"""
        # Public key icon (open lock or broadcast symbol)
        pub_circle = Circle(radius=0.35, color=SYNTH_CYAN, stroke_width=3)
        pub_circle.set_fill(color=SYNTH_CYAN, opacity=0.2)

        # Label
        pub_label = Text("Public Key", font_size=14, color=SYNTH_CYAN, weight=BOLD)
        pub_label.next_to(pub_circle, DOWN, buff=0.2)

        # Hex representation
        hex_text = Text("02a1b2...c3d4", font_size=10, color=SYNTH_CYAN)
        hex_text.set_opacity(0.7)
        hex_text.next_to(pub_label, DOWN, buff=0.1)

        return VGroup(pub_circle, pub_label, hex_text)

    def sign_utxo_and_create_input(self, utxo, txid, vout, keys_group):
        """Sign a UTXO and create the corresponding input"""
        # Show the locking script from the UTXO
        script_pubkey = self.create_script_box(
            "scriptPubKey",
            "OP_DUP OP_HASH160 <pubKeyHash>\nOP_EQUALVERIFY OP_CHECKSIG",
            SYNTH_ORANGE
        )
        script_pubkey.scale(0.7).next_to(utxo, DOWN, buff=0.4)

        self.play(FadeIn(script_pubkey, shift=UP * 0.2), run_time=0.5)
        self.wait(0.3)

        # Signature creation effect
        lightning = self.create_signature_effect()
        lightning.move_to(keys_group).shift(RIGHT * 0.5)

        self.play(Create(lightning), run_time=0.6)
        self.wait(0.2)
        self.play(FadeOut(lightning), run_time=0.3)

        # Create signature
        signature = self.create_signature_visual()
        signature.move_to(script_pubkey.get_center() + RIGHT * 2.5)

        self.play(FadeIn(signature, scale=0.5), run_time=0.5)
        self.wait(0.3)

        # Create the unlocking script (scriptSig)
        script_sig = self.create_script_box(
            "scriptSig",
            "<signature> <publicKey>",
            SYNTH_GOLD
        )
        script_sig.scale(0.7).next_to(signature, DOWN, buff=0.3)

        self.play(
            FadeIn(script_sig, shift=UP * 0.2),
            FadeOut(script_pubkey),
            FadeOut(signature),
            run_time=0.6
        )
        self.wait(0.3)

        # Build the input component
        input_component = self.create_input_box(txid, vout)
        input_component.move_to(utxo)

        self.play(
            Transform(utxo, input_component),
            FadeOut(script_sig),
            run_time=0.8
        )

        return utxo  # Return the transformed object

    def create_script_box(self, label, content, color):
        """Create a box showing a Bitcoin script"""
        label_text = Text(label, font_size=14, color=color, weight=BOLD)
        content_text = Text(content, font_size=10, color=color, font="Courier New")
        content_text.set_opacity(0.8)

        text_group = VGroup(label_text, content_text).arrange(DOWN, buff=0.1)

        box = SurroundingRectangle(
            text_group,
            color=color,
            stroke_width=1.5,
            buff=0.15,
            corner_radius=0.05
        )
        box.set_fill(color=color, opacity=0.1)

        return VGroup(box, text_group)

    def create_signature_effect(self):
        """Create a lightning/energy effect for signature generation"""
        lightning = VGroup()

        for i in range(4):
            angle = i * TAU / 4
            points = [
                ORIGIN,
                np.array([np.cos(angle) * 0.3, np.sin(angle) * 0.3, 0]),
                np.array([np.cos(angle) * 0.5, np.sin(angle) * 0.5, 0]),
            ]

            bolt = VMobject(color=SYNTH_GOLD, stroke_width=2)
            bolt.set_points_as_corners(points)
            bolt.set_stroke(opacity=0.8)
            lightning.add(bolt)

        return lightning

    def create_signature_visual(self):
        """Create a visual representation of a digital signature"""
        sig_text = Text("Signature", font_size=12, color=SYNTH_GOLD, weight=BOLD)
        hex_text = Text("304402...", font_size=10, color=SYNTH_GOLD, font="Courier New")

        sig_group = VGroup(sig_text, hex_text).arrange(DOWN, buff=0.05)

        # Glow box
        box = SurroundingRectangle(
            sig_group,
            color=SYNTH_GOLD,
            stroke_width=2,
            buff=0.1,
            corner_radius=0.05
        )
        box.set_fill(color=SYNTH_GOLD, opacity=0.25)

        return VGroup(box, sig_group)

    def create_input_box(self, txid, vout):
        """Create a transaction input box"""
        # Input components
        txid_label = Text(f"txid: {txid}", font_size=12, color=SYNTH_GREEN)
        vout_label = Text(f"vout: {vout}", font_size=12, color=SYNTH_GREEN)
        scriptsig_label = Text("scriptSig: <sig> <pubKey>", font_size=10, color=SYNTH_GOLD)
        scriptsig_label.set_opacity(0.8)
        sequence_label = Text("sequence: 0xffffffff", font_size=10, color=SYNTH_GREEN)
        sequence_label.set_opacity(0.7)

        input_data = VGroup(
            txid_label, vout_label, scriptsig_label, sequence_label
        ).arrange(DOWN, buff=0.08, aligned_edge=LEFT)

        # Box around input
        box = SurroundingRectangle(
            input_data,
            color=SYNTH_GREEN,
            stroke_width=2,
            buff=0.2,
            corner_radius=0.1
        )
        box.set_fill(color=SYNTH_GREEN, opacity=0.15)

        return VGroup(box, input_data)


class TransactionConstruction(Scene):
    """
    Transaction Construction (1:15-1:45)
    Shows the transaction being built as a data packet.
    """

    def construct(self):
        self.camera.background_color = SYNTH_BG

        # Scene title (no "Act" label)
        title = Text("Transaction Construction", font_size=38, color=SYNTH_CYAN)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # Continuity description
        description = Text(
            "Alice's wallet constructs a transaction to broadcast to the Bitcoin network",
            font_size=24,
            color=SYNTH_PEACH
        )
        description.next_to(title, DOWN, buff=0.5)
        self.play(FadeIn(description, shift=DOWN))
        self.wait(1)

        # Fade out description before showing blocks
        self.play(FadeOut(description))
        self.wait(0.3)

        # Define transaction components (in order from top to bottom when stacked)
        # Reflecting actual Bitcoin transaction structure
        components_data = [
            {"label": "Version", "sublabel": "version: 2", "color": SYNTH_CYAN, "height": 0.6},
            {"label": "Input Count", "sublabel": "2 inputs", "color": SYNTH_CYAN, "height": 0.5},
            {"label": "Inputs", "sublabel": "2 signed UTXOs", "color": SYNTH_GREEN, "height": 1.3},
            {"label": "Output Count", "sublabel": "2 outputs", "color": SYNTH_CYAN, "height": 0.5},
            {"label": "Outputs", "sublabel": "0.7 BTC (Bob), 0.14 BTC (change)", "color": SYNTH_ORANGE, "height": 1.3},
            {"label": "Locktime", "sublabel": "0 (immediate)", "color": SYNTH_CYAN, "height": 0.6},
        ]

        # Build transaction by animating blocks falling upwards from bottom
        # They will stack in order with Header at top
        transaction_blocks = VGroup()
        block_objects = []

        # Calculate total height to center the final structure
        total_height = sum(comp["height"] for comp in components_data) + 0.2 * (len(components_data) - 1)
        start_y = total_height / 2

        current_y = start_y

        for i, comp in enumerate(components_data):
            # Create block below screen
            block = self.create_transaction_block(
                comp["label"],
                comp["sublabel"],
                comp["color"],
                height=comp["height"]
            )

            # Position for final stacked structure
            final_y = current_y - comp["height"] / 2

            # Start position (below screen)
            block.move_to(DOWN * 5)

            # Add to scene and store
            transaction_blocks.add(block)
            block_objects.append({"block": block, "data": comp, "y": final_y})

            # Animate block rising from bottom with slight rotation
            self.play(
                block.animate.move_to(UP * final_y).rotate(0),
                rate_func=rate_functions.ease_out_bounce,
                run_time=0.8
            )

            # Play a subtle "snap" effect
            self.play(
                block.animate.scale(1.05),
                run_time=0.1
            )
            self.play(
                block.animate.scale(1/1.05),
                run_time=0.1
            )

            self.wait(0.2)

            # Update position for next block
            current_y -= (comp["height"] + 0.2)

        self.wait(0.5)

        # Add arrows and labels pointing to each block
        annotations = VGroup()
        for i, block_obj in enumerate(block_objects):
            block = block_obj["block"]
            comp = block_obj["data"]

            # Create detailed label
            label_group = self.create_component_label(
                comp["label"],
                comp["sublabel"],
                comp["color"]
            )
            label_group.next_to(block, RIGHT, buff=1.5)

            # Arrow from block to label
            arrow = Arrow(
                block.get_right(),
                label_group.get_left(),
                color=comp["color"],
                buff=0.1,
                stroke_width=2,
                max_tip_length_to_length_ratio=0.15
            )

            annotations.add(VGroup(arrow, label_group))

            # Animate label appearing
            self.play(
                GrowArrow(arrow),
                FadeIn(label_group, shift=LEFT * 0.3),
                run_time=0.5
            )
            self.wait(0.2)

        self.wait(0.8)

        # Explain the fee calculation
        fee_text = Text(
            "Fee = Inputs (0.85 BTC) - Outputs (0.84 BTC) = 0.01 BTC",
            font_size=20,
            color=SYNTH_GOLD
        )
        fee_text.to_edge(DOWN).shift(UP * 0.5)

        self.play(Write(fee_text))
        self.wait(1.2)

        # Highlight inputs block
        inputs_block = block_objects[2]["block"]  # Inputs is the 3rd block (index 2)
        self.play(
            inputs_block[0].animate.set_stroke(color=SYNTH_GOLD, width=3),
            run_time=0.5
        )
        self.wait(0.3)

        # Highlight outputs block
        outputs_block = block_objects[4]["block"]  # Outputs is the 5th block (index 4)
        self.play(
            inputs_block[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            outputs_block[0].animate.set_stroke(color=SYNTH_GOLD, width=3),
            run_time=0.5
        )
        self.wait(0.8)

        # Transaction ready
        ready_text = Text(
            "Transaction complete and ready to broadcast!",
            font_size=24,
            color=SYNTH_GREEN,
            weight=BOLD
        )
        ready_text.move_to(fee_text)

        self.play(
            Transform(fee_text, ready_text),
            outputs_block[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
            run_time=1
        )

        # Highlight entire transaction structure with glow
        for block_obj in block_objects:
            block = block_obj["block"]
            self.play(
                block[0].animate.set_stroke(color=SYNTH_GREEN, width=3),
                run_time=0.3
            )

        # Final glow effect on all blocks
        self.play(
            *[block_obj["block"][0].animate.set_fill(opacity=0.3) for block_obj in block_objects],
            run_time=0.5
        )
        self.play(
            *[block_obj["block"][0].animate.set_fill(opacity=0.15) for block_obj in block_objects],
            run_time=0.5
        )

        self.wait(2)

    def create_transaction_block(self, label, sublabel, color, height=1.0):
        """Create a simple rectangular block for transaction components"""
        width = 3.5

        # Main rectangular block with rounded corners
        block_rect = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.1,
            color=color,
            stroke_width=3
        )
        block_rect.set_fill(color=color, opacity=0.15)

        # Label text inside block
        label_text = Text(label, font_size=28, color=color, weight=BOLD)
        sublabel_text = Text(sublabel, font_size=16, color=color)
        sublabel_text.set_opacity(0.8)

        text_group = VGroup(label_text, sublabel_text).arrange(DOWN, buff=0.1)
        text_group.move_to(block_rect)

        return VGroup(block_rect, text_group)

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
