from typing import Annotated
from pydantic import BaseModel, StringConstraints

TypedUlidId = Annotated[str, StringConstraints(min_length=28, max_length=64)]


class Product(BaseModel):
    id: TypedUlidId | None = None
    name: str = "default"
    desc: str | None = None
    sku: str | None = None
    cat: str | None = None
    price: float = 0.0
    qty: int = 0
    active: bool = True


class Name(BaseModel):
    first: str
    last: str
    middle: str | None = None

    def full(self, reverse: bool = False):
        return f"{self.last}, {self.first} " if reverse else f"{self.first} {self.last}"

class Phone(BaseModel):
    home: str | None = None
    cell: str | None = None
    work: str | None = None
    other: str | None = None
