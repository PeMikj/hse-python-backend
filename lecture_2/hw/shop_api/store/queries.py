from typing import Iterable, List, Optional 

from .models import Cart, CartItem, Item
from ..api.item.contracts import ItemRequest, ItemPatchRequest

_cart_db = dict[int, Cart]()
_item_db = dict[int, Item]()


def int_id_generator() -> Iterable[int]:
    i = 0
    while True:
        yield i
        i += 1


_id_cart_generator = int_id_generator()
_id_item_generator = int_id_generator()


def create_cart() -> int:
    cart_id = next(_id_cart_generator)
    cart = Cart(id=cart_id)
    _cart_db[cart_id] = cart
    return cart


def get_cart(cart_id: int) -> Optional[Cart]:
    return _cart_db.get(cart_id)


def get_carts(
    offset: int,
    limit: int,
    min_price: Optional[float],
    max_price: Optional[float],
    min_quantity: Optional[int],
    max_quantity: Optional[int],
) -> List[Cart]:
    carts = list(_cart_db.values())

    if not carts:
        return None

    if min_price is not None:
        carts = [cart for cart in carts if cart.price >= min_price]

    if max_price is not None:
        carts = [cart for cart in carts if cart.price <= max_price]


    if min_quantity is not None:
        carts = [
            cart
            for cart in carts
            if sum(item.quantity for item in cart.items) >= min_quantity
        ]

    if max_quantity is not None:
        carts = [
            cart
            for cart in carts
            if sum(item.quantity for item in cart.items) <= max_quantity
        ]

    return carts[offset : offset + limit]


def create_item(item_request: ItemRequest) -> Item:
    item_id = next(_id_item_generator)
    item = Item(id=item_id, name=item_request.name, price=item_request.price)
    _item_db[item_id] = item
    return item


def get_item(item_id: int) -> Optional[Item]:
    return _item_db.get(item_id)


def add_item_to_cart(cart_id: int, item_id: int) -> Cart:
    item = get_item(item_id)
    cart = get_cart(cart_id)

    for cart_item in cart.items:
        if cart_item.id == item_id:
            cart_item.quantity += 1
            break
    else:
        cart.items.append(
            CartItem(id=item.id, name=item.name, quantity=1, available=True)
        )

    cart.price += item.price

    return cart


def get_items(
    offset: int,
    limit: int,
    min_price: Optional[float],
    max_price: Optional[float],
    show_deleted: bool,
) -> List[Item]:
    items = list(_item_db.values())
    if not items:
        return None

    if min_price:
        items = [item for item in items if item.price >= min_price]

    if max_price:
        items = [item for item in items if item.price <= max_price]

    if not show_deleted:
        items = [item for item in items if not item.deleted]

    return items[offset : offset + limit]


def update_item(item_id: int, item_request: ItemRequest) -> Item:
    item = get_item(item_id)

    if item is None or item.deleted:
        return None
    item.name = item_request.name
    item.price = item_request.price
    return item


def patch_item(item_id: int, item_patch_request: ItemPatchRequest) -> Item:
    item = get_item(item_id)
    if item is None or item.deleted:
        return None

    if item_patch_request.name:
        item.name = item_patch_request.name
    if item_patch_request.price:
        item.price = item_patch_request.price

    return item


def delete_item(item_id: int) -> Optional[Item]:
    item = _item_db.get(item_id)
    if item:
        item.deleted = True
    return item
