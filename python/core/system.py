import numpy as np
from python.core.solver import Solver
from python.core.operator import Hamiltonian

class System:
    """
    Represents a quantum system with a state vector (psi) evolving under a Hamiltonian.
    """

    def __init__(self, psi: np.ndarray, hamiltonian: Hamiltonian, solver: Solver):
        if psi.ndim != 1:
            raise ValueError("State vector must be 1D.")
        if not np.isclose(np.linalg.norm(psi), 1):
            psi = psi / np.linalg.norm(psi)

        self.psi = psi.astype(complex)
        self.hamiltonian = hamiltonian
        self.solver = solver

    def apply_global_op(self, op):
        """Applies an operator to the entire system state."""
        self.psi = op @ self.psi

    def apply_local_op(self, op, target: int, total_qubits: int):
        """Applies a local operator to a specific qubit in the full tensor state."""
        I = np.eye(2, dtype=complex)
        ops = [I] * total_qubits
        ops[target] = op
        full_op = ops[0]
        for o in ops[1:]:
            full_op = np.kron(full_op, o)
        self.apply_global_op(full_op)

    def evolve(self, t: float):
        """Evolves the system in time using the assigned solver."""
        self.psi = self.solver.evolve(self.psi, self.hamiltonian, t)
        return self.psi

    def state_vector(self):
        """Returns the current state vector of the system."""
        return self.psi
        