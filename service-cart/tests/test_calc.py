from datetime import datetime
import sys
import os

def test_calc():
    timestamp = 2000000000  # example: Unix timestamp (seconds since epoch)

    # Convert to datetime object
    dt = datetime.fromtimestamp(timestamp)

    # Format to string
    date_string = dt.strftime("%Y-%m-%d %H:%M:%S")

    print("Datetime:", date_string)
