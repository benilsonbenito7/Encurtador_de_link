from datetime import timedelta
from ninja import ModelSchema, Schema
from ..models import Links

class LinkInput(ModelSchema):
    class Meta:
        model = Links
        fields = ['redirect_link', 'token', 'expiration_time', 'max_uniques_cliques']
        
class LinkOutput(ModelSchema):
    expiration_time: str | None

    class Meta:
        model = Links
        fields = [
            "redirect_link",
            "token",
            "expiration_time",
            "max_uniques_cliques",
        ]

    @staticmethod
    def resolve_expiration_time(obj):
        if obj.expiration_time is None:
            return None

        total_seconds = int(obj.expiration_time.total_seconds())

        days, remainder = divmod(total_seconds, 86400)
        hours, remainder = divmod(remainder, 3600)
        minutes, _ = divmod(remainder, 60)

        parts = []

        if days:
            parts.append(f"{days} {'dia' if days == 1 else 'dias'}")

        if hours:
            parts.append(f"{hours} {'hora' if hours == 1 else 'horas'}")

        if minutes:
            parts.append(f"{minutes} {'minuto' if minutes == 1 else 'minutos'}")

        return ", ".join(parts) if parts else "0 minutos"

class UpdateSchemas(Schema):
    redirect_link: str | None = None
    token: str | None = None
    expiration_time: timedelta | None = None
    max_uniques_cliques: int | None = None