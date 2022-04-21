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
]