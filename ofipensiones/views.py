import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ofipensiones.auth0Backend import getRole
import logging

API_GATEWAY_URL = "http://34.67.32.234:8000"

@login_required
def home(request):
    role = getRole(request)
    return render(request, 'base.html', {'role': role})

@login_required
def consultar_logs(request):
    response = requests.get(f"{API_GATEWAY_URL}/logs")
    logs = response.json()
    return render(request, 'consultar_logs.html', {'logs': logs})

logger = logging.getLogger(__name__)

@login_required
def obtener_reportes(request):
    try:
        response = requests.get(f"{API_GATEWAY_URL}/reportes")
        response.raise_for_status()
        reportes = response.json()
        logger.info("url de la api: %s", f"{API_GATEWAY_URL}/reportes")
        logger.info("Reportes obtenidos exitosamente")
        return render(request, 'listar_reportes.html', {'reportes': reportes})
    except requests.exceptions.RequestException as e:
        logger.error(f"Error al obtener reportes: {e}")
        return render(request, 'error.html', {'error': 'No se pudieron obtener los reportes'})

@login_required
def crear_reporte(request):
    if request.method == "POST":
        data = {
            "nombre_institucion": request.POST.get("institucion"),
            "nombre_estudiante": request.POST.get("estudiante"),
            "mensualidad": request.POST.get("mensualidad"),
            "descuento": request.POST.get("descuento"),
            "fechaUltimaPago": request.POST.get("fechaUltimaPago"),
        }
        response = requests.post(f"{API_GATEWAY_URL}/reportes", json=data)
        if response.status_code == 200:
            return render(request, 'crear_reporte.html', {'success': True})
        else:
            return render(request, 'crear_reporte.html', {'error': True})
    return render(request, 'crear_reporte.html')

@login_required
def obtener_reporte_por_id(request, id):
    response = requests.get(f"{API_GATEWAY_URL}/reportes/{id}")
    if response.status_code == 200:
        reporte = response.json()
        return render(request, 'ver_reporte.html', {'reporte': reporte})
    else:
        return render(request, 'error.html', {'error': 'Reporte no encontrado'})

@login_required
def actualizar_reporte(request, id):
    if request.method == "POST":
        data = {
            "nombreInstitucion": request.POST.get("institucion"),
            "nombreEstudiante": request.POST.get("estudiante"),
            "mensualidad": request.POST.get("mensualidad"),
            "descuento": request.POST.get("descuento"),
            "fechaUltimaPago": request.POST.get("fechaUltimaPago"),
        }
        response = requests.put(f"{API_GATEWAY_URL}/reportes/{id}", json=data)
        if response.status_code == 200:
            return render(request, 'modificar_recibo.html', {'success': True, 'reporte': data})
        else:
            return render(request, 'modificar_recibo.html', {'error': True, 'reporte': data})
    else:
        response = requests.get(f"{API_GATEWAY_URL}/reportes/{id}")
        if response.status_code == 200:
            reporte = response.json()
            return render(request, 'modificar_recibo.html', {'reporte': reporte})
        else:
            return render(request, 'error.html', {'error': 'Reporte no encontrado'})

@login_required
def eliminar_reporte(request, id):
    response = requests.delete(f"{API_GATEWAY_URL}/reportes/{id}")
    if response.status_code == 204:
        return render(request, 'eliminar_reporte.html', {'success': True})
    else:
        return render(request, 'eliminar_reporte.html', {'error': True})
