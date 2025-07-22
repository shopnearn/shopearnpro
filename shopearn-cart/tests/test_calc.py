from datetime import datetime


def test_calc():
    timestamp1 = 1810000000  # example: Unix timestamp (seconds since epoch)
    timestamp2 = 1800000000  # example: Unix timestamp (seconds since epoch)

    # Convert to datetime object
    dt1 = datetime.fromtimestamp(timestamp1)
    dt2 = datetime.fromtimestamp(timestamp2)

    print()
    print("abc".endswith("c"))

    # Format to string
    date_string1 = dt1.strftime("%Y-%m-%d %H:%M:%S")
    date_string2 = dt2.strftime("%Y-%m-%d %H:%M:%S")

    print(f"Datetime:{date_string1} {date_string2}")
