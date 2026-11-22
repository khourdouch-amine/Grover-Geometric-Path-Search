# Grover Geometric Path Search

A research codebase for reversible geometric oracles and Grover-based
fixed-length path search in obstacle-constrained grid mazes.

## Research objective

This project investigates the construction of a reversible geometric
phase oracle for fixed-length paths in a two-dimensional grid maze.

It includes classical reference algorithms, route encodings,
reversible coordinate operations, geometric oracle circuits,
and benchmark results.

The main study scenario is **G3 (4x4 grid, path length 6)**.

## G3 benchmark scenario

| Parameter | Value |
|---|---:|
| Grid | 4 x 4 |
| Start | (0, 0) |
| Goal | (3, 3) |
| Obstacles | (1, 0), (2, 1) |
| Fixed path length | 6 moves |
| Search space | 4,096 |
| Valid routes | 7 |
| Grover iterations | 18 |
| Geometric circuit qubits | 26 |
| Initial circuit depth | 3,243 |

The seven valid route indices are:

`63, 207, 243, 783, 819, 3087, 3123`.

## Results and experimental status

### 1. Classical G3 benchmark

Thirty measurements were performed for each classical method.

| Method | Valid runs | Mean execution time |
|---|---:|---:|
| A* shortest path | 30/30 | 31.44 µs |
| Dijkstra shortest path | 30/30 | 28.24 µs |
| Exhaustive fixed-length route enumeration | 30/30 | 8.515 ms |

A* and Dijkstra solve the shortest-path objective. Exhaustive
enumeration is the direct classical comparator for the fixed-length
route-search problem addressed by Grover.

### 2. Geometric Grover circuit

The G3 geometric circuit was constructed with 26 qubits and
18 Grover iterations. Its initial depth was 3,243.

A separate pilot checkpoint records:

- Transpilation time: approximately 7.87 seconds;
- Transpiled circuit depth: 83,588;
- Transpiled operations: 104,296.

**Important:** the G3 geometric Aer simulation was not completed.
The G3 statistics record zero Grover repetitions and no quantum result.
The pilot checkpoint contains no completed simulation runs.

These structural and transpilation measurements must not be
interpreted as a successful quantum simulation.

### 3. Independent lookup-oracle reference

The file in `results/lookup_reference/` records a separate ideal
Grover reference experiment using a lookup-table phase oracle:

- 13 qubits (12 search qubits and one phase qubit);
- 18 Grover iterations;
- 3,000 shots over 30 repetitions;
- 2,994 successful measurements (99.8%);
- Wilson 95% confidence interval: [99.5643%, 99.9083%];
- Exact statevector success probability: approximately 99.8337%.

This is **not** a simulation of the 26-qubit geometric G3 oracle.
It validates an independent lookup-table reference model and must
be interpreted separately.

## Repository structure

The repository contains:
- `planners/classical/`: A* and Dijkstra reference planners.
- `planners/quantum/`: route encoding, reversible coordinates,
  geometric oracle circuits, and Grover construction.
- `experiments/`: classical benchmark and G3 pilot scripts.
- `tests/`: focused tests for encoding, reversible operations,
  and geometric oracles.
- `results/g3_geometric/`: G3 statistics and geometric pilot checkpoint.
- `results/lookup_reference/`: independent lookup-oracle reference data.

## Installation

Python 3.12 is recommended.

Create and activate a virtual environment:

    python3.12 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

Recorded development environment:
- Qiskit 2.6.2
- Qiskit Aer 0.18.4
- NumPy 2.5.5
- SciPy 1.18.1
- pytest 9.2.0

## Tests

Run the focused test suite from the repository root:

    PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 python -m pytest -q tests/test_geometric_oracle.py tests/test_geometric_oracle_optimized.py tests/test_reversible_coordinates.py tests/test_route_encoding.py

The isolated repository copy was validated with **14 passing tests**.

## Reproducibility and limitations

- G3 classical statistics:
  `results/g3_geometric/g3_4x4_l6_statistics.json`.
- Geometric pilot checkpoint:
  `results/g3_geometric/g3_4x4_l6_grover_checkpoint.json`.
- Independent lookup-oracle reference:
  `results/lookup_reference/lookup_oracle_grover_statistics.json`.
- The lookup-oracle implementation used for the reference experiment
  is not included in this repository snapshot.
- The full geometric G3 quantum simulation remains incomplete.
- No quantum hardware experiment is reported.
- No quantum advantage is claimed.
- Classical timing values depend on the execution environment.
- The full scientific manuscript is not included in this repository.

This snapshot focuses on the geometric Grover path-search study and
its currently validated artifacts.

## License

No license has been assigned yet. All rights remain with their
respective authors until a license is explicitly added.
