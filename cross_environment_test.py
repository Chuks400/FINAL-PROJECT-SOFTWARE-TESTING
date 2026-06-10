import pickle
import hashlib

data = 123

pickle_data = pickle.dumps(data, protocol=4)

print("Pickle Bytes:", pickle_data)
print("SHA256:", hashlib.sha256(pickle_data).hexdigest())