from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('consultar_logs/', views.consultar_logs, name='consultar_logs'),
    path('modificar_recibo/', views.modificar_recibo, name='modificar_recibo'),
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),
]
