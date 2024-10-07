from fastapi import APIRouter, HTTPException, Query
from pydantic import ValidationError
from http import HTTPStatus
from typing import List, Optional
from shop_api.crud import create_item, get_item, get_items, update_item, patch_item, delete_item
from shop_api.models import Item, ItemCreateRequest, ItemUpdateRequest, ItemPatchRequest

router = APIRouter()


@router.post(
    "/item",
    status_code=HTTPStatus.CREATED,
    response_model=Item,
    summary="Create a new item",
    description="Create a new item in the store with name and price",
)
async def create_new_item(item: ItemCreateRequest):
    created_item = await create_item(name=item.name, price=item.price)
    return created_item


@router.get(
    "/item/{item_id}",
    response_model=Item,
    summary="Get an item by ID",
    description="Retrieve an item from the store by its ID",
)
async def get_item_by_id(item_id: int):
    item = await get_item(item_id)
    if item is None or item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    return item


@router.get(
    "/item",
    response_model=List[Item],
    summary="Get list of items",
    description="Retrieve a list of items with optional filtering by price and deletion status",
)
async def get_item_list(
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    limit: int = Query(10, gt=0, description="Limit the number of items to retrieve"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price filter"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price filter"),
    show_deleted: bool = Query(False, description="Show deleted items"),
):
    items = await get_items(
        offset=offset, limit=limit, min_price=min_price, max_price=max_price, show_deleted=show_deleted
    )
    return items


@router.put(
    "/item/{item_id}",
    response_model=Item,
    summary="Replace an item by ID",
    description="Completely replace an item in the store by its ID",
)
async def update_item_by_id(item_id: int, item: ItemUpdateRequest):
    updated_item = await update_item(item_id=item_id, name=item.name, price=item.price)
    if updated_item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    return updated_item


@router.patch(
    "/item/{item_id}",
    response_model=Item,
    summary="Partially update an item by ID",
    description="Partially update an item's name or price by its ID",
)
async def patch_item_by_id(item_id: int, item: ItemPatchRequest):
    existing_item = await get_item(item_id)

    if existing_item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")

    if existing_item.deleted:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED, detail="Item is deleted and cannot be modified")

    try:
        updated_item = await patch_item(item_id=item_id, name=item.name, price=item.price)
        return updated_item
    except ValidationError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.delete(
    "/item/{item_id}",
    status_code=HTTPStatus.OK,
    summary="Delete an item by ID",
    description="Mark an item as deleted by its ID",
)
async def delete_item_by_id(item_id: int):
    item = await delete_item(item_id)
    if item is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Item not found")
    return {"message": "Item deleted successfully"}
