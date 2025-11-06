from pydantic import BaseModel
from typing import Optional

class Pagination(BaseModel):
    limit: int = 50
    offset: int = 0

class IdResponse(BaseModel):
    id: str
