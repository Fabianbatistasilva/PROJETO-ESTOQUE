from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.index, name='home'),
    path('logout/', views.logout, name='logout'),
    path('alterar_senha/', views.alterar_senha, name='alterar_senha'),
    path('adicionar_produto/', views.adicionar_produto, name='adicionar_produto'),
    path('detalhes/<int:id>', views.detalhes, name='detalhes'),
    path('entradas/<int:id>', views.entradas, name='entradas'),
    path('saidas/<int:id>', views.saidas, name='saidas'),
    path('relatorio/<int:id>', views.relatorio, name='relatorio'),
    path('alterar/<int:id>', views.alterar, name='alterar'),
    path('desligar/<int:id>', views.desligar_produto, name='desligar'),
    path('cadastros/', views.cadastros, name='cadastros'),
    path('adicionar_categoria/', views.adicionar_categoria, name='adicionar_categoria'),
    path('alterar_categoria/<int:id>', views.alterar_categoria, name='alterar_categoria'),
    path('adicionar_medida/', views.adicionar_medida, name='adicionar_medida'),
    path('alterar_medida/<int:id>', views.alterar_medida, name='alterar_medida'),
    path('adicionar_movimento/', views.adicionar_movimento, name='adicionar_movimento'),
    path('eliminar_historico/<int:id>', views.eliminar_historico, name='eliminar_historico'),
    path('pouco_estoque/<int:quant>', views.pouco_estoque, name='pouco_estoque'),
    path('por_categoria/', views.por_categoria, name='por_categoria'),
    path('produto_por_categoria/<int:id>', views.produto_por_categoria, name='produto_por_categoria'),
]