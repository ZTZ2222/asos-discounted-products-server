from typing import Sequence
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.product import ProductOrm
from src.schemas.product import SProduct
from src.services.product import select_products

router = APIRouter(prefix="/products", tags=["Products Endpoint"])

# temp staff_only
staff_only = "staff_only"


@router.post(
    "/",
    response_model=SProduct,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(staff_only)],
)
async def create_product(payload: SProduct, db_session: AsyncSession = Depends(get_db)):
    """
    Creates a new product.

    Args:
        payload (SProduct): The payload containing the product information.
        db_session (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        ProductOrm: The created product.

    Raises:
                                HTTPException: If there is an error during the save operation. The exception will have a status code of 422 and the detail will be the representation of the SQLAlchemyError.
    """
    product = ProductOrm(**payload.model_dump())
    await product.save(db_session)
    return product


@router.put(
    "/",
    response_model=SProduct,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(staff_only)],
)
async def update_product(payload: SProduct, db_session: AsyncSession = Depends(get_db)):
    """
    Updates a product in the database.

    Args:
        payload (SProduct): The payload containing the updated product information.
        db_session (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        SProduct: The updated product.

    Raises:
        HTTPException: If there is an error during the update operation. The exception will have a status code of 422 and the detail will be the representation of the SQLAlchemyError.
    """
    product = ProductOrm(**payload.model_dump())
    await product.update(db_session, **product.as_dict())
    return product


@router.delete("/", status_code=status.HTTP_200_OK, dependencies=[Depends(staff_only)])
async def delete_product(payload: SProduct, db_session: AsyncSession = Depends(get_db)):
    """
    Deletes a product from the database.

    Args:
        payload (SProduct): The payload containing the slug of the product to be deleted.
        db_session (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        dict: A dictionary containing the detail message indicating the success of the deletion.

    Raises:
        HTTPException: If no product is found with the given slug.

    Dependencies:
        - staff_only: A dependency that ensures the user is a staff member.

    Status Code:
        - 200: If the product is successfully deleted.

    """

    product = await ProductOrm.find(db_session, slug=payload.slug)
    await product.delete(db_session)

    return {
        "detail": f"Product with slug: {payload.slug} has been successfully deleted"
    }


@router.get("/{product_slug}", response_model=SProduct, status_code=status.HTTP_200_OK)
async def get_product(product_slug: str, db_session: AsyncSession = Depends(get_db)):
    """
    Retrieves a product from the database based on its slug.

    Args:
        product_slug (str): The slug of the product to retrieve.
        db_session (AsyncSession, optional): The database session. Defaults to Depends(get_db).

    Returns:
        SProduct: The retrieved product.

    Raises:
        HTTPException: If no product is found with the given slug.

    Status Code:
        200: If the product is successfully retrieved.
    """

    product = await ProductOrm.find(db_session, slug=product_slug)
    return product


@router.get("/", response_model=Sequence[SProduct], status_code=status.HTTP_200_OK)
async def get_all_products(
    offset: int = 0,
    limit: int = 20,
):
    """
    Retrieves all products from the database with pagination.

    Args:
        offset (int): The number of records to skip. Defaults to 0.
        limit (int): The maximum number of records to return. Defaults to 20.

    Returns:
        Sequence[SProduct]: A sequence of SProduct objects representing the retrieved products.

    Raises:
        HTTPException: If no products are found in the database.

    Status Code:
        - 200: If the products are successfully retrieved.
        - 404: If no products are found in the database.
    """

    result = await select_products(offset=offset, limit=limit)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Products do not exist"
        )
    return result
