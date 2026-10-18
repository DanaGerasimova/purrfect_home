from purrfect_home.schemas.cat import (
    CatSchemaIn, CatSchemaOut, CatSchemaUpdate
)
from purrfect_home.models.cats import Cat, CatStatus, AdoptionPriority
from purrfect_home.app.crud import (
    create_cat, get_cats_list, update_cat, delete_cat
)
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from purrfect_home.app.deps import get_cat_or_404
from purrfect_home.db.session import get_db


router = APIRouter(prefix='/cats', tags=['cats'])


@router.post(
    "",
    response_model=CatSchemaOut,
    status_code=status.HTTP_201_CREATED,
    summary='Create a cat'
)
async def create(
    payload: CatSchemaIn,
    db: AsyncSession = Depends(get_db)
):
    return await create_cat(db, payload)


@router.get(
    "",
    response_model=list[CatSchemaOut],
    status_code=status.HTTP_200_OK,
    summary='Get a list of cats'
)
async def get_list(
    db: AsyncSession = Depends(get_db),
    status_filter: CatStatus | None = Query(
        default=None,
        alias='status',
        description='Filter by cat status'
    ),
    priority_filter: AdoptionPriority | None = Query(
        default=None,
        alias='priority',
        description='Filter by adoption priority'
    ),
    limit: int = Query(default=30, ge=1, le=100, description='Limit per page')
):
    return await get_cats_list(
        db,
        status=status_filter,
        priority=priority_filter,
        limit=limit
    )


@router.get(
    "/{cat_id}",
    response_model=CatSchemaOut,
    status_code=status.HTTP_200_OK,
    summary='Get a cat'
)
async def get(
    cat: Cat = Depends(get_cat_or_404)
):
    return cat


@router.patch(
    "/{cat_id}",
    response_model=CatSchemaOut,
    status_code=status.HTTP_200_OK,
    summary='Update a cat'
)
async def update(
    payload: CatSchemaUpdate,
    cat: Cat = Depends(get_cat_or_404),
    db: AsyncSession = Depends(get_db)
):
    return await update_cat(db, cat, payload)


@router.delete(
    "/{cat_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete a cat'
)
async def delete(
    cat: Cat = Depends(get_cat_or_404),
    db: AsyncSession = Depends(get_db)
):
    return await delete_cat(db, cat)
