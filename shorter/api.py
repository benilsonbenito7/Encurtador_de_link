from ninja import Router
from .schemas.schemas import LinkInput, LinkOutput
from .models import Links
from .services.services import RedirectService

sh_router = Router(tags=["Rotas do encurtador"])

@sh_router.post('create/', response = {200: LinkOutput, 409: dict})
def create(request, link_schema: LinkInput):
    return RedirectService.create_link(link_schema)