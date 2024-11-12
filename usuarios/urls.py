from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.usuario_manager, name='usuarios_manager'),
    path('users/<int:pk>', views.usuario_manager, name='usuarios_manager'),
]