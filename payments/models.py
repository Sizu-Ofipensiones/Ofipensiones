from django.db import models

class Payment(models.Model):

    class MetodoPago(models.TextChoices):
        CORRESPONSAL_BANCARIO = 'corresponsal_Bancario', 'Corresponsal Bancario'
        APP = 'app', 'App'

    id = models.BigAutoField(primary_key=True) 
    usuario = models.CharField(max_length=255)  
    codigoUsuario = models.BigIntegerField()  
    metodoPago = models.CharField(max_length=21, choices=MetodoPago.choices)
    concepto = models.CharField(max_length=255)
    valor = models.IntegerField()  
    estado = models.CharField(max_length=50)  
    
    def __str__(self):
        return f"Pago: {self.id} - {self.usuario} ({self.get_metodoPago_display()})"
