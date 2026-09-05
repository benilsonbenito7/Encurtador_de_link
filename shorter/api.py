from ninja import Router

sh_router = Router(tags=["Rotas do encurtador"])

@sh_router.get('create/')
def create(request):
    return {'message': 'ok'}