from core.system import System
from core.operator import Hamiltonian
from core.solver import ExpmSolver

import numpy as np

psi0 = np.array([1, 0], dtype=complex)

print ("Initial state:", psi0)

H = Hamiltonian(np.array([[0, 1],
                          [1, 0]], dtype=complex))

solver = ExpmSolver()
system = System(psi0, H, solver)

psi_t = system.evolve(np.pi / 2)
print ("Final state:", psi_t)

