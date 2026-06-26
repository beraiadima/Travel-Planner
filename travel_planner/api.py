from ninja import NinjaAPI
from trips.views import router as trips_router

api = NinjaAPI()
api.add_router("/trips", trips_router, tags=["Trips"])