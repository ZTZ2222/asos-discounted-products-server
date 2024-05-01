from fastapi import FastAPI, HTTPException, status
from schemas.schemas import SProduct

from ..services.services import select_products

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/products", response_model=list[SProduct], status_code=status.HTTP_200_OK)
async def get_products(offset: int = 0, limit: int = 20):

    result = await select_products(offset=offset, limit=limit)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"There is no product in the database",
        )
    return result


# offset: int = 0, limit: int = 20
