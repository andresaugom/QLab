from python.core.qubit import Qubit
from python.core.gates import X, Y, Z, H, Rz, Ry, Rx

import numpy as np

class BlochAPI:
    def __init__(self):
        self.qubit = Qubit(np.array([1, 0], dtype=complex))
    
    def state_vector(self):
        return self.qubit.state_vector()
    
    def apply_gate(self, gate_name, theta=0):
        gates = {
            "X": X(),
            "Y": Y(),
            "Z": Z(),
            "H": H(),
            "Rx": Rx(theta),
            "Ry": Ry(theta),
            "Rz": Rz(theta)
        }
        op = gates[gate_name]
        self.qubit.apply_gate(op)

    def measure(self):
        return self.qubit.measure()