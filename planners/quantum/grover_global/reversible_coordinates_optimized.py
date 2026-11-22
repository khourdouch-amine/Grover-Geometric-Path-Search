"""Experimental reversible coordinate arithmetic optimization."""

from qiskit import QuantumCircuit


def controlled_increment_optimized(qc, register, controls, ctrl_state):
    """Conditionally increment a little-endian register."""
    for bit in reversed(range(len(register))):
        if bit == 0:
            qc.mcx(controls, register[bit], ctrl_state=ctrl_state)
        else:
            lower = list(register[:bit])
            combined = list(controls) + lower
            lower_state = (1 << bit) - 1
            state = ctrl_state | (lower_state << len(controls))
            qc.mcx(combined, register[bit], ctrl_state=state)


def controlled_decrement_optimized(qc, register, controls, ctrl_state):
    """Conditionally decrement a little-endian register."""
    for bit in reversed(range(len(register))):
        if bit == 0:
            qc.mcx(controls, register[bit], ctrl_state=ctrl_state)
        else:
            lower = list(register[:bit])
            combined = list(controls) + lower
            qc.mcx(combined, register[bit], ctrl_state=ctrl_state)


def apply_reversible_move_optimized(qc, direction_bits, x_register, y_register):
    """Apply one reversible cardinal movement."""
    controlled_increment_optimized(qc, x_register, direction_bits, 0)
    controlled_decrement_optimized(qc, y_register, direction_bits, 1)
    controlled_decrement_optimized(qc, x_register, direction_bits, 2)
    controlled_increment_optimized(qc, y_register, direction_bits, 3)
