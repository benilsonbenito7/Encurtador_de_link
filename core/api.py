from ninja import NinjaAPI
from shorter.api import sh_router

api = NinjaAPI()

api.add_router("v1/", sh_router)