from sqlalchemy import BIGINT, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from db.utils import TimeBasedModel, Base


class User(TimeBasedModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(unique=True)


class Category(TimeBasedModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)


class Product(TimeBasedModel):
    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    photo: Mapped[str] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey(Category.id), nullable=False)


metadata = Base.metadata
