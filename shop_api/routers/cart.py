from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from http import HTTPStatus
from typing import List
from shop_api.crud import create_cart, get_cart, get_carts, add_item_to_cart
from shop_api.models import Cart

router = APIRouter()


@router.post(
    "/cart",
    status_code=HTTPStatus.CREATED,
    summary="Create a new cart",
    description="Create a new shopping cart (RPC). No request body required.",
)
async def create_new_cart():
    cart = await create_cart()
    return JSONResponse(
        content={"id": cart.id}, headers={"Location": f"/cart/{cart.id}"}, status_code=HTTPStatus.CREATED
    )


@router.get(
    "/cart/{cart_id}",
    response_model=Cart,
    summary="Get a cart by ID",
    description="Retrieve a shopping cart by its ID",
)
async def get_cart_by_id(cart_id: int):
    cart = await get_cart(cart_id)
    if cart is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cart not found")
    return cart


@router.get(
    "/cart",
    response_model=List[Cart],
    summary="Get list of carts",
    description="Retrieve a list of carts with optional filtering by total price and item quantity",
)
async def get_cart_list(
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, gt=0, description="Limit the number of carts to retrieve"),
    min_price: float = Query(None, ge=0, description="Minimum price filter"),
    max_price: float = Query(None, ge=0, description="Maximum price filter"),
    min_quantity: int = Query(None, ge=0, description="Minimum quantity of items"),
    max_quantity: int = Query(None, ge=0, description="Maximum quantity of items"),
):
    carts = await get_carts(
        offset=offset,
        limit=limit,
        min_price=min_price,
        max_price=max_price,
        min_quantity=min_quantity,
        max_quantity=max_quantity,
    )
    return carts


@router.post(
    "/cart/{cart_id}/add/{item_id}", summary="Add an item to a cart", description="Add an item to a cart by its ID"
)
async def add_item_to_cart_route(cart_id: int, item_id: int):
    cart = await add_item_to_cart(cart_id, item_id)
    if cart is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Cart or item not found")
    return cart
