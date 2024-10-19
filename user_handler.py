import os
import django
import pika
import json

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ofipensiones.settings')
django.setup()

from users.models import User  # Importar el modelo User de Django

def callback_user(ch, method, properties, body):
    """Callback que procesa las solicitudes relacionadas con usuarios"""
    payload = json.loads(body.decode('utf8')) # Decodificar el mensaje
    action = payload.get('action') # Obtener la acción a realizar

    if action == 'create':
        create_user(payload)
    elif action == 'update':
        update_user(payload)
    elif action == 'delete':
        delete_user(payload)

    print(f"Procesando {action} para el usuario: {payload.get('name')}")

#---------------------------------------- Funciones para realizar las operaciones CRUD de usuarios------------------------------------

#Crear un usuario
def create_user(data):
    """Crear un usuario en la base de datos"""
    user = User(name=data['name'], email=data['email'], password=data['password'], position=data['position'])
    user.save()#Guardar el usuario en la base de datos
    print(f"Usuario {user.name} creado exitosamente.")

#Actualizar un usuario
def update_user(data):
    """Actualizar un usuario existente"""
    try:
        user = User.objects.get(id=data['id'])
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.position = data.get('position', user.position)
        user.save() #Guardar los cambios en la base de datos
        print(f"Usuario {user.name} actualizado exitosamente.")
    except User.DoesNotExist:
        print("Usuario no encontrado.")

#Eliminar un usuario
def delete_user(data):
    """Eliminar un usuario de la base de datos"""
    try:
        user = User.objects.get(id=data['id'])
        user.delete()# Eliminar el usuario de la base de datos
        print(f"Usuario {user.name} eliminado exitosamente.")
    except User.DoesNotExist:
        print("Usuario no encontrado.")

#---------------------------------------- Función para iniciar el manejador de usuarios------------------------------------

def start_user_handler():
    """Iniciar el manejador de usuarios que escucha la cola 'user_queue'"""
    credentials = pika.PlainCredentials('monitoring_user', 'isis2503')
    connection = pika.BlockingConnection(pika.ConnectionParameters('10.128.0.4', 5672, '/', credentials))
    channel = connection.channel()

    # Declarar la cola (por si no ha sido creada) y enlazarla al exchange
    channel.queue_declare(queue='user_queue', arguments={'x-max-priority': 10})
    
    # Enlazar la cola al exchange 'bus_mensajeria'
    channel.queue_bind(exchange='bus_mensajeria', queue='user_queue', routing_key='user.#')

    # Consumir mensajes desde la cola user_queue
    channel.basic_consume(queue='user_queue', on_message_callback=callback_user, auto_ack=True)

    print("UserHandler escuchando en 'user_queue'...")
    channel.start_consuming()

if __name__ == "__main__":
    start_user_handler()
