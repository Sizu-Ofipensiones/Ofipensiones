from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # Ruta para el panel de administración
    path('admin/', admin.site.urls),

    # Ruta para la página de inicio
    path('', views.home, name='home'),

    # Rutas para autenticación de usuarios (login, logout, etc.)
    path('auth/', include('django.contrib.auth.urls')),

    # Rutas para autenticación con Social Auth (auth0, por ejemplo)
    path('auth/', include('social_django.urls')),
]
