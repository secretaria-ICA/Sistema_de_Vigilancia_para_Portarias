from django.db import models
from django.utils import timezone

# Create your models here.
# pessoa_identificada = (models.CharField(max_length=200))

class Analise(models.Model):
    id = models.BigAutoField(primary_key=True)
    rosto_identificado = models.BooleanField(default=False)
    posicao = models.CharField(max_length=200, default="")
    olhos = models.CharField(max_length=200, default="")
    abertura_olho_esquerdo = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    abertura_olho_direito = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    situacao = models.CharField(max_length=50, default="")
    data = models.DateTimeField(default=timezone.now())
    status = models.CharField(max_length=50, default="Normal")
    nomeVigilante = models.CharField(max_length=50,default="Vigilante")

class Alarme(models.Model):
    id = models.BigAutoField(primary_key=True)
    tipo_alarme =  models.CharField(max_length=50, default="")
    situacao = models.CharField(max_length=50, default="")
    mensagem = models.CharField(max_length=200, default="")
    data = models.DateTimeField(default=timezone.now())
