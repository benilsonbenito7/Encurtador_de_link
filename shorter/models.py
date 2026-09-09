from django.db import models
from secrets import token_urlsafe
from django.utils import timezone

class Links(models.Model):
    redirect_link = models.URLField()
    token = models.CharField(max_length=20, unique=True, null=True, blank=True)
    creat_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DurationField(null=True, blank=True) #PT2H ou PT3D e em ISO 8601
    max_uniques_cliques = models.PositiveIntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.redirect_link
    
    def save(self, *args, **kwargs):
        if not self.token:
            while True:
                self.token = token_urlsafe(8)
                if not Links.objects.filter(token=self.token).exists():
                    break
        super().save(*args, **kwargs)
    
    def expired(self):
        if not self.expiration_time:
            return False
        return timezone.now() > self.creat_at + self.expiration_time
    
class Clicks(models.Model):
    link = models.ForeignKey(Links, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f"{self.ip} - {self.created_at}"