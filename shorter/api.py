from ninja import Router
from .schemas.schemas import LinkInput, LinkOutput, UpdateSchemas
from .models import Links
from .services.services import RedirectService

sh_router = Router(tags=["Rotas do encurtador"])

@sh_router.post('create/', response = {200: LinkOutput, 409: dict})
def create(request, link_schema: LinkInput):
    return RedirectService.create_link(link_schema)

@sh_router.get("/{token}", response = {200: None, 410: dict, 403: dict})
def get_link(request, token):
    return RedirectService.get_link(token, request)

@sh_router.patch("/{link_id}/", response={200: UpdateSchemas, 409: dict, 410: dict, 403: dict})
def update_link(request, link_id: int, link_schema: UpdateSchemas):
    return RedirectService.update_link(link_id, link_schema)


@sh_router.get("/statistics/{link_id}/", response={200: dict, 404: dict})
def statistica(request, link_id: int):
    return RedirectService.statistics(link_id)