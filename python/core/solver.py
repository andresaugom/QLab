import numpy as np
from scipy.linalg import expm

class Solver:
    """Abstract solver interface."""

    def evolve(self, psi: np.ndarray, hamiltonian, t: float) -> np.ndarray:
        raise NotImplementedError


class ExpmSolver(Solver):
    """Matrix exponential solver using SciPy."""

    def evolve(self, psi: np.ndarray, hamiltonian, t: float, planck_const=1.0) -> np.ndarray:
        U = expm(-1j * hamiltonian.op * t / planck_const)
        return U @ psi
