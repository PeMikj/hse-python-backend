from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query
from ..cart.contracts import CartResponse
from ...store import queries
from starlette.responses import Response

router = APIRouter(prefix="/cart")


@router.get(
    "/{cart_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=CartResponse,
)
async def get_cart(cart_id: int) -> CartResponse:
    try:
        cart = queries.get_cart(cart_id)
        if cart is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Cart not found"
            )
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return cart


@router.get(
    "/",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return",
        },
    },
    status_code=HTTPStatus.OK,
    response_model=List[CartResponse],
)
async def get_carts(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, gt=0),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    min_quantity: Optional[int] = Query(None, ge=0),
    max_quantity: Optional[int] = Query(None, ge=0),
) -> List[CartResponse]:
    try:
        carts = queries.get_carts(
            offset, limit, min_price, max_price, min_quantity, max_quantity
        )
        if carts is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail="Carts not found"
            )
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return carts


@router.post(
    "/",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully created",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to create",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=CartResponse,
)
async def create_cart(response: Response) -> CartResponse:
    try:
        cart = queries.create_cart()
        response.headers["location"] = f"/cart/{cart.id}"
        return cart
    except ValueError as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))


@router.post(
    "/{cart_id}/add/{item_id}",
    responses={
        HTTPStatus.CREATED: {
            "description": "Successfully added",
        },
        HTTPStatus.UNPROCESSABLE_ENTITY: {
            "description": "Failed to add",
        },
    },
    status_code=HTTPStatus.CREATED,
    response_model=CartResponse,
)
async def add_item_to_cart(cart_id: int, item_id: int) -> CartResponse:
    try:
        cart = queries.add_item_to_cart(cart_id, item_id)
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail=str(e))
    return cart
