from pydantic import BaseModel, Field


class HeroSchema(BaseModel):
    id: int | None
    name: str


class HeroFilter(BaseModel):
    hero_ids: list[int]
