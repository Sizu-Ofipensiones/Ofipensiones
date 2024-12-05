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
def modificar_recibo(request):
    if request.method == "POST":
        data = {
            "institucion": request.POST.get("institucion"),
            "estudiante": request.POST.get("estudiante"),
            "valor": request.POST.get("valor"),
            "inscripcion": request.POST.get("inscripcion"),
        }
        response = requests.post(f"{API_GATEWAY_URL}/recibos", json=data)
        if response.status_code == 200:
            return render(request, 'modificar_recibo.html', {'success': True})
        else:
            return render(request, 'modificar_recibo.html', {'error': True})
    return render(request, 'modificar_recibo.html')