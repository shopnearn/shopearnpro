def db_write(event, context):
    print("db_write executed")


def parse_value(value):
    if isinstance(value, dict):
        for key, val in value.items():
            # Handle type annotations
            if key == "S":  # String
                return str(val)
            elif key == "N":  # Number
                return int(val) if val.isdigit() else float(val)
            elif key == "BOOL":  # Boolean
                return bool(val)
            elif key == "NULL":  # Null
                return None
            elif key == "M":  # Map
                return {k: parse_value(v) for k, v in value.items()}
            elif key == "L":  # List
                return [parse_value(item) for item in val]
            elif key == "SS":  # String Set
                return set(val)
            elif key == "NS":  # Number Set
                return set(int(item) if item.isdigit() else float(item) for item in val)
            elif key == "BS":  # Binary Set
                return set(bytes(item, 'utf-8') for item in val)
    return value


def dblist_to_json(dynamodb_json_list):
    return [parse_value(v) for v in dynamodb_json_list]
