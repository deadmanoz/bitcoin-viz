"""
Bitcoin Vehicle Intro - Proof of Concept
=========================================

This animation demonstrates the core concept: visualizing Bitcoin Core
as a vehicle, then peeling back layers to reveal the technical components.

Inspired by 3Blue1Brown's visual storytelling approach.
"""

from manim import *

class BitcoinVehicleIntro(Scene):
    """
    POC animation showing:
    1. Title introduction
    2. Simple vehicle representation (car shape)
    3. Transformation to Bitcoin Core components
    4. Brief explanation of each subsystem
    """

    def construct(self):
        # === Part 1: Title Introduction ===
        title = Text("Understanding Bitcoin Core", font_size=48)
        subtitle = Text(
            "Peeling back the layers of abstraction",
            font_size=28,
            color=GRAY
        )
        subtitle.next_to(title, DOWN)

        self.play(Write(title))
        self.play(FadeIn(subtitle, shift=UP))
        self.wait(1)
        self.play(FadeOut(title), FadeOut(subtitle))

        # === Part 2: Vehicle Metaphor ===
        vehicle_title = Text("Think of Bitcoin Core as a Vehicle", font_size=36)
        vehicle_title.to_edge(UP)

        # Simple car shape using basic shapes
        car_body = Rectangle(
            height=1.5,
            width=3.5,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_width=3
        )
        car_top = Rectangle(
            height=0.8,
            width=2,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_width=3
        ).move_to(car_body.get_top() + UP * 0.4)

        # Wheels
        wheel1 = Circle(radius=0.4, fill_color=DARK_GRAY, fill_opacity=1)
        wheel1.move_to(car_body.get_bottom() + LEFT * 1.2 + DOWN * 0.2)
        wheel2 = Circle(radius=0.4, fill_color=DARK_GRAY, fill_opacity=1)
        wheel2.move_to(car_body.get_bottom() + RIGHT * 1.2 + DOWN * 0.2)

        vehicle = VGroup(car_body, car_top, wheel1, wheel2)

        self.play(Write(vehicle_title))
        self.play(DrawBorderThenFill(vehicle))
        self.wait(1)

        # === Part 3: Component Labels ===
        component_text = Text(
            "But what's under the hood?",
            font_size=32,
            color=YELLOW
        )
        component_text.next_to(vehicle, DOWN, buff=1)

        self.play(Write(component_text))
        self.wait(1)

        # === Part 4: Transformation to Components ===
        self.play(
            FadeOut(vehicle_title),
            FadeOut(component_text),
            vehicle.animate.scale(0.5).to_edge(LEFT)
        )

        # Create component labels mapped to vehicle parts
        components = [
            ("Consensus Engine", BLUE, "Engine"),
            ("P2P Network", GREEN, "Transmission"),
            ("UTXO Set", ORANGE, "Fuel System"),
            ("Mempool", RED, "Exhaust"),
        ]

        component_vgroup = VGroup()
        arrows = VGroup()

        for i, (name, color, analogy) in enumerate(components):
            # Component box
            box = Rectangle(
                height=0.7,
                width=3.5,
                fill_color=color,
                fill_opacity=0.3,
                stroke_color=color,
                stroke_width=2
            )

            # Component text
            comp_name = Text(name, font_size=24, color=WHITE)
            comp_analogy = Text(f"({analogy})", font_size=18, color=GRAY)
            comp_text = VGroup(comp_name, comp_analogy).arrange(DOWN, buff=0.1)
            comp_text.move_to(box)

            component = VGroup(box, comp_text)
            component.move_to(RIGHT * 2.5 + UP * 2 + DOWN * i * 1.2)

            # Arrow from vehicle to component
            arrow = Arrow(
                vehicle.get_right(),
                component.get_left(),
                color=color,
                buff=0.2,
                stroke_width=2
            )

            component_vgroup.add(component)
            arrows.add(arrow)

        # Animate components appearing one by one
        for i, (component, arrow) in enumerate(zip(component_vgroup, arrows)):
            self.play(
                GrowArrow(arrow),
                FadeIn(component, shift=LEFT),
                run_time=0.7
            )
            self.wait(0.3)

        self.wait(1)

        # === Part 5: Transaction Flow Teaser ===
        flow_title = Text(
            "Let's follow a transaction...",
            font_size=32,
            color=YELLOW
        )
        flow_title.to_edge(DOWN)

        # Create a small "transaction" dot
        tx_dot = Dot(color=YELLOW, radius=0.15)
        tx_dot.move_to(vehicle.get_right())

        self.play(Write(flow_title))
        self.play(FadeIn(tx_dot, scale=0.5))

        # Animate transaction flowing through components
        for i in range(len(component_vgroup)):
            self.play(
                tx_dot.animate.move_to(component_vgroup[i].get_center()),
                component_vgroup[i][0].animate.set_fill(opacity=0.6),
                run_time=0.6
            )
            self.wait(0.2)
            self.play(
                component_vgroup[i][0].animate.set_fill(opacity=0.3),
                run_time=0.3
            )

        # Transaction confirmed!
        confirmed = Text("✓ Confirmed!", font_size=36, color=GREEN)
        confirmed.next_to(tx_dot, RIGHT)
        self.play(
            FadeIn(confirmed, shift=LEFT),
            tx_dot.animate.set_color(GREEN).scale(1.5)
        )

        self.wait(2)

        # === Part 6: Ending ===
        end_text = VGroup(
            Text("Coming soon:", font_size=32),
            Text("Deep dives into each component", font_size=28, color=GRAY),
        ).arrange(DOWN, buff=0.3)

        self.play(
            FadeOut(vehicle),
            FadeOut(component_vgroup),
            FadeOut(arrows),
            FadeOut(tx_dot),
            FadeOut(confirmed),
            FadeOut(flow_title),
        )

        self.play(Write(end_text))
        self.wait(2)
        self.play(FadeOut(end_text))


class TransactionJourney(Scene):
    """
    A more detailed look at a transaction's journey through Bitcoin Core.
    This demonstrates the potential for future episodes.
    """

    def construct(self):
        title = Text("Transaction Journey", font_size=42)
        title.to_edge(UP)
        self.play(Write(title))

        # Create a visual representation of the transaction lifecycle
        stages = [
            ("Created", BLUE),
            ("Validated", GREEN),
            ("Broadcasted", YELLOW),
            ("Mempool", ORANGE),
            ("Mined", PURPLE),
            ("Confirmed", GREEN),
        ]

        stage_dots = VGroup()
        stage_labels = VGroup()

        # Arrange stages in a circular flow
        radius = 2.5
        for i, (stage_name, color) in enumerate(stages):
            angle = i * TAU / len(stages) - PI/2  # Start from top

            # Create dot for stage
            dot = Dot(
                point=np.array([
                    radius * np.cos(angle),
                    radius * np.sin(angle),
                    0
                ]),
                color=color,
                radius=0.2
            )

            # Create label
            label = Text(stage_name, font_size=24, color=color)
            label.next_to(dot, direction=dot.get_center()/np.linalg.norm(dot.get_center()), buff=0.3)

            stage_dots.add(dot)
            stage_labels.add(label)

        # Draw the cycle
        self.play(Create(stage_dots), Write(stage_labels))

        # Create arrows between stages
        arrows = VGroup()
        for i in range(len(stage_dots)):
            next_i = (i + 1) % len(stage_dots)
            arrow = CurvedArrow(
                stage_dots[i].get_center(),
                stage_dots[next_i].get_center(),
                color=GRAY,
                angle=-TAU/len(stages),
            )
            arrows.add(arrow)

        self.play(Create(arrows))

        # Animate a transaction moving through the cycle
        tx = Dot(color=YELLOW, radius=0.25)
        tx.move_to(stage_dots[0])
        self.play(FadeIn(tx, scale=0.3))

        for i in range(len(stage_dots) * 2):  # Go around twice
            next_i = (i + 1) % len(stage_dots)
            self.play(
                MoveAlongPath(tx, arrows[i % len(arrows)]),
                stage_dots[next_i].animate.scale(1.5),
                run_time=0.7
            )
            self.play(stage_dots[next_i].animate.scale(1/1.5), run_time=0.3)

        self.wait(1)

        # Final message
        final_text = Text(
            "Each stage reveals deeper complexity",
            font_size=28,
            color=GRAY
        )
        final_text.to_edge(DOWN)

        self.play(Write(final_text))
        self.wait(2)
