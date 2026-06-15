# Pickle Module Stability and Correctness Testing

## Overview
This project comprehensively tests the stability and correctness of Python's pickle module. The pickle module implements binary protocols for serializing and deserializing Python object structures. This test suite verifies whether the same input always creates identical (hash-identical) serialized output.

## Project Structure
```
pickle-stability-project/
├── black_box_pickle_test.py      # Equivalence partitioning tests
├── boundary_pickle_test.py       # Boundary value analysis tests
├── fuzz_test.py                  # Fuzz testing with random inputs
├── white_box_test.py             # White-box testing (control flow, data flow, coverage)
├── negative_tests.py             # Negative testing (protocol differences, corrupted data)
├── run_all.py                    # Automated test runner
├── cross_environment_test.py     # Cross-environment verification
├── results.txt                   # Comprehensive test results log
├── traceability_matrix.md        # Requirements to test cases mapping
├── findings.md                   # Test results and findings
├── limitations.md                # Test suite limitations
├── README.md                     # This file
└── report/                       # Final report directory
```

## Testing Techniques Used

### Black-Box Testing
1. **Equivalence Partitioning**: Groups similar inputs into equivalence classes
   - Basic types: int, float, string
   - Collections: list, dict, tuple, set
   - Nested structures

2. **Boundary Value Analysis**: Tests edge cases and boundaries
   - Empty collections
   - Zero values
   - Very large values
   - Deep nesting

3. **Fuzz Testing**: Random input generation
   - 800 random test cases across 8 categories
   - Reproducible with fixed random seed

### White-Box Testing
1. **Control Flow Analysis**: Tests serialization and deserialization paths
   - All pickle protocols (0-5)
   - Valid and invalid data paths
   - Exception handling paths

2. **Data Flow Testing**: All-def and All-uses coverage
   - Variable definition flow
   - Different use patterns

3. **Statement Coverage**: Code path coverage
   - Protocol versions
   - Encoding options
   - File-like operations

4. **Branch Coverage**: Conditional branch testing
   - Data type branches
   - Collection branches
   - Exception branches

### Negative Testing
1. **Protocol Difference Verification**: Confirms different protocols produce different hashes
   - Tests protocol 4 vs protocol 5
   - Verifies expected hash differences

2. **Corrupted Data Handling**: Tests error handling for invalid pickle data
   - Truncated pickle data
   - Verifies UnpicklingError is raised

## Running the Tests

### Prerequisites
- Python 3.x
- Standard library modules: pickle, hashlib, random, string, sys, io, struct

### Running Individual Test Suites

```bash
# Equivalence partitioning
python black_box_pickle_test.py

# Boundary value analysis
python boundary_pickle_test.py

# Fuzz testing
python fuzz_test.py

# White-box testing
python white_box_test.py

# Negative testing
python negative_tests.py

# Cross-environment test
python cross_environment_test.py
```

### Running All Tests
```bash
# Run all test suites using automated runner
python run_all.py
```

## Test Results Summary

| Metric | Value |
|--------|-------|
| Total Test Cases | 40 |
| Passed | 40 |
| Failed | 0 |
| Pass Rate | 100% |
| Testing Techniques | 6 |
| Data Types Tested | 11 |
| Protocols Tested | 6 (0-5) |
| Fuzz Test Iterations | 800 |
| Negative Test Cases | 2 |
| Operating Systems Tested | 2 (Windows 11, Ubuntu) |
| Python Versions Tested | 4 (3.8, 3.9, 3.12, 3.14) |

## Key Findings

1. **Pickle serialization is deterministic**: All tests produced identical SHA256 hashes for repeated serialization of the same input
2. **Protocol compatibility**: All pickle protocols (0-5) correctly serialize and deserialize data
3. **Data type coverage**: All standard Python data types work correctly
4. **Edge case handling**: Robust handling of extreme values and large structures
5. **Recursive structures**: Self-referential and deeply nested structures handled correctly
6. **Exception handling**: Invalid data properly raises appropriate exceptions
7. **Negative testing**: Different protocols correctly produce different hashes, and corrupted data is properly rejected

## Limitations

- Limited operating systems (Windows 11, Ubuntu tested; macOS not tested)
- Limited Python versions (3.8, 3.9, 3.12, 3.14 tested; 3.10, 3.11 not tested)
- Limited object types (custom classes not tested)
- Limited Unicode testing
- No performance testing
- No security testing

See [limitations.md](limitations.md) for detailed limitations.

## Traceability

See [traceability_matrix.md](traceability_matrix.md) for the complete mapping of requirements to test cases.

## Code Style

All code follows PEP 8 guidelines:
- 4-space indentation
- Maximum line length of 79 characters
- Descriptive variable names
- Docstrings for all functions
- Type hints where appropriate

## Team Members

[Add team member names and contributions here]

## License

This project is for educational purposes as part of a software testing course.

## References

- Python Pickle Documentation: https://docs.python.org/3/library/pickle.html
- PEP 8 -- Style Guide for Python Code: https://peps.python.org/pep-0008/
