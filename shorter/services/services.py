from ..models import Links, Clicks
# pyrefly: ignore [missing-import]
from django.shortcuts import get_object_or_404, redirect

class RedirectService:

    @staticmethod
    def create_link(data):
        data = data.model_dump()
        token = data['token']
        
        if token and Links.objects.filter(token=token).exists():
            return 409, {'error': f'O token {token} ja foi utilizado'}
        link = Links(**data)
        link.save()
        
        return 200, link

    @staticmethod
    def get_link(token, request):
        link = get_object_or_404(Links, token=token)
        if not link.active:
            return 410, {'error': 'Link desativado'}
        if link.expired():
            return 410, {'error': 'Link expirado'}
       
        uniques_clicks = Clicks.objects.filter(link=link).values('ip').distinct().count()
        if link.max_uniques_cliques and uniques_clicks >= link.max_uniques_cliques:
            return 403, {'error': 'Limite de cliques atingido'}
        
        click = Clicks(
            link=link,
            ip=request.META.get("REMOTE_ADDR")
        )
        click.save()
        
        return redirect(link.redirect_link)
    
    @staticmethod
    def update_link(link_id, link_schemas):
        link = get_object_or_404(Links, id=link_id)
        data = link_schemas.model_dump(exclude_unset=True, exclude_none=True)
        
        token = data.get('token')

        if token and Links.objects.filter(token=token).exclude(id=link_id).exists():
            return 409, {'error': f'O token {token} ja foi utilizado'}

        for chave, valor in data.items():
            setattr(link, chave, valor)
        link.save()

        return 200, link
    
    @staticmethod
    def statistics(link_id):
        link = get_object_or_404(Links, id=link_id)
        return 200, {
            'total_clicks': Clicks.objects.filter(link=link).count(),
            'uniques_clicks': Clicks.objects.filter(link=link).values('ip').distinct().count(),
            'link': link.redirect_link
        }