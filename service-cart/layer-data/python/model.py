from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    desc: str
    price: float
    sku: str
    qty: int
    cat: str | None = None
    active: bool = True


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
