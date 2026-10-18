from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from purrfect_home.models.cats import CatStatus, CatSex, AdoptionPriority


class CatBase(BaseModel):
    name: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description='Cat name',
        examples=['Tom']
    )
    age_months: int = Field(
        ...,
        ge=0,
        description='Cat age in months',
        examples=[12]
    )
    sex: CatSex = Field(
        default=CatSex.UNKNOWN,
        description='Cat sex'
    )
    description: str | None = Field(
        default=None,
        description='Cat description',
        examples=['Fat and angry']
    )
    priority: AdoptionPriority = Field(
        default=AdoptionPriority.MID,
        description='Adoption urgency'
    )


class CatSchemaIn(CatBase):
    pass


class CatSchemaOut(CatBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    status: CatStatus
    created_at: datetime
    updated_at: datetime


class CatSchemaUpdate(BaseModel):
    name: str = Field(
        default=None,
        min_length=3,
        max_length=100
    )
    age_months: int = Field(default=None, ge=0)
    sex: CatSex = None
    description: str | None = None
    status: CatStatus = None
    priority: AdoptionPriority = None
