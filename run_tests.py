import subprocess
import sys

def run_pytest():
    print("Running tests...")
    result = subprocess.run(["pytest"], text=True)
    if result.returncode == 0:
        print("\nAll tests are successful!")
    else:
        print("\nSome tests encountered issues.")
        sys.exit(result.returncode)

if __name__ == "__main__":
    run_pytest()
