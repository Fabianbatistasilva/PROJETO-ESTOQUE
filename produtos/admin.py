from django.contrib import admin
from .models import Categoria, Medidas, Movimento, Produto, Historico
# Register your models here.


class AdmProduto(admin.ModelAdmin):
    list_display = ('id', 'produto', 'categoria', 'data_ultima_compra', 'preco_ultima_compra', 'preco_venda', 'estoque')
    list_display_links = ('id', 'produto',)
    list_per_page = 10
    search_field = ['produto',]
    list_filter = ['categoria']

class AdmHistorico(admin.ModelAdmin):
    list_display = ('id', 'data', 'movimentacao', 'produto', 'quantidade', 'preco', 'excluido')
    list_display_links = ('id', 'data',)
    list_per_page = 10
    list_filter = ['movimentacao']

admin.site.register(Categoria)
admin.site.register(Movimento)
admin.site.register(Medidas)
admin.site.register(Produto, AdmProduto)
admin.site.register(Historico, AdmHistorico)