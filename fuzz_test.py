"""
Fuzz Testing for Pickle Module Stability
This module performs fuzz testing by generating random inputs
and testing pickle serialization stability.
"""

import pickle
import hashlib
import random
import string
import sys


def get_pickle_hash(data):
    """Generate SHA256 hash of pickled data."""
    pickle_data = pickle.dumps(data)
    return hashlib.sha256(pickle_data).hexdigest()


def generate_random_string(length):
    """Generate a random string of given length."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_random_list(depth, max_length):
    """Generate a random nested list."""
    if depth == 0 or random.random() < 0.3:
        return random.choice([
            random.randint(-1000, 1000),
            random.random() * 100,
            generate_random_string(random.randint(0, 10)),
            None,
            True,
            False
        ])
    
    length = random.randint(0, max_length)
    return [generate_random_list(depth - 1, max_length) for _ in range(length)]


def generate_random_dict(depth, max_items):
    """Generate a random nested dictionary."""
    if depth == 0 or random.random() < 0.3:
        return random.choice([
            random.randint(-1000, 1000),
            random.random() * 100,
            generate_random_string(random.randint(0, 10)),
            None,
            True,
            False
        ])
    
    items = {}
    num_items = random.randint(0, max_items)
    for _ in range(num_items):
        key = generate_random_string(random.randint(1, 5))
        items[key] = generate_random_dict(depth - 1, max_items)
    return items


def generate_random_tuple(depth, max_length):
    """Generate a random nested tuple."""
    if depth == 0 or random.random() < 0.3:
        return random.choice([
            random.randint(-1000, 1000),
            random.random() * 100,
            generate_random_string(random.randint(0, 10)),
            None,
            True,
            False
        ])
    
    length = random.randint(0, max_length)
    return tuple(generate_random_tuple(depth - 1, max_length) for _ in range(length))


def generate_random_set(max_items):
    """Generate a random set."""
    items = set()
    num_items = random.randint(0, max_items)
    for _ in range(num_items):
        items.add(random.choice([
            random.randint(-1000, 1000),
            generate_random_string(random.randint(1, 5)),
            random.random() * 100
        ]))
    return items


def fuzz_test_integer(num_tests=100):
    """Fuzz test with random integers."""
    print("\n=== Fuzz Testing: Integers ===")
    passed = 0
    failed = 0
    
    for i in range(num_tests):
        data = random.randint(-10**20, 10**20)
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        if hash1 == hash2:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: Input: {data}")
            print(f"Hash 1: {hash1}")
            print(f"Hash 2: {hash2}")
    
    print(f"Passed: {passed}/{num_tests}")
    print(f"Failed: {failed}/{num_tests}")
    return failed == 0


def fuzz_test_float(num_tests=100):
    """Fuzz test with random floats."""
    print("\n=== Fuzz Testing: Floats ===")
    passed = 0
    failed = 0
    
    for i in range(num_tests):
        data = random.uniform(-1e100, 1e100)
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        if hash1 == hash2:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: Input: {data}")
            print(f"Hash 1: {hash1}")
            print(f"Hash 2: {hash2}")
    
    print(f"Passed: {passed}/{num_tests}")
    print(f"Failed: {failed}/{num_tests}")
    return failed == 0


def fuzz_test_string(num_tests=100):
    """Fuzz test with random strings."""
    print("\n=== Fuzz Testing: Strings ===")
    passed = 0
    failed = 0
    
    for i in range(num_tests):
        length = random.randint(0, 1000)
        data = generate_random_string(length)
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        if hash1 == hash2:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: Input: '{data}' (length: {length})")
            print(f"Hash 1: {hash1}")
            print(f"Hash 2: {hash2}")
    
    print(f"Passed: {passed}/{num_tests}")
    print(f"Failed: {failed}/{num_tests}")
    return failed == 0


def fuzz_test_list(num_tests=100):
    """Fuzz test with random nested lists."""
    print("\n=== Fuzz Testing: Lists ===")
    passed = 0
    failed = 0
    
    for i in range(num_tests):
        depth = random.randint(0, 5)
        max_length = random.randint(0, 20)
        data = generate_random_list(depth, max_length)
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        if hash1 == hash2:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: Input: {data} (depth={depth}, length={max_length})")
            print(f"Hash 1: {hash1}")
            print(f"Hash 2: {hash2}")
    
    print(f"Passed: {passed}/{num_tests}")
    print(f"Failed: {failed}/{num_tests}")
    return failed == 0


def fuzz_test_dict(num_tests=100):
    """Fuzz test with random nested dictionaries."""
    print("\n=== Fuzz Testing: Dictionaries ===")
    passed = 0
    failed = 0
    
    for i in range(num_tests):
        depth = random.randint(0, 5)
        max_items = random.randint(0, 20)
        data = generate_random_dict(depth, max_items)
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        if hash1 == hash2:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: Input: {data} (depth={depth}, items={max_items})")
            print(f"Hash 1: {hash1}")
            print(f"Hash 2: {hash2}")
    
    print(f"Passed: {passed}/{num_tests}")
    print(f"Failed: {failed}/{num_tests}")
    return failed == 0


def fuzz_test_tuple(num_tests=100):
    """Fuzz test with random nested tuples."""
    print("\n=== Fuzz Testing: Tuples ===")
    passed = 0
    failed = 0
    
    for i in range(num_tests):
        depth = random.randint(0, 5)
        max_length = random.randint(0, 20)
        data = generate_random_tuple(depth, max_length)
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        if hash1 == hash2:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: Input: {data} (depth={depth}, length={max_length})")
            print(f"Hash 1: {hash1}")
            print(f"Hash 2: {hash2}")
    
    print(f"Passed: {passed}/{num_tests}")
    print(f"Failed: {failed}/{num_tests}")
    return failed == 0


def fuzz_test_set(num_tests=100):
    """Fuzz test with random sets."""
    print("\n=== Fuzz Testing: Sets ===")
    passed = 0
    failed = 0
    
    for i in range(num_tests):
        max_items = random.randint(0, 20)
        data = generate_random_set(max_items)
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        if hash1 == hash2:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: Input: {data} (items={max_items})")
            print(f"Hash 1: {hash1}")
            print(f"Hash 2: {hash2}")
    
    print(f"Passed: {passed}/{num_tests}")
    print(f"Failed: {failed}/{num_tests}")
    return failed == 0


def fuzz_test_mixed(num_tests=100):
    """Fuzz test with mixed data types."""
    print("\n=== Fuzz Testing: Mixed Data Types ===")
    passed = 0
    failed = 0
    
    for i in range(num_tests):
        data = random.choice([
            random.randint(-10**20, 10**20),
            random.uniform(-1e100, 1e100),
            generate_random_string(random.randint(0, 100)),
            generate_random_list(random.randint(0, 3), random.randint(0, 10)),
            generate_random_dict(random.randint(0, 3), random.randint(0, 10)),
            generate_random_tuple(random.randint(0, 3), random.randint(0, 10)),
            generate_random_set(random.randint(0, 10)),
            None,
            True,
            False
        ])
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        if hash1 == hash2:
            passed += 1
        else:
            failed += 1
            print(f"FAIL: Input: {data} (type: {type(data).__name__})")
            print(f"Hash 1: {hash1}")
            print(f"Hash 2: {hash2}")
    
    print(f"Passed: {passed}/{num_tests}")
    print(f"Failed: {failed}/{num_tests}")
    return failed == 0


def main():
    """Run all fuzz tests."""
    print("=" * 60)
    print("FUZZ TESTING FOR PICKLE MODULE STABILITY")
    print("=" * 60)
    
    random.seed(42)  # For reproducibility
    
    results = {}
    results['Integer'] = fuzz_test_integer(100)
    results['Float'] = fuzz_test_float(100)
    results['String'] = fuzz_test_string(100)
    results['List'] = fuzz_test_list(100)
    results['Dictionary'] = fuzz_test_dict(100)
    results['Tuple'] = fuzz_test_tuple(100)
    results['Set'] = fuzz_test_set(100)
    results['Mixed'] = fuzz_test_mixed(100)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    for test_type, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"{test_type}: {status}")
    
    all_passed = all(results.values())
    print("\n" + "=" * 60)
    if all_passed:
        print("OVERALL RESULT: ALL TESTS PASSED")
    else:
        print("OVERALL RESULT: SOME TESTS FAILED")
    print("=" * 60)
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
