from sqlmodel import SQLModel, Field
from enum import Enum
from typing import Optional

class StatusEnum(str, Enum):
    Lost = "Lost"
    Found = "Found"
    Returned = "Returned"

class ItemBase(SQLModel):
    title: str = Field(min_length=1, description="Name/title of the item (must not be empty)")
    description: str = Field(min_length=1, description="Meaningful description of the item")
    category: str = Field(description="Category such as Electronics, Documents, Accessories, etc.")
    location: str = Field(description="Location where the item was lost/found")
    reported_by: str = Field(description="Name of the person reporting it")
    status: StatusEnum = Field(description="Lost, Found, or Returned")

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1)
    description: Optional[str] = Field(default=None, min_length=1)
    category: Optional[str] = None
    location: Optional[str] = None
    reported_by: Optional[str] = None
    status: Optional[StatusEnum] = None

