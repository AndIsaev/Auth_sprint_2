from pydantic import BaseModel

from models.mixin import BaseModelMixin, PaginationMixin


class ElasticGenre(BaseModel):
    id: str
    name: str


class FilmGenre(BaseModelMixin):
    """Schema for Film work detail"""

    name: str


class DetailResponseGenre(FilmGenre):
    """Schema for Genre detail"""

    # film_ids: Optional[list[UUID]] = []


class GenrePagination(PaginationMixin):
    genres: list[FilmGenre] = []
