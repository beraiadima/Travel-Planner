from datetime import date, datetime
from typing import Optional
from ninja import Schema


class ProjectIn(Schema):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None


class PlaceIn(Schema):
    external_id: int


class ProjectWithPlacesIn(Schema):
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    places: list[PlaceIn] = []


class ProjectUpdateIn(Schema):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None


class PlaceUpdateIn(Schema):
    notes: Optional[str] = None
    is_visited: Optional[bool] = None


class PlaceOut(Schema):
    id: int
    external_id: int
    title: str
    notes: Optional[str] = None
    is_visited: bool
    created_at: datetime


class ProjectOut(Schema):
    id: int
    name: str
    description: Optional[str] = None
    start_date: Optional[date] = None
    is_completed: bool
    created_at: datetime
    places: list[PlaceOut] = []


class PlaceFilter(Schema):
    is_visited: Optional[bool] = None


class ProjectFilter(Schema):
    is_completed: Optional[bool] = None


class ArtworkOut(Schema):
    id: int
    title: str


class ArtworkListOut(Schema):
    total: int
    items: list[ArtworkOut]