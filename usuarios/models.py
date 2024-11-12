from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import TokenProxy
from django.db.models.signals import post_save
from django.dispatch import receiver

class Usuarios(AbstractUser):
    cargo_choices = (('A', 'Admnistrador'), ('M', 'Motorista'))
    cpf = models.CharField(max_length=11, null=False, blank=False)
    cargo = models.CharField(max_length=1, choices=cargo_choices, null=False, blank=False, default='M')

@receiver(post_save, sender=Usuarios)
def create_token(sender, instance:Usuarios, created, **kwargs):
    if created and instance.cargo == 'A':
        token = TokenProxy(user=instance)
        token.save()
post_save.connect(create_token, sender=Usuarios)