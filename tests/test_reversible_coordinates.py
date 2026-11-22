import numpy as np
from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector

from planners.quantum.grover_global.reversible_coordinates import (
    apply_reversible_move,
    controlled_increment,
    controlled_decrement,
)


def run_basis_circuit(qc):
    state = Statevector.from_instruction(qc)
    probabilities = np.abs(state.data) ** 2
    return int(np.argmax(probabilities))


def test_controlled_increment_and_decrement_are_exact_inverses():
    for width in (2, 3):
        for value in range(1 << width):
            control = QuantumRegister(2, "control")
            coord = QuantumRegister(width, "coord")
            qc = QuantumCircuit(control, coord)

            qc.x(control[0])

            for bit in range(width):
                if (value >> bit) & 1:
                    qc.x(coord[bit])

            controlled_increment(qc, list(coord), list(control), 0)
            controlled_decrement(qc, list(coord), list(control), 0)

            index = run_basis_circuit(qc)
            actual_control = index & 0b11
            actual_coord = (index >> 2) & ((1 << width) - 1)

            assert actual_control == 0b01
            assert actual_coord == value


def test_reversible_move_and_inverse_restore_coordinates():
    for x_value in range(8):
        for y_value in range(8):
            for direction in range(4):
                route = QuantumRegister(2, "route")
                x = QuantumRegister(3, "x")
                y = QuantumRegister(3, "y")
                qc = QuantumCircuit(route, x, y)

                for bit in range(3):
                    if (x_value >> bit) & 1:
                        qc.x(x[bit])
                    if (y_value >> bit) & 1:
                        qc.x(y[bit])

                for bit in range(2):
                    if (direction >> bit) & 1:
                        qc.x(route[bit])

                apply_reversible_move(qc, list(route), list(x), list(y))

                # Exact inverse of the four controlled operations.
                from planners.quantum.grover_global.reversible_coordinates import (
                    controlled_increment,
                    controlled_decrement,
                )

                controlled_increment(qc, list(x), list(route), 2)
                controlled_decrement(qc, list(y), list(route), 3)
                controlled_decrement(qc, list(x), list(route), 0)
                controlled_increment(qc, list(y), list(route), 1)

                index = run_basis_circuit(qc)
                actual_route = index & 0b11
                actual_x = (index >> 2) & 0b111
                actual_y = (index >> 5) & 0b111

                assert actual_route == direction
                assert actual_x == x_value
                assert actual_y == y_value
