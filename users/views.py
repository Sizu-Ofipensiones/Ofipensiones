from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from users.models import User
import json

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def create_user(request):
    """Crear un usuario en la base de datos"""
    try:
        # Verificar el cuerpo de la solicitud
        logger.info(f"Body de la solicitud: {request.body}")
        
        # Decodificar el cuerpo
        data = json.loads(request.body.decode('utf8'))
        logger.info(f"Datos decodificados: {data}")
        
        # Crear el usuario
        user = User(name=data['name'], email=data['email'], password=data['password'], position=data['position'])
        user.save()

        return JsonResponse({'message': f'Usuario {user.name} creado exitosamente.'})

    except json.JSONDecodeError as e:
        return JsonResponse({'error': 'Error al procesar JSON: ' + str(e)}, status=400)
    except KeyError as e:
        return JsonResponse({'error': f"Falta el campo requerido: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse({'error': 'Error interno del servidor: ' + str(e)}, status=500)

@csrf_exempt
@require_http_methods(["PUT"])
def update_user(request, id):
    """Actualizar un usuario existente"""
    data = json.loads(request.body.decode('utf8'))
    try:
        user = User.objects.get(id=id)
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.position = data.get('position', user.position)
        user.save()
        return JsonResponse({'message': f'Usuario {user.name} actualizado exitosamente.'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
def delete_user(request, id):
    """Eliminar un usuario de la base de datos"""
    try:
        user = User.objects.get(id=id)
        user.delete()
        return JsonResponse({'message': f'Usuario {user.name} eliminado exitosamente.'})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_user(request, id):
    """Obtener la información de un usuario específico"""
    try:
        user = User.objects.get(id=id)
        user_data = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'position': user.position
        }
        return JsonResponse(user_data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)
    
@csrf_exempt
@require_http_methods(["GET"])
def get_all_users(request):
    """Obtener la información de todos los usuarios"""
    users = User.objects.all()
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email, 'position': user.position} for user in users]
    return JsonResponse(users_data, safe=False)