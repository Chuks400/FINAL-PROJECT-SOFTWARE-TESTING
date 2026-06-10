"""
White-Box Testing for Pickle Module
This module implements control flow analysis, data flow testing,
statement coverage, and branch coverage for pickle operations.
"""

import pickle
import hashlib
import sys
import io
import struct


def get_pickle_hash(data):
    """Generate SHA256 hash of pickled data."""
    pickle_data = pickle.dumps(data)
    return hashlib.sha256(pickle_data).hexdigest()


# ============================================================================
# CONTROL FLOW ANALYSIS - Serialization Path (pickle.dumps)
# ============================================================================

def test_control_flow_serialization():
    """
    Test control flow through pickle.dumps for different data types.
    Covers different protocol versions and data type paths.
    """
    print("\n=== Control Flow Analysis: Serialization Path ===")
    
    test_cases = [
        # Basic types
        ("Integer", 42),
        ("Float", 3.14),
        ("String", "hello"),
        ("Bytes", b"binary"),
        ("None", None),
        ("Boolean True", True),
        ("Boolean False", False),
        
        # Collections
        ("Empty List", []),
        ("List with integers", [1, 2, 3]),
        ("List with mixed types", [1, "a", 3.14, None]),
        ("Empty Tuple", ()),
        ("Tuple", (1, 2, 3)),
        ("Empty Dict", {}),
        ("Dict", {"a": 1, "b": 2}),
        ("Empty Set", set()),
        ("Set", {1, 2, 3}),
        
        # Nested structures
        ("Nested List", [[1, 2], [3, 4]]),
        ("Nested Dict", {"outer": {"inner": "value"}}),
        ("Mixed Nesting", {"list": [1, 2, {"key": "val"}]}),
        
        # Special cases
        ("Large Integer", 10**100),
        ("Negative Integer", -42),
        ("Zero", 0),
        ("Empty String", ""),
    ]
    
    results = []
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        print(f"\nProtocol {protocol}:")
        protocol_results = []
        
        for name, data in test_cases:
            try:
                # Serialize with specific protocol
                pickled = pickle.dumps(data, protocol=protocol)
                
                # Verify deserialization works
                unpickled = pickle.loads(pickled)
                
                # Verify data integrity
                if unpickled == data:
                    protocol_results.append((name, "PASS"))
                    print(f"  {name}: PASS (Input: {data})")
                else:
                    protocol_results.append((name, "FAIL - Data mismatch"))
                    print(f"  {name}: FAIL - Data mismatch (Input: {data})")
            except Exception as e:
                protocol_results.append((name, f"FAIL - {str(e)}"))
                print(f"  {name}: FAIL - {str(e)} (Input: {data})")
        
        results.append((protocol, protocol_results))
    
    return results


# ============================================================================
# CONTROL FLOW ANALYSIS - Deserialization Path (pickle.loads)
# ============================================================================

def test_control_flow_deserialization():
    """
    Test control flow through pickle.loads for different scenarios.
    Covers valid and invalid pickle data paths.
    """
    print("\n=== Control Flow Analysis: Deserialization Path ===")
    
    # Test valid deserialization
    valid_cases = [
        ("Integer", pickle.dumps(42)),
        ("Float", pickle.dumps(3.14)),
        ("String", pickle.dumps("hello")),
        ("List", pickle.dumps([1, 2, 3])),
        ("Dict", pickle.dumps({"a": 1})),
    ]
    
    print("\nValid Pickle Data:")
    for name, pickled in valid_cases:
        try:
            unpickled = pickle.loads(pickled)
            print(f"  {name}: PASS")
        except Exception as e:
            print(f"  {name}: FAIL - {str(e)}")
    
    # Test invalid/corrupted pickle data
    invalid_cases = [
        ("Empty bytes", b""),
        ("Random bytes", b"\x00\x01\x02\x03"),
        ("Truncated pickle", pickle.dumps([1, 2, 3])[:5]),
        ("Corrupted header", b"\x80\x04"),  # Protocol 4 header without data
        ("Invalid opcode", b"\x80\x04\x95\xff\xff\xff\xff"),
    ]
    
    print("\nInvalid Pickle Data (should raise exceptions):")
    for name, pickled in invalid_cases:
        try:
            unpickled = pickle.loads(pickled)
            print(f"  {name}: FAIL - Should have raised exception")
        except Exception as e:
            print(f"  {name}: PASS - Raised {type(e).__name__}")


# ============================================================================
# DATA FLOW TESTING - All-Def Coverage
# ============================================================================

def test_data_flow_all_def():
    """
    Test all-def coverage: ensure all variable definitions are used.
    Focus on pickle operations where data flows through serialization.
    """
    print("\n=== Data Flow Testing: All-Def Coverage ===")
    
    # Test that defined variables are properly serialized
    test_data = [
        ("Simple int", 42),
        ("String variable", "test_string"),
        ("List variable", [1, 2, 3]),
        ("Dict variable", {"key": "value"}),
    ]
    
    print("\nTesting variable definitions flow through serialization:")
    for name, data in test_data:
        # Define variable
        var = data
        
        # Serialize (definition flows to dumps)
        pickled = pickle.dumps(var)
        
        # Deserialize (definition flows to loads)
        unpickled = pickle.loads(pickled)
        
        # Verify definition was preserved
        if unpickled == var:
            print(f"  {name}: PASS - Definition preserved")
        else:
            print(f"  {name}: FAIL - Definition not preserved")


# ============================================================================
# DATA FLOW TESTING - All-Uses Coverage
# ============================================================================

def test_data_flow_all_uses():
    """
    Test all-uses coverage: ensure all uses of variables are tested.
    Focus on different use patterns of pickled data.
    """
    print("\n=== Data Flow Testing: All-Uses Coverage ===")
    
    # Test different uses of pickled data
    data = [1, 2, 3, 4, 5]
    pickled = pickle.dumps(data)
    
    uses = [
        ("Direct deserialization", lambda: pickle.loads(pickled)),
        ("Hash computation", lambda: hashlib.sha256(pickled).hexdigest()),
        ("Length check", lambda: len(pickled)),
        ("File write simulation", lambda: io.BytesIO(pickled).getvalue()),
    ]
    
    print("\nTesting different uses of pickled data:")
    for name, use_func in uses:
        try:
            result = use_func()
            print(f"  {name}: PASS")
        except Exception as e:
            print(f"  {name}: FAIL - {str(e)}")
    
    # Test uses of unpickled data
    unpickled = pickle.loads(pickled)
    
    uses_unpickled = [
        ("Iteration", lambda: list(unpickled)),
        ("Indexing", lambda: unpickled[0]),
        ("Slicing", lambda: unpickled[1:3]),
        ("Length", lambda: len(unpickled)),
        ("Modification", lambda: unpickled + [6]),
    ]
    
    print("\nTesting different uses of unpickled data:")
    for name, use_func in uses_unpickled:
        try:
            result = use_func()
            print(f"  {name}: PASS")
        except Exception as e:
            print(f"  {name}: FAIL - {str(e)}")


# ============================================================================
# STATEMENT COVERAGE
# ============================================================================

def test_statement_coverage():
    """
    Test statement coverage by exercising different code paths in pickle operations.
    """
    print("\n=== Statement Coverage Testing ===")
    
    # Cover different pickle protocols
    print("\nTesting different protocol versions:")
    for protocol in range(pickle.HIGHEST_PROTOCOL + 1):
        data = {"test": "data"}
        pickled = pickle.dumps(data, protocol=protocol)
        unpickled = pickle.loads(pickled)
        status = "PASS" if unpickled == data else "FAIL"
        print(f"  Protocol {protocol}: {status}")
    
    # Cover different encoding options
    print("\nTesting encoding options:")
    data = "test string with unicode: 你好"
    pickled_utf8 = pickle.dumps(data, protocol=pickle.HIGHEST_PROTOCOL)
    unpickled_utf8 = pickle.loads(pickled_utf8)
    status = "PASS" if unpickled_utf8 == data else "FAIL"
    print(f"  UTF-8 encoding: {status}")
    
    # Cover file-like object operations
    print("\nTesting file-like object operations:")
    data = [1, 2, 3, 4, 5]
    buffer = io.BytesIO()
    pickle.dump(data, buffer)
    buffer.seek(0)
    unpickled = pickle.load(buffer)
    status = "PASS" if unpickled == data else "FAIL"
    print(f"  BytesIO dump/load: {status}")


# ============================================================================
# BRANCH COVERAGE
# ============================================================================

def test_branch_coverage():
    """
    Test branch coverage by exercising conditional paths in pickle operations.
    """
    print("\n=== Branch Coverage Testing ===")
    
    # Branch: Different data types
    print("\nTesting different data type branches:")
    data_types = [
        ("None", None),
        ("Boolean True", True),
        ("Boolean False", False),
        ("Integer", 42),
        ("Float", 3.14),
        ("String", "test"),
        ("Bytes", b"test"),
        ("List", [1, 2, 3]),
        ("Tuple", (1, 2, 3)),
        ("Dict", {"a": 1}),
        ("Set", {1, 2, 3}),
    ]
    
    for name, data in data_types:
        try:
            pickled = pickle.dumps(data)
            unpickled = pickle.loads(pickled)
            status = "PASS" if unpickled == data else "FAIL"
            print(f"  {name}: {status}")
        except Exception as e:
            print(f"  {name}: FAIL - {str(e)}")
    
    # Branch: Empty vs non-empty collections
    print("\nTesting empty vs non-empty branches:")
    collections = [
        ("Empty list", []),
        ("Non-empty list", [1]),
        ("Empty dict", {}),
        ("Non-empty dict", {"a": 1}),
        ("Empty tuple", ()),
        ("Non-empty tuple", (1,)),
        ("Empty set", set()),
        ("Non-empty set", {1}),
    ]
    
    for name, data in collections:
        try:
            pickled = pickle.dumps(data)
            unpickled = pickle.loads(pickled)
            status = "PASS" if unpickled == data else "FAIL"
            print(f"  {name}: {status}")
        except Exception as e:
            print(f"  {name}: FAIL - {str(e)}")
    
    # Branch: Exception handling paths
    print("\nTesting exception handling branches:")
    exception_cases = [
        ("Invalid pickle data", b"invalid"),
        ("Truncated data", b"\x80\x04"),
        ("Wrong protocol marker", b"\x80\x99"),
    ]
    
    for name, data in exception_cases:
        try:
            unpickled = pickle.loads(data)
            print(f"  {name}: FAIL - Should have raised exception")
        except Exception:
            print(f"  {name}: PASS - Exception raised")


# ============================================================================
# EXCEPTION PATH TESTING
# ============================================================================

def test_exception_paths():
    """
    Test exception paths for invalid/corrupted pickle data.
    """
    print("\n=== Exception Path Testing ===")
    
    exception_cases = [
        ("Empty bytes", b"", pickle.UnpicklingError),
        ("Random garbage", b"\x00\x01\x02\x03\x04\x05", pickle.UnpicklingError),
        ("Invalid protocol", b"\x80\x99", pickle.UnpicklingError),
        ("Truncated after header", b"\x80\x04", pickle.UnpicklingError),
        ("Corrupted opcode", b"\x80\x04\x95\xff\xff\xff\xff", pickle.UnpicklingError),
    ]
    
    print("\nTesting exception paths:")
    for name, data, expected_exception in exception_cases:
        try:
            unpickled = pickle.loads(data)
            print(f"  {name}: FAIL - Expected {expected_exception.__name__}")
        except expected_exception:
            print(f"  {name}: PASS - Raised {expected_exception.__name__}")
        except Exception as e:
            print(f"  {name}: PARTIAL - Raised {type(e).__name__} instead of {expected_exception.__name__}")


# ============================================================================
# RECURSIVE DATA STRUCTURE TESTING
# ============================================================================

def test_recursive_structures():
    """
    Test serialization of recursive data structures.
    """
    print("\n=== Recursive Data Structure Testing ===")
    
    # Create a simple recursive structure
    recursive_list = []
    recursive_list.append(recursive_list)
    
    print("\nTesting self-referential list:")
    try:
        pickled = pickle.dumps(recursive_list)
        unpickled = pickle.loads(pickled)
        # Check if it's still self-referential
        if unpickled[0] is unpickled:
            print("  Self-referential list: PASS")
        else:
            print("  Self-referential list: FAIL - Reference not preserved")
    except Exception as e:
        print(f"  Self-referential list: FAIL - {str(e)}")
    
    # Test deeply nested structure
    deep_nested = 1
    for _ in range(100):
        deep_nested = [deep_nested]
    
    print("\nTesting deeply nested structure (100 levels):")
    try:
        pickled = pickle.dumps(deep_nested)
        unpickled = pickle.loads(pickled)
        print("  Deeply nested structure: PASS")
    except Exception as e:
        print(f"  Deeply nested structure: FAIL - {str(e)}")


# ============================================================================
# MAIN TEST RUNNER
# ============================================================================

def main():
    """Run all white-box tests."""
    print("=" * 60)
    print("WHITE-BOX TESTING FOR PICKLE MODULE")
    print("=" * 60)
    
    # Run all test categories
    test_control_flow_serialization()
    test_control_flow_deserialization()
    test_data_flow_all_def()
    test_data_flow_all_uses()
    test_statement_coverage()
    test_branch_coverage()
    test_exception_paths()
    test_recursive_structures()
    
    print("\n" + "=" * 60)
    print("WHITE-BOX TESTING COMPLETE")
    print("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
