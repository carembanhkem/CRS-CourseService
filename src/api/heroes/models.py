from sqlmodel import Column, Field, SQLModel
import sqlalchemy.dialects.postgresql as pg


class Hero(SQLModel, table=True):
    __tablename__ = "heroes"

    id: int | None = Field(
        sa_column=Column(pg.INTEGER, nullable=False, primary_key=True)
    )
    name: str = Field(alias="localized_name")
