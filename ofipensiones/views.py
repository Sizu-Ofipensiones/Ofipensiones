import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ofipensiones.auth0Backend import getRole

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

@login_required
def obtener_reportes(request):
    response = requests.get(f"{API_GATEWAY_URL}/reportes")
    if response.status_code == 200:
        reportes = response.json()
        return render(request, 'listar_reportes.html', {'reportes': reportes})
    else:
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
            "nombre_institucion": request.POST.get("institucion"),
            "nombre_estudiante": request.POST.get("estudiante"),
            "mensualidad": request.POST.get("mensualidad"),
            "descuento": request.POST.get("descuento"),
            "fechaUltimaPago": request.POST.get("fechaUltimaPago"),
        }
        response = requests.put(f"{API_GATEWAY_URL}/reportes/{id}", json=data)
        if response.status_code == 200:
            return render(request, 'actualizar_reporte.html', {'success': True})
        else:
            return render(request, 'actualizar_reporte.html', {'error': True})
    return render(request, 'actualizar_reporte.html')

@login_required
def eliminar_reporte(request, id):
    response = requests.delete(f"{API_GATEWAY_URL}/reportes/{id}")
    if response.status_code == 204:
        return render(request, 'eliminar_reporte.html', {'success': True})
    else:
        return render(request, 'eliminar_reporte.html', {'error': True})
