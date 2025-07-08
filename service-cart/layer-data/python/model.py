from abc import ABC, abstractmethod


class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price


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
