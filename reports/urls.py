from django.urls import path
from .views import ReportDetailView, ReportCreateView

urlpatterns = [
    path('report/<int:pk>/', ReportDetailView.as_view(), name='report_detail'),  # Ver detalles de un usuario
    path('report/new/', ReportCreateView.as_view(), name='report_create'),  # Crear un nuevo usuario
]
