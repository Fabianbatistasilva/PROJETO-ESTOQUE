from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models import Categoria, Historico, Medidas, Movimento, Produto
from django.utils import timezone
from datetime import datetime
from django.core.paginator import Paginator
# Create your views here.

def login(request):
    if request.method != 'POST':
        return render(request, 'paginas/login.html')
    else:
        usuario = request.POST.get('usuario')
        senha = request.POST.get('senha')
        user = auth.authenticate(request, username=usuario, password=senha)

    if not user:
        messages.add_message(request, messages.ERROR, f'ERRO! Usuário ou senha inválidos')
        return render(request, 'paginas/login.html')
    else:
        auth.login(request, user)
        messages.add_message(request, messages.SUCCESS, f'Login feito com sucesso!')
        return redirect('home')

def logout(request):
    auth.logout(request)
    messages.add_message(request, messages.SUCCESS, 'Logout feito com sucesso')
    return redirect('login')

def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Senha alterada com sucesso, faça o login')
            return redirect('login')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'paginas/alterar_senha.html', {'form_senha': form_senha})



def index(request):
    produtos = Produto.objects.all().filter(
        ativo=True
    )
    paginator = Paginator(produtos, 5)
    page = request.GET.get('p')
    produtos = paginator.get_page(page)
    return render(request, 'paginas/index.html', {'produtos':produtos})

def adicionar_produto(request):
    categorias = Categoria.objects.all()
    medidas = Medidas.objects.all()
    if request.method != 'POST':
        return render(request, 'paginas/adicionar_produto.html', {'categorias':categorias, 'medidas':medidas})
    else:
        produto = request.POST.get('produto').strip().title()
        preco = request.POST.get('preco')
        info = request.POST.get('informacoes')
        categ = Categoria.objects.get(id=request.POST.get('categorias'))
        medida = Medidas.objects.get(id=request.POST.get('medidas'))
        foto = request.FILES.get('foto')
        print(foto)
        usuario = request.user
        if len(produto) < 5:
            messages.add_message(request, messages.ERROR, 'Descrição do produto muito curta, mínimo 5 digitos')
            return render(request, 'paginas/adicionar_produto.html', {'categorias':categorias, 'medidas':medidas})
        else:
            item = Produto.objects.create(produto=produto, categoria=categ, medida=medida, informacoes=info, foto=foto, usuario=usuario, preco_venda=preco)
            item.save()
            messages.add_message(request, messages.SUCCESS, 'Produto cadastrado com sucesso.')
            return redirect('home')


def detalhes(request, id):
    produto = Produto.objects.get(id=id)
    return render(request, 'paginas/detalhes.html', {'produto':produto})

def entradas(request, id):
    t_entrada = Movimento.objects.all().filter(
        entrada=True
    )
    produto = Produto.objects.get(id=id)
    hoje = datetime.today()
    hoje = datetime.strftime(hoje, '%Y-%m-%d')
    dt_atual = datetime.today()
    if produto.data_ultima_compra:
        ultima_compra = datetime.strftime(produto.data_ultima_compra, '%Y-%m-%d')
        sem_compra = False
    else:
        sem_compra = True
    if request.method != 'POST':
        return render(request, 'paginas/entradas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje})
    else:
        tipo = Movimento.objects.get(id=request.POST.get('mov'))
        preco = float(request.POST.get('preco'))
        quant = int(request.POST.get('quantidade'))
        data = request.POST.get('data')
        if preco <= 0 and not tipo.somente_contabil:
            messages.add_message(request, messages.ERROR, 'Preço inválido, precisa ser positivo (diferente de zero)')
            return render(request, 'paginas/entradas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje})
        if preco < 0:
            messages.add_message(request, messages.ERROR, 'Preço inválido, precisa ser positivo (diferente de zero)')
            return render(request, 'paginas/entradas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje})
        if quant <= 0:
            messages.add_message(request, messages.ERROR, 'Quantidade inválida, precisa ser positivo (diferente de zero)')
            return render(request, 'paginas/entradas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje})
        if data > hoje:
            messages.add_message(request, messages.ERROR, 'Data inválida, precisa ser anterior a data atual')
            return render(request, 'paginas/entradas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje})
        else:
            historico = Historico.objects.create(data=data, movimentacao=tipo, produto=produto, quantidade=quant, preco=preco)
            historico.save()
            if not tipo.somente_contabil:
                if sem_compra:
                    produto.data_ultima_compra = data
                    produto.preco_ultima_compra = preco
                elif ultima_compra:
                    if ultima_compra < data:
                        produto.data_ultima_compra = data
                        produto.preco_ultima_compra = preco
            produto.estoque = produto.estoque + quant
            produto.save()
            return redirect('home')

def saidas(request, id):
    t_entrada = Movimento.objects.all().filter(
        entrada=False
    )
    produto = Produto.objects.get(id=id)
    preco_venda = str(produto.preco_venda)
    hoje = datetime.today()
    hoje = datetime.strftime(hoje, '%Y-%m-%d')
    dt_atual = datetime.today()
    if produto.data_ultima_venda:
        ultima_venda = datetime.strftime(produto.data_ultima_venda, '%Y-%m-%d')
        sem_venda = False
    else:
        sem_venda = True
    if request.method != 'POST':
        return render(request, 'paginas/saidas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje, 'preco_venda':preco_venda})
    else:
        tipo = Movimento.objects.get(id=request.POST.get('mov'))
        preco = float(request.POST.get('preco'))
        quant = int(request.POST.get('quantidade'))
        data = request.POST.get('data')
        if preco <= 0 and not tipo.somente_contabil:
            messages.add_message(request, messages.ERROR, 'Preço inválido, precisa ser positivo (diferente de zero)')
            return render(request, 'paginas/saidas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje, 'preco_venda':preco_venda})
        if preco < 0:
            messages.add_message(request, messages.ERROR, 'Preço inválido, precisa ser positivo (diferente de zero)')
            return render(request, 'paginas/saidas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje, 'preco_venda':preco_venda})
        if quant <= 0:
            messages.add_message(request, messages.ERROR, 'Quantidade inválida, precisa ser positivo (diferente de zero)')
            return render(request, 'paginas/saidas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje, 'preco_venda':preco_venda})
        if quant > produto.estoque:
            messages.add_message(request, messages.ERROR, f'Não existe quantidade suficiente, só existem no estoque {produto.estoque} unidades')
            return render(request, 'paginas/saidas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje, 'preco_venda':preco_venda})
        if data > hoje:
            messages.add_message(request, messages.ERROR, 'Data inválida, precisa ser anterior a data atual')
            return render(request, 'paginas/saidas.html', {'t_entrada':t_entrada, 'produto':produto, 'hoje':hoje, 'preco_venda':preco_venda})
        else:
            historico = Historico.objects.create(data=data, movimentacao=tipo, produto=produto, quantidade=quant, preco=preco)
            historico.save()
            if not tipo.somente_contabil:
                if sem_venda:
                    produto.data_ultima_venda = data
                elif ultima_venda:
                    if ultima_venda < data:
                        produto.data_ultima_venda = data
            produto.estoque = produto.estoque - quant
            produto.save()
            return redirect('home')

def relatorio(request, id):
    produto = Produto.objects.get(id=id)
    historico = Historico.objects.all().filter(
        produto=produto
    ).order_by('-data')
    paginator = Paginator(historico, 5)
    page = request.GET.get('p')
    historico = paginator.get_page(page)
    total = []
    for c in historico:
        total.append(c.preco*c.quantidade)
    print(total)
    teste = zip(historico, total)
    print(teste)
    return render(request, 'paginas/relatorios.html', {'produto':produto, 'historico':historico, 'total':total, 'teste':teste})

def alterar(request, id):
    produto = Produto.objects.get(id=id)
    produto.preco_venda = str(produto.preco_venda)
    categorias = Categoria.objects.all()
    medidas = Medidas.objects.all()
    if request.method != 'POST':
        return render(request, 'paginas/alterar.html', {'produto':produto, 'categorias':categorias, 'medidas':medidas})
    else:
        produto.produto = request.POST.get('produto').strip().title()
        produto.preco_venda = request.POST.get('preco')
        produto.informacoes = request.POST.get('informacoes')
        produto.categoria = Categoria.objects.get(id=request.POST.get('categorias'))
        produto.medida = Medidas.objects.get(id=request.POST.get('medidas'))
        foto = request.FILES.get('foto')
        print(foto)
        if foto:
            produto.foto = foto
        if len(produto.produto) < 5:
            messages.add_message(request, messages.ERROR, 'Descrição do produto muito curta, mínimo 5 digitos')
            return render(request, 'paginas/alterar.html', {'produto':produto, 'categorias':categorias, 'medidas':medidas})
        else:
            produto.save()
            messages.add_message(request, messages.SUCCESS, 'Produto alterado com sucesso.')
            return redirect('home')

def desligar_produto(request, id):
    produto = Produto.objects.get(id=id)
    produto.ativo = False
    produto.save()
    messages.add_message(request, messages.SUCCESS, 'Produto desligado com sucesso.')
    return redirect('home')
