from pydantic import BaseModel
from typing import Optional, List


class ItemBase(BaseModel):
    title: str
    content: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True

class ValidateRequest(BaseModel):
    title: str
    description: Optional[str] = None


class ErrorDetail(BaseModel):
    field: str
    message: str


class ValidateResponse(BaseModel):
    valid: bool
    slug: Optional[str] = None
    warnings: Optional[List[str]] = None
    errors: Optional[List[ErrorDetail]] = None

