import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ofipensiones.auth0Backend import getRole
import logging
from django.views.decorators.http import require_http_methods
import time


API_GATEWAY_URL = "http://35.225.182.131:8000"

@login_required
def home(request):
    role = getRole(request)
    return render(request, 'base.html', {'role': role})

@login_required
def consultar_logs(request):
    try:
        response = requests.get(f"{API_GATEWAY_URL}/logs")
        response.raise_for_status()  # Verifica si la respuesta tiene un error HTTP
        logs = response.json()
        return JsonResponse(logs, safe=False)  # Muestra el JSON directamente
    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": str(e)}, status=500)

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
@require_http_methods(["GET", "POST"])
def actualizar_reporte(request, id):
    if request.method == "POST":
        data = {
            "nombreInstitucion": request.POST.get("institucion"),
            "nombreEstudiante": request.POST.get("estudiante"),
            "mensualidad": request.POST.get("mensualidad"),
            "descuento": request.POST.get("descuento"),
            "fechaUltimaPago": request.POST.get("fechaUltimaPago"),
        }
        try:
            response = requests.put(f"{API_GATEWAY_URL}/reportes/{id}", json=data)
            response.raise_for_status()
            reporte = response.json()
            logger.info("Reporte actualizado exitosamente: %s", reporte)
            return render(request, 'modificar_recibo.html', {'success': True, 'reporte': reporte})
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al actualizar reporte: {e}")
            return render(request, 'modificar_recibo.html', {'error': True, 'reporte': data})
    else:
        try:
            response = requests.get(f"{API_GATEWAY_URL}/reportes/{id}")
            response.raise_for_status()
            reporte = response.json()
            logger.info("Reporte obtenido para actualización: %s", reporte)
            return render(request, 'modificar_recibo.html', {'reporte': reporte})
        except requests.exceptions.RequestException as e:
            logger.error(f"Error al obtener reporte: {e}")
            return render(request, 'error.html', {'error': 'Reporte no encontrado'})

@login_required
def eliminar_reporte(request, id):
    response = requests.delete(f"{API_GATEWAY_URL}/reportes/{id}")
    if response.status_code == 204:
        return render(request, 'eliminar_reporte.html', {'success': True})
    else:
        return render(request, 'eliminar_reporte.html', {'error': True})

@login_required
def obtener_usuarios(request):
    try:
        response = requests.get(f"{API_GATEWAY_URL}/usuarios/")
        response.raise_for_status()
        usuarios = response.json()
        return render(request, 'listar_usuarios.html', {'usuarios': usuarios})
    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error': 'No se pudieron obtener los usuarios'})
    

@login_required
def prueba_carga_usuarios(request):
    try:
        total_requests = 1000
        total_time = 0

        # Hacer 1000 solicitudes
        for _ in range(total_requests):
            start_time = time.time()  # Marca el inicio de la solicitud
            response = requests.get(f"{API_GATEWAY_URL}/usuarios/")
            total_time += (time.time() - start_time)  # Suma el tiempo de respuesta de la solicitud

        # Calcula el tiempo promedio
        average_time = total_time / total_requests
        return JsonResponse({"message": f"Prueba de carga completada. Tiempo promedio de respuesta: {average_time:.4f} segundos."})

    except requests.exceptions.RequestException as e:
        return JsonResponse({"error": f"Error durante la prueba de carga: {str(e)}"}, status=500)