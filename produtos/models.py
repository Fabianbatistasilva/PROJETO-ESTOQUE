from django.db import models
from django.contrib.auth.models import User
from django import forms
# Create your models here.

class Categoria(models.Model):
    categoria = models.CharField(max_length=100)
    def __str__(self):
        return self.categoria

class Movimento(models.Model):
    tipo_movimento = models.CharField(max_length=50)
    entrada = models.BooleanField()
    somente_contabil = models.BooleanField(default=False)
    def __str__(self):
        return self.tipo_movimento

class Medidas(models.Model):
    descricao = models.CharField(max_length=50)
    def __str__(self):
        return self.descricao

class Produto(models.Model):
    produto = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    medida = models.ForeignKey(Medidas, on_delete=models.DO_NOTHING, blank=True, null=True)
    data_ultima_compra = models.DateField(blank=True, null=True)
    preco_ultima_compra = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    preco_venda = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    data_ultima_venda = models.DateField(blank=True, null=True)
    estoque = models.IntegerField(default=0)
    informacoes = models.TextField(blank=True, null=True)
    foto = models.ImageField(blank=True, upload_to='fotos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ativo = models.BooleanField(default=True)
    def __str__(self):
        return self.produto

class Historico(models.Model):
    data = models.DateField()
    movimentacao = models.ForeignKey(Movimento, on_delete=models.DO_NOTHING)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
    quantidade = models.IntegerField()
    preco = models.DecimalField(max_digits=7, decimal_places=2)
    excluido = models.BooleanField(default=False)
