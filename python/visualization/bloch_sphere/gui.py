# gui.py  -- VPython Bloch GUI (fixed + improved)
import numpy as np
from vpython import (
    canvas, scene, vector, arrow, sphere, color,
    button, menu, slider, wtext, rate
)

from python.visualization.bloch_sphere.bloch_api import BlochAPI


class BlochGUI:
    def __init__(self):
        self.api = BlochAPI()
        self.setup_scene()
        self.setup_controls()
        # initial draw
        self.update_visualization()

    def setup_scene(self):
        """Set up the 3D canvas and the sphere objects."""
        self.canvas = canvas(title='Bloch Sphere Simulator', width=800, height=600)
        scene.range = 1.3

        # translucent sphere + axes
        sphere(radius=1, opacity=0.12, color=color.white)
        arrow(axis=vector(1.2, 0, 0), color=color.red, shaftwidth=0.01)
        arrow(axis=vector(0, 1.2, 0), color=color.green, shaftwidth=0.01)
        arrow(axis=vector(0, 0, 1.2), color=color.blue, shaftwidth=0.01)

        # dynamic Bloch vector
        self.bloch_vector = arrow(
            axis=vector(0, 0, 1),
            color=color.cyan,
            shaftwidth=0.04
        )

    def setup_controls(self):
        """Set up the GUI widgets (buttons, sliders, etc.)."""
        # Put widgets under the canvas caption area
        self.canvas.append_to_caption('\n\n')

        # State text (will be updated)
        self.state_text = wtext(text="|ψ⟩ = [1.00+0.00j, 0.00+0.00j]")
        self.canvas.append_to_caption('\n\n')

        # Gate menu: bind callback receives a single object (menu)
        self.gate_menu = menu(
            choices=["X", "Y", "Z", "H", "Rx", "Ry", "Rz"],
            selected="H",
            bind=self.on_gate_select
        )
        self.canvas.append_to_caption('  ')

        # Buttons
        button(text="Apply Gate", bind=self.apply_gate_callback)
        self.canvas.append_to_caption('  ')
        button(text="Measure", bind=self.measure_callback)
        self.canvas.append_to_caption('\n\n')

        # Theta slider must include bind at construction time
        self.theta_slider = slider(
            min=0,
            max=2 * np.pi,
            step=0.01,
            value=0,
            length=300,
            disabled=True,
            bind=self.on_slider_change
        )
        # text showing numeric theta
        self.theta_text = wtext(text=f"    Theta (for rotations): {self.theta_slider.value:.2f}")

    # ---------------- widget callbacks ----------------
    def on_gate_select(self, menu_obj):
        """Triggered when the user changes the gate in the menu."""
        # menu_obj.selected is current selection in VPython
        selected_gate = menu_obj.selected
        if selected_gate in ["Rx", "Ry", "Rz"]:
            self.theta_slider.disabled = False
        else:
            self.theta_slider.disabled = True
            # reset display maybe
            self.theta_slider.value = 0
            self.theta_text.text = f"    Theta (for rotations): {self.theta_slider.value:.2f}"

    def on_slider_change(self, slider_obj):
        """Triggered when the user moves the slider."""
        self.theta_text.text = f"    Theta (for rotations): {slider_obj.value:.2f}"

    def apply_gate_callback(self, btn):
        """Called when the 'Apply Gate' button is pressed."""
        gate = self.gate_menu.selected
        theta = self.theta_slider.value

        # Debug print (optional)
        print(f"[GUI] Apply gate {gate} theta={theta:.3f}")

        if gate in ["Rx", "Ry", "Rz"]:
            self.api.apply_gate(gate, theta)
        else:
            self.api.apply_gate(gate)

        # Immediately reflect change
        self.update_visualization()

    def measure_callback(self, btn):
        """Called when the 'Measure' button is pressed."""
        result = self.api.measure()
        self.state_text.text = f"** Measured: |{result}⟩ **"
        # After measurement update Bloch vector (collapsed state)
        self.update_visualization()

    # ---------------- visualization logic ----------------
    def update_visualization(self):
        """
        Retrieves the state from the backend (API) and updates
        both the 3D vector and the state text.
        """
        psi = self.api.state_vector()
        # Ensure psi is a length-2 complex array (single qubit)
        psi = np.asarray(psi, dtype=complex).flatten()
        if psi.shape[0] != 2:
            # fallback: don't update if not a single-qubit state
            self.state_text.text = "Non single-qubit state (can't plot)"
            return

        a, b = psi[0], psi[1]

        # Display state robustly (real+imag explicit)
        def fmt(c):
            return f"{c.real:.2f}{c.imag:+.2f}j"
        self.state_text.text = f"|ψ⟩ = [{fmt(a)}, {fmt(b)}]"

        # Compute Bloch spherical coords
        # theta = 2 * arccos(|a|)
        abs_a = np.clip(np.abs(a), 0.0, 1.0)
        theta = 2.0 * np.arccos(abs_a)
        # phi is relative phase between b and a
        # handle edge cases where amplitude is ~0
        if np.isclose(abs_a, 0.0) and np.isclose(np.abs(b), 0.0):
            phi = 0.0
        elif np.isclose(abs_a, 0.0):
            # a ~ 0 => global phase ambiguous; use phase of b
            phi = np.angle(b)
        else:
            phi = (np.angle(b) - np.angle(a))

        # Map to Cartesian coords on unit sphere
        x = np.sin(theta) * np.cos(phi)
        y = np.sin(theta) * np.sin(phi)
        z = np.cos(theta)

        # Update arrow safely (VPython accepts vector)
        self.bloch_vector.axis = vector(float(x), float(y), float(z))

    # ---------------- run loop ----------------
def main():
    gui = BlochGUI()

    # continuous update loop (keeps VPython responsive and reflects external changes)
    while True:
        rate(60)               # 60 FPS cap
        gui.update_visualization()


if __name__ == "__main__":
    main()
