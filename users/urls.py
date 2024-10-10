from django.urls import path
from .views import UserListView, UserDetailView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),  # Listar usuarios
    path('user/<int:pk>/', UserDetailView.as_view(), name='user_detail'),  # Ver detalles de un usuario
    path('user/new/', UserCreateView.as_view(), name='user_create'),  # Crear un nuevo usuario
    path('user/<int:pk>/edit/', UserUpdateView.as_view(), name='user_update'),  # Actualizar un usuario
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),  # Eliminar un usuario
]
