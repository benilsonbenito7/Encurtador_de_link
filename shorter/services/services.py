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
        if link.expired():
            return 410, {'error': 'Link expirado'}
       
        uniques_clicks = Clicks.objects.filter(link=link).values('ip')
        print(uniques_clicks)
        
        click = Clicks(
            link=link,
            ip=request.META.get("REMOTE_ADDR")
        )
        click.save()
        
        return redirect(link.redirect_link)
    