import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tu_proyecto.settings')
django.setup()

from users.models import User

# Crear 10 nuevos usuarios
for i in range(1, 11):
    user = User(
        name=f'Usuario{i}',
        email=f'usuario{i}@ejemplo.com',
        password='password123',
        position='Empleado'
    )
    user.save()
    print(f'Usuario {user.name} creado exitosamente.')