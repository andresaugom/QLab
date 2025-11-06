import numpy as np
from scipy.linalg import expm

class Operator:
    """Represents a general linear operator acting on a quantum state."""

    def __init__(self, op: np.ndarray):
        self.op = np.array(op, dtype=complex)

    def __call__(self):
        """Return the underlying array when the instance is called."""
        return self.op

    def __repr__(self):
        return repr(self.op)

    def __str__(self):
        return str(self.op)
    
    __array_priority__ = 1000

    @property
    def shape(self):
        return self.op.shape

    def _coerce_other_op(self, other):
        """Return underlying ndarray if other is Operator, else other unchanged."""
        return other.op if isinstance(other, Operator) else other

    def __matmul__(self, other):
        """Matrix multiply: Operator @ Operator -> Operator, Operator @ array -> array."""
        other_val = self._coerce_other_op(other)
        if isinstance(other_val, np.ndarray):
            res = self.op @ other_val
            return Operator(res) if isinstance(other, Operator) else res
        raise TypeError(f"Unsupported operand type(s) for @: 'Operator' and '{type(other).__name__}'")

    def __rmatmul__(self, other):
        """array @ Operator -> array, Operator @ Operator handled by __matmul__."""
        if isinstance(other, np.ndarray):
            return other @ self.op
        raise TypeError(f"Unsupported operand type(s) for @: '{type(other).__name__}' and 'Operator'")

    def __mul__(self, other):
        """If other is an Operator, do composition (matrix multiply).
           If other is a scalar, scale the operator.
           If other is an ndarray, apply operator to array (matrix multiply)."""
        other_val = self._coerce_other_op(other)
        if np.isscalar(other_val):
            return Operator(self.op * other_val)
        if isinstance(other_val, np.ndarray):
            res = self.op @ other_val
            return Operator(res) if isinstance(other, Operator) else res
        raise TypeError(f"Unsupported operand type(s) for *: 'Operator' and '{type(other).__name__}'")

    def __rmul__(self, other):
        """Scalar * Operator or array @ Operator (when array is on left)."""
        if np.isscalar(other):
            return Operator(self.op * other)
        if isinstance(other, np.ndarray):
            return other @ self.op
        raise TypeError(f"Unsupported operand type(s) for *: '{type(other).__name__}' and 'Operator'")

    def __add__(self, other):
        other_val = self._coerce_other_op(other)
        if isinstance(other_val, np.ndarray):
            return Operator(self.op + other_val)
        raise TypeError(f"Unsupported operand type(s) for +: 'Operator' and '{type(other).__name__}'")

    def __sub__(self, other):
        other_val = self._coerce_other_op(other)
        if isinstance(other_val, np.ndarray):
            return Operator(self.op - other_val)
        raise TypeError(f"Unsupported operand type(s) for -: 'Operator' and '{type(other).__name__}'")

    def __neg__(self):
        return Operator(-self.op)

    def __eq__(self, other):
        if not isinstance(other, Operator):
            return False
        return np.allclose(self.op, other.op, atol=1e-10)

    def dagger(self):
        """Returns the Hermitian conjugate (adjoint) of the operator."""
        return Operator(self.op.conj().T)

    def is_hermitian(self, tol=1e-10):
        """Checks if the operator is Hermitian."""
        return np.allclose(self.op, self.op.conj().T, atol=tol)

    def is_unitary(self, tol=1e-10):
        """Checks if the operator is unitary."""
        I = np.eye(self.op.shape[0])
        return np.allclose(self.op.conj().T @ self.op, I, atol=tol)


class Hamiltonian(Operator):
    """Hamiltonian operator governing time evolution."""

    def evolve(self, psi, t: float, planck_const=1.0):
        """Applies time evolution U(t) = exp(-iHt/planck_const)."""
        U = expm(-1j * self.op * t / planck_const)
        return U @ psi
