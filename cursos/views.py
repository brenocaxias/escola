from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404

import requests as http_requests

from cursos.models import Aluno, Curso, Galeria, Material
from .forms import CadastroAlunoForm, FotoGaleriaForm, MaterialForm, CursoForm, ModuloForm
from .models import Galeria
from django.contrib.auth.models import User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _is_staff(u):
    return u.is_staff


def _is_superuser(u):
    return u.is_superuser


# ---------------------------------------------------------------------------
# Views públicas / pós-login
# ---------------------------------------------------------------------------

def index(request):
    if not request.user.is_authenticated:
        cursos = Curso.objects.all()
        return render(request, 'cursos/index.html', {'cursos': cursos})

    if request.user.is_superuser:
        cursos = Curso.objects.all()
    else:
        if hasattr(request.user, 'aluno'):
            cursos = request.user.aluno.cursos_matriculados.all()
        else:
            cursos = Curso.objects.none()

    return render(request, 'cursos/index.html', {'cursos': cursos})


@login_required
def detalhe_curso(request, instrumento_slug):
    curso = get_object_or_404(Curso, slug=instrumento_slug)

    if not request.user.is_superuser:
        if not hasattr(request.user, 'aluno') or curso not in request.user.aluno.cursos_matriculados.all():
            return render(request, 'cursos/acesso_negado.html', {
                'mensagem': 'Você não tem permissão para acessar este curso ou não está matriculado.'
            })

    return render(request, 'cursos/detalhe_curso.html', {'curso': curso})


@login_required
def login_sucesso(request):
    if request.user.is_superuser:
        return redirect('painel_coordenador')
    return redirect('index')


def home(request):
    fotos_galeria = Galeria.objects.all().order_by('-data_postagem')
    return render(request, 'cursos/home.html', {'fotos': fotos_galeria})


# ---------------------------------------------------------------------------
# Proxy para servir materiais (resolve bloqueio CORS/auth do Cloudinary)
# ---------------------------------------------------------------------------

@login_required
def servir_material(request, material_id):
    """
    Busca o arquivo no Cloudinary autenticado pelo servidor
    e entrega ao aluno — resolve o bloqueio 401 no iframe.
    Só permite acesso se o aluno estiver matriculado no curso.
    """
    material = get_object_or_404(Material, id=material_id)

    # Verifica permissão de acesso ao curso
    if not request.user.is_superuser:
        curso = material.modulo.curso
        if not hasattr(request.user, 'aluno') or curso not in request.user.aluno.cursos_matriculados.all():
            raise Http404

    url = material.url_corrigida
    if not url:
        raise Http404

    try:
        resp = http_requests.get(url, timeout=15)
        resp.raise_for_status()
    except Exception:
        raise Http404

    # Define o content-type correto por tipo de material
    tipos_content = {
        'pdf':    'application/pdf',
        'video':  'video/mp4',
        'imagem': 'image/jpeg',
    }
    content_type = tipos_content.get(material.tipo, 'application/octet-stream')

    return HttpResponse(resp.content, content_type=content_type)


# ---------------------------------------------------------------------------
# Painel do Coordenador
# ---------------------------------------------------------------------------

@login_required
@user_passes_test(_is_staff)
def painel_coordenador(request):
    busca = request.GET.get('search', '').strip()

    alunos_qs = User.objects.filter(aluno__isnull=False)
    if busca:
        alunos_qs = alunos_qs.filter(
            Q(username__icontains=busca) | Q(first_name__icontains=busca)
        )

    materiais = Material.objects.all().order_by('-data_upload')
    cursos = Curso.objects.all()

    return render(request, 'cursos/painel_coordenador.html', {
        'alunos': alunos_qs,
        'materiais': materiais,
        'cursos': cursos,
        'busca': busca,
    })


# ---------------------------------------------------------------------------
# Gestão de Alunos
# ---------------------------------------------------------------------------

@login_required
@user_passes_test(_is_staff)
def cadastrar_aluno(request):
    if request.method == 'POST':
        form = CadastroAlunoForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
            )
            aluno = Aluno.objects.create(user=user)
            aluno.cursos_matriculados.set(form.cleaned_data['cursos'])
            messages.success(request, f'Aluno "{user.username}" cadastrado com sucesso.')
            return redirect('painel_coordenador')
    else:
        form = CadastroAlunoForm()
    return render(request, 'cursos/cadastrar_aluno.html', {'form': form})


@login_required
@user_passes_test(_is_staff)
def editar_aluno(request, aluno_id):
    aluno = get_object_or_404(User, id=aluno_id)

    if request.method == 'POST':
        form = CadastroAlunoForm(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado com sucesso.')
            return redirect('painel_coordenador')
    else:
        form = CadastroAlunoForm(instance=aluno)

    return render(request, 'cursos/editar_aluno.html', {'form': form, 'aluno': aluno})


@login_required
@user_passes_test(_is_staff)
@require_POST
def excluir_aluno(request, aluno_id):
    aluno = get_object_or_404(User, id=aluno_id)
    if not aluno.is_staff:
        nome = aluno.username
        aluno.delete()
        messages.success(request, f'Aluno "{nome}" excluído.')
    else:
        messages.error(request, 'Não é possível excluir um administrador por aqui.')
    return redirect('painel_coordenador')


# ---------------------------------------------------------------------------
# Gestão de Materiais
# ---------------------------------------------------------------------------

@login_required
@user_passes_test(_is_superuser)
def upload_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material enviado com sucesso.')
            return redirect('painel_coordenador')
    else:
        form = MaterialForm()
    return render(request, 'cursos/upload_material.html', {'form': form})


@login_required
@user_passes_test(_is_staff)
def editar_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)

    if request.method == 'POST':
        form = MaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material atualizado.')
            return redirect('painel_coordenador')
    else:
        form = MaterialForm(instance=material)

    return render(request, 'cursos/editar_material.html', {'form': form, 'material': material})


@login_required
@user_passes_test(_is_staff)
@require_POST
def excluir_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if material.arquivo:
        material.arquivo.delete(save=False)
    material.delete()
    messages.success(request, 'Material excluído.')
    return redirect('painel_coordenador')


# ---------------------------------------------------------------------------
# Gestão de Cursos e Módulos
# ---------------------------------------------------------------------------

@login_required
@user_passes_test(_is_staff)
def cadastrar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Curso criado com sucesso.')
            return redirect('painel_coordenador')
    else:
        form = CursoForm()
    return render(request, 'cursos/cadastrar_curso.html', {'form': form})


@login_required
@user_passes_test(_is_staff)
def cadastrar_modulo(request):
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Módulo criado com sucesso.')
            return redirect('painel_coordenador')
    else:
        form = ModuloForm()
    return render(request, 'cursos/cadastrar_modulo.html', {'form': form})


# ---------------------------------------------------------------------------
# Galeria
# ---------------------------------------------------------------------------

@login_required
@user_passes_test(_is_staff)
def gerenciar_galeria(request):
    fotos = Galeria.objects.all().order_by('-data_postagem')

    if request.method == 'POST':
        form = FotoGaleriaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Foto adicionada à galeria.')
            return redirect('gerenciar_galeria')
    else:
        form = FotoGaleriaForm()

    return render(request, 'cursos/gerenciar_galeria.html', {'fotos': fotos, 'form': form})


@login_required
@user_passes_test(_is_staff)
@require_POST
def excluir_foto(request, foto_id):
    foto = get_object_or_404(Galeria, id=foto_id)
    if foto.imagem:
        foto.imagem.delete(save=False)
    foto.delete()
    messages.success(request, 'Foto excluída.')
    return redirect('gerenciar_galeria')