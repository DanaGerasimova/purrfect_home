from purrfect_home.models.cats import Cat, CatStatus, AdoptionPriority
from purrfect_home.schemas.cat import CatSchemaIn, CatSchemaUpdate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_cat(db: AsyncSession, payload: CatSchemaIn):
    cat = Cat(**payload.model_dump())
    db.add(cat)
    await db.flush()
    await db.refresh(cat)
    return cat


async def get_cat(db: AsyncSession, cat_id: int):
    return await db.get(Cat, cat_id)


async def get_cats_list(
    db: AsyncSession,
    *,
    status: CatStatus,
    priority: AdoptionPriority,
    limit: int = 30
):
    conditions = []
    if status is not None:
        conditions.append(Cat.status == status)
    if priority is not None:
        conditions.append(Cat.priority == priority)

    cats_raw = (
        select(Cat)
        .where(*conditions)
        .order_by(Cat.created_at.desc())
        .limit(limit)
    )

    cats = (await db.execute(cats_raw)).scalars().all()
    return cats


async def update_cat(db: AsyncSession, cat: Cat, payload: CatSchemaUpdate):
    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(cat, field, value)
    await db.flush()
    await db.refresh(cat)
    return cat


async def delete_cat(db: AsyncSession, cat: Cat):
    await db.delete(cat)
    await db.flush()
