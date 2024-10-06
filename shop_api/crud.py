from typing import List, Optional
from shop_api.models import Item, Cart, CartItem

items_db: List[Item] = []
carts_db: List[Cart] = []
item_id_counter = 1
cart_id_counter = 1


async def create_item(name: str, price: float) -> Item:
    global item_id_counter
    item = Item(id=item_id_counter, name=name, price=price)
    items_db.append(item)
    item_id_counter += 1
    return item


async def get_item(item_id: int) -> Optional[Item]:
    for item in items_db:
        if item.id == item_id:
            return item
    return None


async def get_items(
    offset: int = 0, limit: int = 10, min_price: float = None, max_price: float = None, show_deleted: bool = False
) -> List[Item]:
    filtered_items = [
        item
        for item in items_db
        if (min_price is None or item.price >= min_price)
        and (max_price is None or item.price <= max_price)
        and (show_deleted or not item.deleted)
    ]
    return filtered_items[offset : offset + limit]


async def update_item(item_id: int, name: str, price: float) -> Optional[Item]:
    item = await get_item(item_id)
    if item:
        item.name = name
        item.price = price
    return item


async def patch_item(item_id: int, name: Optional[str] = None, price: Optional[float] = None) -> Optional[Item]:
    item = await get_item(item_id)
    if item:
        if name is not None:
            item.name = name
        if price is not None:
            item.price = price
        return item
    return None


async def delete_item(item_id: int) -> Optional[Item]:
    item = await get_item(item_id)
    if item:
        item.deleted = True
    return item


async def create_cart() -> Cart:
    global cart_id_counter
    cart = Cart(id=cart_id_counter)
    carts_db.append(cart)
    cart_id_counter += 1
    return cart


async def get_cart(cart_id: int) -> Optional[Cart]:
    for cart in carts_db:
        if cart.id == cart_id:
            return cart
    return None


async def add_item_to_cart(cart_id: int, item_id: int) -> Optional[Cart]:
    cart = await get_cart(cart_id)
    item = await get_item(item_id)

    if cart and item:
        for cart_item in cart.items:
            if cart_item.id == item.id:
                cart_item.quantity += 1
                await update_cart_price(cart)
                return cart

        cart.items.append(CartItem(id=item.id, name=item.name, quantity=1, available=not item.deleted))
        await update_cart_price(cart)
    else:
        return None
    return cart


async def update_cart_price(cart: Cart):
    total_price = 0.0
    for cart_item in cart.items:
        if cart_item.available:
            item = await get_item(cart_item.id)
            total_price += cart_item.quantity * item.price
    cart.price = total_price


async def get_carts(
    offset: int = 0,
    limit: int = 10,
    min_price: float = None,
    max_price: float = None,
    min_quantity: int = None,
    max_quantity: int = None,
) -> List[Cart]:
    filtered_carts = [
        cart
        for cart in carts_db
        if (min_price is None or cart.price >= min_price)
        and (max_price is None or cart.price <= max_price)
        and (min_quantity is None or sum(item.quantity for item in cart.items) >= min_quantity)
        and (max_quantity is None or sum(item.quantity for item in cart.items) <= max_quantity)
    ]
    return filtered_carts[offset : offset + limit]
