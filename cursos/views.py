from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from cursos.models import Aluno, Curso, Galeria, Material
from .forms import CadastroAlunoForm, FotoGaleriaForm, MaterialForm, CursoForm, ModuloForm
from django.contrib.auth.models import User
def index(request):
    # 1. Se não estiver logado, mostra a vitrine
    if not request.user.is_authenticated:
        cursos = Curso.objects.all()
        return render(request, 'cursos/index.html', {'cursos': cursos})

    # 2. Se for Admin, mostra tudo
    if request.user.is_superuser:
        cursos = Curso.objects.all()
    else:
        # 3. Se for Aluno, tenta buscar o perfil
        # Usamos hasattr para checar se a relação User -> Aluno existe
        if hasattr(request.user, 'aluno'):
            cursos = request.user.aluno.cursos_matriculados.all()
            # DICA: Adicione um print aqui no seu terminal para testar
            # print(f"Cursos do {request.user.username}: {cursos}")
        else:
            cursos = []

    return render(request, 'cursos/index.html', {'cursos': cursos})
def detalhe_curso(request, instrumento_slug):
    # 1. Busca o curso pelo slug
    curso = get_object_or_404(Curso, slug=instrumento_slug)
    
    # 2. Trava de Segurança: Verifica se o usuário tem permissão
    # Se for superuser, ele passa direto.
    if not request.user.is_superuser:
        # Se não for superuser, verificamos se ele é um aluno matriculado
        if not hasattr(request.user, 'aluno') or curso not in request.user.aluno.cursos_matriculados.all():
            return render(request, 'cursos/acesso_negado.html', {
                'mensagem': 'Você não tem permissão para acessar este curso ou não está matriculado.'
            })

    # 3. Preparação para o Template
    # Não filtramos materiais aqui! O template acessará via curso.modulos.all
    context = {
        'curso': curso,
    }
    
    return render(request, 'cursos/detalhe_curso.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def painel_coordenador(request):
    busca = request.GET.get('search', '')
    if busca:
        alunos = User.objects.filter(username__icontains=busca) | User.objects.filter(first_name__icontains=busca)
    else:
        alunos = User.objects.all()

    materiais = Material.objects.all().order_by('-data_upload')
    cursos = Curso.objects.all() # <-- ADICIONADO: Puxa os cursos para a lista

    return render(request, 'cursos/painel_coordenador.html', {
        'alunos': alunos,
        'materiais': materiais,
        'cursos': cursos, # <-- ADICIONADO
        'busca': busca 
    })
def login_sucesso(request):
    if request.user.is_superuser:
        return redirect('painel_coordenador')
    else:
        return redirect('index')
def cadastrar_aluno(request):
    if request.method == 'POST':
        form= CadastroAlunoForm(request.POST)
        if form.is_valid():
            user= User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name']
            )
            aluno=Aluno.objects.create(user=user)
            aluno.cursos_matriculados.set(form.cleaned_data['cursos'])
            aluno.save()
            return redirect('painel_coordenador')
    else:
        form= CadastroAlunoForm()
    return render (request, 'cursos/cadastrar_aluno.html', {'form':form})
# No seu views.py, adicione:

@user_passes_test(lambda u: u.is_superuser)
def upload_material(request):
    if request.method == 'POST':
        # request.FILES é obrigatório para uploads
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('painel_coordenador')
    else:
        form = MaterialForm()
    return render(request, 'cursos/upload_material.html', {'form': form})

def excluir_material(request,material_id):
    material=get_object_or_404(Material, id=material_id)
    if material.arquivo:
        material.arquivo.delete()
    material.delete()
    return redirect ('painel_coordenador')

@login_required
@user_passes_test(lambda u: u.is_staff)
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(User, id=aluno_id)
    if not aluno.is_staff: # Segurança: impede que o admin exclua a si mesmo
        aluno.delete()
    return redirect('painel_coordenador')
@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(User, id=aluno_id)
    
    if request.method == 'POST':
        # Passamos 'instance=aluno' para o Django saber que estamos editando, não criando
        form = CadastroAlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            return redirect('painel_coordenador')
    else:
        form = CadastroAlunoForm(instance=aluno)
    
    return render(request, 'cursos/editar_aluno.html', {'form': form, 'aluno': aluno})
@login_required
@user_passes_test(lambda u: u.is_staff)
def editar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    
    if request.method == 'POST':
        # Passamos instance=material para carregar os dados existentes
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('painel_coordenador')
    else:
        form = MaterialForm(instance=material)
    
    return render(request, 'cursos/editar_material.html', {'form': form, 'material': material})
@login_required
@user_passes_test(lambda u: u.is_staff)
@login_required
@user_passes_test(lambda u: u.is_staff) # Adicionado para proteger a gestão
def gerenciar_galeria(request):
    # Busca todas as fotos para listar na tabela
    fotos = Galeria.objects.all().order_by('-data_postagem')
    
    if request.method == 'POST':
        # Importante: request.FILES é essencial para processar a imagem
        form = FotoGaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gerenciar_galeria')
    else:
        form = FotoGaleriaForm()
    
    return render(request, 'cursos/gerenciar_galeria.html', {'fotos': fotos, 'form': form})

@login_required
@user_passes_test(lambda u: u.is_staff)
def excluir_foto(request, foto_id):
    foto = get_object_or_404(Galeria, id=foto_id)
    # Boa prática: remove o arquivo físico do computador/servidor
    if foto.imagem:
        foto.imagem.delete()
    foto.delete()
    return redirect('gerenciar_galeria')
# C:\Users\breno\aprendendo_django\cursos\views.py
from .models import Galeria # Importante importar o modelo correto

def home(request):
    # 1. Buscamos todas as fotos, da mais recente para a mais antiga
    fotos_galeria = Galeria.objects.all().order_by('-data_postagem')
    
    # 2. Criamos o dicionário de contexto (a 'entrega' para o HTML)
    contexto = {
        'fotos': fotos_galeria, # O nome 'fotos' deve ser igual ao do seu {% for foto in fotos %}
    }
    
    # 3. Renderizamos o template com os dados
    return render(request, 'cursos/home.html', contexto)
# 2. Crie a view de cadastro de curso
@login_required
@user_passes_test(lambda u: u.is_staff)
def cadastrar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('painel_coordenador')
    else:
        form = CursoForm()
    return render(request, 'cursos/cadastrar_curso.html', {'form': form})
@login_required
@user_passes_test(lambda u: u.is_staff)
def cadastrar_modulo(request):
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('painel_coordenador')
    else:
        form = ModuloForm()
    return render(request, 'cursos/cadastrar_modulo.html', {'form': form})