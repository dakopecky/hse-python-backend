from pydantic import BaseModel, ConfigDict
from typing import List, Optional


class Item(BaseModel):
    id: int
    name: str
    price: float
    deleted: bool = False


class CartItem(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool


class Cart(BaseModel):
    id: int
    items: List[CartItem] = []
    price: float = 0.0


class ItemCreateRequest(BaseModel):
    name: str
    price: float


class ItemUpdateRequest(BaseModel):
    name: str
    price: float


class ItemPatchRequest(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None

    model_config = ConfigDict(extra="forbid")
