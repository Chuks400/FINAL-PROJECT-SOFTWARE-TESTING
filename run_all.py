import subprocess

print("Running Black-Box Tests...")
subprocess.run(["python", "black_box_pickle_test.py"])

print("\nRunning Boundary Tests...")
subprocess.run(["python", "boundary_pickle_test.py"])

print("\nRunning Fuzz Tests...")
subprocess.run(["python", "fuzz_test.py"])

print("\nRunning White-Box Tests...")
subprocess.run(["python", "white_box_test.py"])

print("\nRunning Negative Tests...")
subprocess.run(["python", "negative_tests.py"])

print("\nALL TESTS COMPLETED")