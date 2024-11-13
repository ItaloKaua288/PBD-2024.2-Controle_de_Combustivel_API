from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, AbstractBaseUser, BaseUserManager, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.authtoken.models import TokenProxy
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.apps import apps

class CustomUserManager(BaseUserManager):
    def _create_user(self, usuario, password, **extra_fields):
        if not usuario:
            raise ValueError("The given usuario must be set")
        GlobalUserModel = apps.get_model(
            self.model._meta.app_label, self.model._meta.object_name
        )
        usuario = GlobalUserModel.normalize_username(usuario)
        user = self.model(usuario=usuario, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, usuario, password=None, **extra_fields):
        return self._create_user(usuario, password, **extra_fields)

    def create_superuser(self, usuario, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(usuario, password, **extra_fields)
  

class Usuarios(AbstractBaseUser, PermissionsMixin):
    cargo_choices = (('A', 'Admnistrador'), ('M', 'Motorista'))
    cargo = models.CharField(max_length=1, choices=cargo_choices, null=False, blank=False, default='M')
    username = models.CharField(max_length=150, unique=True, null=False, validators=[UnicodeUsernameValidator()], error_messages={'unique': 'Usuario já existe'})
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = ("usuario")
        verbose_name_plural = ("usuarios")

    @property
    def is_staff(self):
        return self.is_superuser
    objects = CustomUserManager()


@receiver(post_save, sender=Usuarios)
def create_token(sender, instance:Usuarios, created, **kwargs):
    if created and instance.cargo == 'A':
        token = TokenProxy(user=instance)
        token.save()
post_save.connect(create_token, sender=Usuarios)