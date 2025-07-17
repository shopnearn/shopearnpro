import json
import os
from abc import abstractmethod, ABC
from decimal import Decimal
from json import JSONEncoder

from boto3 import resource
from boto3.dynamodb.types import TypeDeserializer
from config import ddb_config

MARKET_TABLE = os.environ["MARKET_TABLE"]
ddb = resource('dynamodb', config=ddb_config)
market = ddb.Table(MARKET_TABLE)
deserializer = TypeDeserializer()


class DecimalEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o) if o % 1 == 0 else float(o)
        return super().default(o)

def ddb_dumps(item):
    return json.dumps(item, cls=DecimalEncoder)

def from_ddb(item):
    return {k: deserializer.deserialize(v) for k, v in item.items()}

def get_handler():
    return DdbProductHandler()


class DbProductHandler(ABC):
    @abstractmethod
    def create_product(self, product):
        pass

    @abstractmethod
    def get_product(self, product_id):
        pass

    @abstractmethod
    def delete_product(self, product_id):
        pass

    @abstractmethod
    def list_product(self):
        pass


class DdbProductHandler(DbProductHandler):
    def create_product(self, product):
        # TODO: implement this method
        pass

    def get_product(self, product_id):
        # TODO: implement this method
        pass

    def delete_product(self, product_id):
        # TODO: implement this method
        pass

    def list_product(self):
        # TODO: implement this method
        pass
