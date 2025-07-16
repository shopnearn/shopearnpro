from abc import abstractmethod, ABC

from boto3 import resource
from botocore.config import Config

import model
import os

config = Config(
    retries={
        'max_attempts': 7,
        'mode': 'standard'
    },
    read_timeout=20,
    connect_timeout=10,
)

MARKET = os.environ["MARKET_TABLE"]
# client = boto3.client('dynamodb')
ddb = resource('dynamodb', config=config)
market = ddb.Table(MARKET)


def db_write():
    print("db_write executed")


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
