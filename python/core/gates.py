from .operator import Operator
import numpy as np

def X():
    return Operator(np.array([[0, 1],
                               [1, 0]], dtype=complex))
def Y():
    return Operator(np.array([[0, -1j],
                               [1j, 0]], dtype=complex))
def Z():
    return Operator(np.array([[1, 0],
                               [0, -1]], dtype=complex))
def Rx(theta):
    return Operator(np.array([[np.cos(theta/2), -1j*np.sin(theta/2)],
                               [-1j*np.sin(theta/2), np.cos(theta/2)]], dtype=complex))
def Ry(theta):
    return Operator(np.array([[np.cos(theta/2), -np.sin(theta/2)],
                               [np.sin(theta/2), np.cos(theta/2)]], dtype=complex))
def Rz(theta):
    return Operator(np.array([[np.exp(-1j*theta/2), 0],
                               [0, np.exp(1j*theta/2)]], dtype=complex))
def H():
    return Operator((1/np.sqrt(2)) * np.array([[1, 1],
                                               [1, -1]], dtype=complex))