from __future__ import annotations
from pydantic import BaseModel
from typing import List


class CartItem(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool

class CartRequest(BaseModel):
    item_id: int

class CartResponse(BaseModel):
    id: int
    items: List[CartItem]
    price: float



