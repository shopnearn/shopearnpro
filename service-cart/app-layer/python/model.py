
from abc import ABC, abstractmethod

from pydantic.dataclasses import dataclass

from pydantic import BaseModel

class Product(BaseModel):
    id: str
    name: str | None = "default"
    desc: str | None = None
    sku: str | None = None
    cat: str | None = None
    price: float | None = 0.0
    qty: int | None = 0
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
