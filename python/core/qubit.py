# qubih 🥀

from python.core.system import System
import numpy as np

class Qubit(System):
    def __init__(self, psi=np.array([1, 0], dtype=complex)):
        super().__init__(psi=psi, hamiltonian=None, solver=None)

    def apply_gate(self, gate):
        """Applies a quantum gate (operator) to the qubit."""
        self.apply_global_op(gate)
        return self.psi
    
    def measure(self):
        """Simulates a measurement of the qubit in the computational basis."""
        probabilities = np.abs(self.psi)**2
        outcome = np.random.choice([0, 1], p=probabilities)
        # Collapse the state
        collapsed_state = np.zeros_like(self.psi)
        collapsed_state[outcome] = 1.0
        self.psi = collapsed_state
        return outcome
