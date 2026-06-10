import pickle
import hashlib


def get_pickle_hash(data):
    pickle_data = pickle.dumps(data)
    return hashlib.sha256(pickle_data).hexdigest()


test_cases = {
    "none_value": None,
    "boolean_true": True,
    "boolean_false": False,
    "zero_integer": 0,
    "negative_integer": -1,
    "very_large_integer": 10 ** 100,
    "empty_tuple": (),
    "empty_dictionary": {},
    "empty_set": set(),
    "large_list": list(range(10000)),
    "large_string": "A" * 10000,
    "deep_nested_list": [[[[[1]]]]],
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