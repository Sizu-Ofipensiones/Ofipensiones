from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('consultar_logs/', views.consultar_logs, name='consultar_logs'),
    path('actualizar_reporte/<int:id>/', views.actualizar_reporte, name='actualizar_reporte'),
    path('listar_reportes/', views.obtener_reportes, name='listar_reportes'),
    path('listar_usuarios/', views.obtener_usuarios, name='listar_usuarios'),
    path('prueba-carga-usuarios/', views.prueba_carga_usuarios, name='prueba_carga_usuarios'),
    path(r'', include('django.contrib.auth.urls')),
    path(r'', include('social_django.urls')),
]
