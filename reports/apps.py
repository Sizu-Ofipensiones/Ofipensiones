import threading
from django.apps import AppConfig
from .report_handler import start_report_handler, generate_reports


class ReportsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reports'
    def ready(self):
        # Generar los reportes
        generate_reports()

        # Iniciar el manejador de reportes en un hilo separado
        thread = threading.Thread(target=start_report_handler)
        thread.daemon = True
        thread.start()




