import pickle
import hashlib


def get_pickle_hash(data):
    pickle_data = pickle.dumps(data)
    return hashlib.sha256(pickle_data).hexdigest()


test_cases = {
    "integer": 123,
    "float": 3.14,
    "string": "Hello",
    "empty_list": [],
    "normal_list": [1, 2, 3, 4, 5],
    "dictionary": {"name": "John", "age": 25},
    "nested_data": {"numbers": [1, 2, 3], "text": "test"},
    "empty_string": "",
    "large_number": 999999999999,
}

for name, data in test_cases.items():
    hash1 = get_pickle_hash(data)
    hash2 = get_pickle_hash(data)

    print("Test case:", name)
    print("Input:", data)
    print("Hash 1:", hash1)
    print("Hash 2:", hash2)

    if hash1 == hash2:
        print("Result: PASS - Stable output")
    else:
        print("Result: FAIL - Unstable output")

    print("-" * 50)