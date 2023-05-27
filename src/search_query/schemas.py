from datetime import datetime

from src.schemas import BaseModel

from pydantic import UUID4, constr


class SearchQueryRead(BaseModel):
    id: UUID4
    text_query: str
    created_at: datetime

class SearchQueryString(BaseModel):
    text_query: constr(strip_whitespace=True, min_length=2, max_length=255, to_lower=True)