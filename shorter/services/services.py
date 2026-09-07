from ..models import Links, Clicks

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
