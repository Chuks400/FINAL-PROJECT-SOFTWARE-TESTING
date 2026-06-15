import pickle
import hashlib


def get_hash(data, protocol):
    pickle_bytes = pickle.dumps(data, protocol=protocol)
    return hashlib.sha256(pickle_bytes).hexdigest()


def test_protocol_difference():
    print("=" * 60)
    print("NEGATIVE TEST 1: Protocol Difference Test")
    print("=" * 60)

    data = {"name": "John", "age": 25}

    hash_protocol_4 = get_hash(data, protocol=4)
    hash_protocol_5 = get_hash(data, protocol=5)

    print("Input:", data)
    print("Hash using Protocol 4:", hash_protocol_4)
    print("Hash using Protocol 5:", hash_protocol_5)

    if hash_protocol_4 == hash_protocol_5:
        print("Result: PASS - Hashes are the same")
    else:
        print("Result: FAIL - Hashes are different because protocols are different")

    print()


def test_corrupted_pickle_data():
    print("=" * 60)
    print("NEGATIVE TEST 2: Corrupted Pickle Data Test")
    print("=" * 60)

    data = [1, 2, 3, 4, 5]

    good_pickle = pickle.dumps(data, protocol=4)
    corrupted_pickle = good_pickle[:-2]

    print("Original input:", data)
    print("Trying to load corrupted pickle data...")

    try:
        pickle.loads(corrupted_pickle)
        print("Result: PASS - Data loaded successfully")
    except Exception as error:
        print("Result: FAIL - Corrupted data could not be loaded")
        print("Error Type:", type(error).__name__)
        print("Error Message:", error)

    print()


if __name__ == "__main__":
    test_protocol_difference()
    test_corrupted_pickle_data()