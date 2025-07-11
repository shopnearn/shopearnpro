from boto3 import resource
from botocore.config import Config

import model
import os

config = Config(
    retries = {
        'max_attempts': 7,
        'mode': 'standard'
    },
    read_timeout = 20,
    connect_timeout = 10,
)

MARKET = os.environ["MARKET_TABLE"]
# client = boto3.client('dynamodb')
ddb = resource('dynamodb', config=config)
market = ddb.Table(MARKET)


def db_write():
    print("db_write executed")


def get_handler():
    return DdbProductHandler()


class DdbProductHandler(model.DbProductHandler):
    def create_product(self, product):
        #TODO: implement this method
        pass

    def get_product(self, product_id):
        #TODO: implement this method
        pass

    def delete_product(self, product_id):
        #TODO: implement this method
        pass

    def list_product(self):
        #TODO: implement this method
        pass


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
