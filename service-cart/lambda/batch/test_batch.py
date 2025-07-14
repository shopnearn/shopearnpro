from datetime import datetime
import sys

def test_batch():
    # Get the current date and time
    now = datetime.now()

    # Convert to timestamp (seconds since epoch)
    timestamp = now.timestamp()

    print("Current date and time:", now)
    print("Current timestamp:", int(timestamp * 1000))
    print("Max size (platform-dependent):", sys.maxsize)
    print(2**32, 2**64)
