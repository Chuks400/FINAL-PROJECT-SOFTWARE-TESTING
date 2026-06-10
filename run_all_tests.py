"""
Run all test suites for pickle module stability and correctness testing.
"""

import subprocess
import sys


def run_test_file(filename):
    """Run a single test file and return success status."""
    print(f"\n{'=' * 70}")
    print(f"Running: {filename}")
    print('=' * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, filename],
            cwd="c:/Users/John/Downloads/FINAL PROJECT SOFTWARE TESTING",
            capture_output=False
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {filename}: {e}")
        return False


def main():
    """Run all test files."""
    print("=" * 70)
    print("RUNNING ALL PICKLE MODULE TESTS")
    print("=" * 70)
    
    test_files = [
        "black_box_pickle_test.py",
        "boundary_pickle_test.py",
        "fuzz_test.py",
        "white_box_test.py",
        "unstable_test.py",
    ]
    
    results = {}
    
    for test_file in test_files:
        success = run_test_file(test_file)
        results[test_file] = success
    
    # Print summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    for test_file, success in results.items():
        status = "PASS" if success else "FAIL"
        print(f"{test_file}: {status}")
    
    total = len(results)
    passed = sum(1 for v in results.values() if v)
    failed = total - passed
    
    print(f"\nTotal: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass Rate: {(passed/total)*100:.1f}%")
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
