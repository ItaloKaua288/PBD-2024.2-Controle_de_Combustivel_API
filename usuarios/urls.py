from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.token, name='token'),
    path('token/validation/', views.token_validation, name='token_validation'),
    path('users/', views.usuarios_manager, name='usuarios_manager'),
    path('users/<int:pk>', views.usuario_manager, name='usuario_manager'),
]