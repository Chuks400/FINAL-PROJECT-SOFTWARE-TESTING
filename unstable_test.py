"""
Unstable Test Cases for Pickle Module
This module tests scenarios where pickle behavior may vary.
These are legitimate edge cases that demonstrate potential instability.
"""

import pickle
import hashlib
import sys
import time


def get_pickle_hash(data, protocol=None):
    """Generate SHA256 hash of pickled data."""
    if protocol is None:
        pickle_data = pickle.dumps(data)
    else:
        pickle_data = pickle.dumps(data, protocol=protocol)
    return hashlib.sha256(pickle_data).hexdigest()


class CustomObject:
    """Custom object with non-deterministic state."""
    def __init__(self, value):
        self.value = value
        self.timestamp = None
    
    def __getstate__(self):
        # Simulate non-deterministic state
        return {'value': self.value, 'timestamp': time.time()}
    
    def __setstate__(self, state):
        self.value = state['value']
        self.timestamp = state['timestamp']


def test_set_ordering():
    """
    Test that sets may produce different pickle outputs due to unordered nature.
    Sets are unordered, so different Python versions/implementations may serialize differently.
    """
    print("\n=== Unstable Test: Set Ordering ===")
    
    # Create sets with same elements but different creation order
    # This can cause different internal ordering in some Python versions
    set1 = set()
    for i in [3, 1, 4, 1, 5, 9, 2, 6]:
        set1.add(i)
    
    set2 = set()
    for i in [6, 2, 9, 5, 1, 4, 1, 3]:
        set2.add(i)
    
    # Serialize both sets
    hash1 = get_pickle_hash(set1)
    hash2 = get_pickle_hash(set2)
    
    print(f"Set 1 (created with [3,1,4,1,5,9,2,6]): {set1}")
    print(f"Set 2 (created with [6,2,9,5,1,4,1,3]): {set2}")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    
    if hash1 == hash2:
        print("Result: STABLE - Set serialization is consistent in this Python version")
        print("Note: Sets may still vary across different Python versions or implementations")
        return False  # Not unstable in this run
    else:
        print("Result: UNSTABLE - Set serialization varies based on creation order")
        return True


def test_floating_point_precision():
    """
    Test floating point numbers that may have precision issues.
    Different floating point representations across systems may cause variations.
    """
    print("\n=== Unstable Test: Floating Point Precision ===")
    
    # Test with floating point numbers that might have precision issues
    test_cases = [
        ("PI approximation", 3.141592653589793),
        ("Very small float", 1e-100),
        ("Very large float", 1e100),
        ("NaN", float('nan')),
        ("Infinity", float('inf')),
        ("Negative Infinity", float('-inf')),
    ]
    
    found_unstable = False
    
    for name, data in test_cases:
        hash1 = get_pickle_hash(data)
        hash2 = get_pickle_hash(data)
        
        print(f"\n{name}:")
        print(f"Input: {data}")
        print(f"Hash 1: {hash1}")
        print(f"Hash 2: {hash2}")
        
        if hash1 == hash2:
            print("Result: STABLE")
        else:
            print("Result: UNSTABLE")
            found_unstable = True
    
    return found_unstable


def test_protocol_differences():
    """
    Test that different protocol versions produce different pickle outputs.
    This is expected behavior, not a bug.
    """
    print("\n=== Unstable Test: Protocol Version Differences ===")
    
    data = {"key": "value", "number": 42}
    
    hashes = {}
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        hash_value = get_pickle_hash(data, protocol)
        hashes[protocol] = hash_value
        print(f"Protocol {protocol}: {hash_value}")
    
    # Check if all hashes are the same (they shouldn't be)
    unique_hashes = set(hashes.values())
    
    print(f"\nInput: {data}")
    print(f"Number of unique hashes across protocols: {len(unique_hashes)}")
    
    if len(unique_hashes) > 1:
        print("Result: UNSTABLE (Expected) - Different protocols produce different outputs")
        print("This is intentional design, not a bug")
        return True
    else:
        print("Result: STABLE - All protocols produce same output")
        return False


def test_custom_object_with_state():
    """
    Test custom objects with __getstate__ that might produce non-deterministic output.
    """
    print("\n=== Unstable Test: Custom Object with State ===")
    
    data = CustomObject(42)
    
    hash1 = get_pickle_hash(data)
    
    # Add a small delay to ensure timestamp changes
    time.sleep(0.01)
    
    hash2 = get_pickle_hash(data)
    
    print(f"Input: CustomObject(value=42)")
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    
    if hash1 == hash2:
        print("Result: STABLE")
        return False
    else:
        print("Result: UNSTABLE - Timestamp changes between serializations")
        return True


def test_dictionary_insertion_order():
    """
    Test that dictionaries with different insertion orders may produce different outputs.
    Note: Python 3.7+ preserves insertion order, but this may vary across versions.
    """
    print("\n=== Unstable Test: Dictionary Insertion Order ===")
    
    # Create dictionaries with same content but different insertion order
    dict1 = {}
    dict1['a'] = 1
    dict1['b'] = 2
    dict1['c'] = 3
    
    dict2 = {}
    dict2['c'] = 3
    dict2['b'] = 2
    dict2['a'] = 1
    
    print(f"Dict 1 (insertion order: a, b, c): {dict1}")
    print(f"Dict 2 (insertion order: c, b, a): {dict2}")
    
    hash1 = get_pickle_hash(dict1)
    hash2 = get_pickle_hash(dict2)
    
    print(f"Hash 1: {hash1}")
    print(f"Hash 2: {hash2}")
    
    if hash1 == hash2:
        print("Result: STABLE - Dictionary order is preserved (Python 3.7+)")
        return False
    else:
        print("Result: UNSTABLE - Dictionary insertion order affects serialization")
        return True


def test_bytes_vs_bytearray():
    """
    Test that bytes and bytearray may produce different pickle outputs.
    """
    print("\n=== Unstable Test: Bytes vs Bytearray ===")
    
    data_bytes = b"hello"
    data_bytearray = bytearray(b"hello")
    
    print(f"Input (bytes): {data_bytes}")
    print(f"Input (bytearray): {data_bytearray}")
    
    hash_bytes = get_pickle_hash(data_bytes)
    hash_bytearray = get_pickle_hash(data_bytearray)
    
    print(f"Hash (bytes): {hash_bytes}")
    print(f"Hash (bytearray): {hash_bytearray}")
    
    if hash_bytes == hash_bytearray:
        print("Result: STABLE - bytes and bytearray serialize identically")
        return False
    else:
        print("Result: UNSTABLE - bytes and bytearray serialize differently")
        return True


def main():
    """Run all unstable tests."""
    print("=" * 60)
    print("UNSTABLE TEST CASES FOR PICKLE MODULE")
    print("=" * 60)
    print("\nThese tests demonstrate scenarios where pickle behavior may vary.")
    print("Some variations are expected (e.g., protocol differences),")
    print("while others may indicate potential issues.")
    
    results = {}
    
    results['Set Ordering'] = test_set_ordering()
    results['Floating Point Precision'] = test_floating_point_precision()
    results['Protocol Differences'] = test_protocol_differences()
    results['Custom Object with State'] = test_custom_object_with_state()
    results['Dictionary Insertion Order'] = test_dictionary_insertion_order()
    results['Bytes vs Bytearray'] = test_bytes_vs_bytearray()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    unstable_count = sum(1 for v in results.values() if v)
    stable_count = sum(1 for v in results.values() if not v)
    
    for test_name, is_unstable in results.items():
        status = "UNSTABLE" if is_unstable else "STABLE"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal Unstable: {unstable_count}/{len(results)}")
    print(f"Total Stable: {stable_count}/{len(results)}")
    
    print("\n" + "=" * 60)
    if unstable_count > 0:
        print("CONCLUSION: Found unstable scenarios")
        print("These demonstrate that pickle is not always deterministic")
    else:
        print("CONCLUSION: All tests stable in this environment")
        print("Unstable behavior may occur in different Python versions or OS")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
