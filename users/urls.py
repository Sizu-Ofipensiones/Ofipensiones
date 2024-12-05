from django.urls import path
from .views import get_all_users, create_user

urlpatterns = [
    path('usuarios/', get_all_users, name='get_all_users'),  # GET /usuarios/
    path('usuarios/create/', create_user, name='create_user'),  # POST /usuarios/create/
]
