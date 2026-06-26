from django.shortcuts import get_object_or_404
from ninja import Router
from ninja import Query
from typing import Optional
from ninja.pagination import paginate, PageNumberPagination

from .models import TravelProject, ProjectPlace
from .schemas import (
    ProjectWithPlacesIn,
    ProjectUpdateIn,
    ProjectOut,
    PlaceIn,
    PlaceOut,
    PlaceUpdateIn,
    PlaceFilter,
    ProjectFilter,
    ArtworkOut,
    ArtworkListOut,
)

from .services.art_institute import get_artwork, search_artworks

router = Router()


@router.post("/projects", response={201: ProjectOut})
def create_project(request, payload: ProjectWithPlacesIn):
    if len(payload.places) < 1:
        return 400, {"detail": "Project must have at least 1 place"}

    if len(payload.places) > 10:
        return 400, {"detail": "Maximum 10 places per project"}
    
    project = TravelProject.objects.create(
        name=payload.name,
        description=payload.description,
        start_date=payload.start_date,
    )

    for place in payload.places:
        artwork = get_artwork(place.external_id)
        if not artwork:
            project.delete()
            return 400, {"detail": f"Artwork {place.external_id} not found in Art Institute API"}

        ProjectPlace.objects.create(
            project=project,
            external_id=artwork.id,
            title=artwork.title,
        )

    return 201, project


@router.get("/projects", response=list[ProjectOut])
@paginate(PageNumberPagination)
def list_projects(request, filters: ProjectFilter = Query(...)):
    qs = TravelProject.objects.prefetch_related("places").all()
    if filters.is_completed is not None:
        qs = qs.filter(is_completed=filters.is_completed)
    return qs

@router.get("/projects/{project_id}", response=ProjectOut)
def get_project(request, project_id: int):
    return get_object_or_404(TravelProject, id=project_id)


@router.patch("/projects/{project_id}", response=ProjectOut)
def update_project(request, project_id: int, payload: ProjectUpdateIn):
    project = get_object_or_404(TravelProject, id=project_id)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(project, attr, value)
    project.save()

    return project


@router.delete("/projects/{project_id}", response={204: None, 400: dict})
def delete_project(request, project_id: int):
    project = get_object_or_404(TravelProject, id=project_id)

    if project.places.filter(is_visited=True).exists():
        return 400, {"detail": "Cannot delete project with visited places"}

    project.delete()
    return 204, None



@router.post("/projects/{project_id}/places", response={201: PlaceOut, 400: dict})
def add_place(request, project_id: int, payload: PlaceIn):
    project = get_object_or_404(TravelProject, id=project_id)

    if project.places.count() >= 10:
        return 400, {"detail": "Maximum 10 places per project"}

    if project.places.filter(external_id=payload.external_id).exists():
        return 400, {"detail": "Place already exists in this project"}

    artwork = get_artwork(payload.external_id)
    if not artwork:
        return 400, {"detail": f"Artwork {payload.external_id} not found in Art Institute API"}

    place = ProjectPlace.objects.create(
        project=project,
        external_id=artwork.id,
        title=artwork.title,
    )

    if project.is_completed:
        project.is_completed = False
        project.save()

    return 201, place


@router.get("/projects/{project_id}/places", response=list[PlaceOut])
@paginate(PageNumberPagination)
def list_places(request, project_id: int, filters: PlaceFilter = Query(...)):
    project = get_object_or_404(TravelProject, id=project_id)
    qs = project.places.all()
    if filters.is_visited is not None:
        qs = qs.filter(is_visited=filters.is_visited)
    return qs


@router.get("/projects/{project_id}/places/{place_id}", response=PlaceOut)
def get_place(request, project_id: int, place_id: int):
    return get_object_or_404(ProjectPlace, id=place_id, project_id=project_id)


@router.patch("/projects/{project_id}/places/{place_id}", response=PlaceOut)
def update_place(request, project_id: int, place_id: int, payload: PlaceUpdateIn):
    place = get_object_or_404(ProjectPlace, id=place_id, project_id=project_id)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(place, attr, value)
    place.save()

    project = place.project
    if project.places.filter(is_visited=False).count() == 0:
        project.is_completed = True
        project.save()

    return place


@router.get("/artworks", response={200: ArtworkListOut, 400: dict})
def search_artworks_endpoint(request, q: str, limit: int = 10, offset: int = 0):
    if limit > 100:
        return 400, {"detail": "Maximum limit is 100"}
    return 200, search_artworks(q, limit, offset)