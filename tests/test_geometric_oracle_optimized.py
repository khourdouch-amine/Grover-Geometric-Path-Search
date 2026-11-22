import numpy as np
import pytest

from qiskit import QuantumCircuit, QuantumRegister
from qiskit.quantum_info import Statevector

from planners.quantum.grover_global.geometric_oracle import (
    build_geometric_phase_oracle as build_reference,
)
from planners.quantum.grover_global.geometric_oracle_optimized import (
    build_geometric_phase_oracle as build_optimized,
    _compute_invalid_flag,
    _uncompute_invalid_flag,
)


def test_optimized_invalid_flag_exhaustive_and_reversible():
    obstacles = {(1, 0), (2, 1)}

    x = QuantumRegister(3, "x")
    y = QuantumRegister(3, "y")
    flag = QuantumRegister(1, "flag")
    ancilla = QuantumRegister(1, "ancilla")
    qc = QuantumCircuit(x, y, flag, ancilla)

    for px in range(8):
        for py in range(8):
            test = QuantumCircuit(x, y, flag, ancilla)

            for bit in range(3):
                if (px >> bit) & 1:
                    test.x(x[bit])
                if (py >> bit) & 1:
                    test.x(y[bit])

            _compute_invalid_flag(
                test, list(x), list(y), flag[0],
                4, 4, obstacles, ancilla[0],
            )

            state = Statevector.from_instruction(test)
            probabilities = state.probabilities()
            measured_index = int(np.argmax(probabilities))

            expected_invalid = (
                px >= 4 or py >= 4 or (px, py) in obstacles
            )
            expected_flag = int(expected_invalid)

            assert probabilities[measured_index] == pytest.approx(1.0)
            assert ((measured_index >> 6) & 1) == expected_flag
            assert ((measured_index >> 7) & 1) == 0

            _uncompute_invalid_flag(
                test, list(x), list(y), flag[0],
                4, 4, obstacles, ancilla[0],
            )

            final_state = Statevector.from_instruction(test)
            final_probabilities = final_state.probabilities()
            final_index = int(np.argmax(final_probabilities))

            expected_index = px | (py << 3)
            assert final_probabilities[final_index] == pytest.approx(1.0)
            assert final_index == expected_index


def test_optimized_oracle_matches_reference_on_superposition():
    params = dict(
        width=4,
        height=4,
        start=(0, 0),
        goal=(3, 3),
        obstacles={(1, 0), (2, 1)},
        route_length=2,
    )

    reference = build_reference(**params)
    optimized = build_optimized(**params)

    assert reference.num_qubits == optimized.num_qubits

    route_qubits = 2 * params["route_length"]
    phase_qubit = reference.num_qubits - 1

    initial = QuantumCircuit(reference.num_qubits)
    initial.h(range(route_qubits))
    initial.x(phase_qubit)
    initial.h(phase_qubit)

    reference_state = Statevector.from_instruction(
        initial.compose(reference)
    )
    optimized_state = Statevector.from_instruction(
        initial.compose(optimized)
    )

    fidelity = abs(np.vdot(
        reference_state.data,
        optimized_state.data,
    )) ** 2

    assert fidelity == pytest.approx(1.0, abs=1e-10)
