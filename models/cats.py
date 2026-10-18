import enum
from sqlalchemy import String, Text
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from purrfect_home.db.base import TimeStampMixin, Base


class CatStatus(str, enum.Enum):
    AVAILABLE = 'available'
    RESERVED = 'reserved'
    ADOPTED = 'adopted'
    WITHDRAWN = 'withdrawn'


class AdoptionPriority(str, enum.Enum):
    LOW = 'low'
    MID = 'mid'
    HIGH = 'high'
    URGENT = 'urgent'


class CatSex(str, enum.Enum):
    MALE = 'male'
    FEMALE = 'female'
    UNKNOWN = 'unknown'


class Cat(TimeStampMixin, Base):
    __tablename__ = 'cats'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    age_months: Mapped[int] = mapped_column()
    sex: Mapped[CatSex] = mapped_column(
        SAEnum(CatSex, max_length=7, native_enum=False),
        nullable=False,
        default=CatSex.UNKNOWN
    )
    description: Mapped[str | None] = mapped_column(Text)
    status: Mapped[CatStatus] = mapped_column(
        SAEnum(CatStatus, max_length=9, native_enum=False),
        nullable=False,
        default=CatStatus.AVAILABLE
    )
    priority: Mapped[AdoptionPriority] = mapped_column(
        SAEnum(AdoptionPriority, max_length=6, native_enum=False),
        nullable=False,
        default=AdoptionPriority.MID
    )

    def __repr__(self) -> str:
        return f'<Cat id={self.id} name={self.name} status={self.status}>'
