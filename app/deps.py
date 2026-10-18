from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from purrfect_home.app.crud import get_cat
from purrfect_home.db.session import get_db


async def get_cat_or_404(
    cat_id: int = Path(
        ...,
        ge=1,
        description='Cat identify value'
    ),
    db: AsyncSession = Depends(get_db)
):
    cat = await get_cat(db, cat_id)
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Cat id={cat_id} not found'
        )
    return cat
