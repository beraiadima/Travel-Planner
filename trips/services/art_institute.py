from django.core.cache import cache
import requests
from dataclasses import dataclass

ARTIC_BASE_URL = "https://api.artic.edu/api/v1"


@dataclass
class ArtworkData:
    id: int
    title: str


def get_artwork(external_id: int) -> ArtworkData | None:
    cache_key = f"artwork_{external_id}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    url = f"{ARTIC_BASE_URL}/artworks/{external_id}"
    response = requests.get(url, params={"fields": "id,title"}, timeout=10)

    if response.status_code == 404:
        return None

    response.raise_for_status()
    data = response.json()["data"]
    result = ArtworkData(id=data["id"], title=data["title"])
    cache.set(cache_key, result)
    return result


def search_artworks(query: str, limit: int = 10, offset: int = 0) -> dict:
    cache_key = f"search_{query}_{limit}_{offset}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    url = f"{ARTIC_BASE_URL}/artworks/search"
    params = {
        "q": query,
        "fields": "id,title",
        "limit": limit,
        "from": offset,
    }
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    result = {
        "total": data["pagination"]["total"],
        "items": [ArtworkData(id=item["id"], title=item["title"]) for item in data["data"]],
    }
    cache.set(cache_key, result)
    return result