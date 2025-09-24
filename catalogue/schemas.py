from pydantic import BaseModel, ConfigDict


class Manufacturer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class Category(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class Model(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class Part(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    number: str
    name: str | None


class Meta(BaseModel):
    current_page: int
    page_count: int


class ManufacturersResponse(BaseModel):
    meta: Meta
    manufacturers: list[Manufacturer]


class CategoriesResponse(BaseModel):
    meta: Meta
    categories: list[Category]


class ModelsResponse(BaseModel):
    meta: Meta
    models: list[Model]


class PartsResponse(BaseModel):
    meta: Meta
    parts: list[Part]
