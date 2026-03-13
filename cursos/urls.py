from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login-sucesso/', views.login_sucesso, name='login_sucesso'),

    # Painel
    path('painel-gestao/', views.painel_coordenador, name='painel_coordenador'),
    path('painel-gestao/cadastrar-aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('painel-gestao/upload-material/', views.upload_material, name='upload_material'),
    path('painel/curso/cadastrar/', views.cadastrar_curso, name='cadastrar_curso'),
    path('painel/modulo/cadastrar/', views.cadastrar_modulo, name='cadastrar_modulo'),

    # Alunos
    path('painel-gestao/editar-aluno/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    path('painel-gestao/excluir-aluno/<int:aluno_id>/', views.excluir_aluno, name='excluir_aluno'),

    # Materiais
    path('painel-gestao/editar-material/<int:material_id>/', views.editar_material, name='editar_material'),
    path('painel-gestao/excluir-material/<int:material_id>/', views.excluir_material, name='excluir_material'),

    # Galeria
    path('gestao/galeria/', views.gerenciar_galeria, name='gerenciar_galeria'),
    path('gestao/galeria/excluir/<int:foto_id>/', views.excluir_foto, name='excluir_foto'),

    # BUG CORRIGIDO: rota com <str:slug> deve ficar SEMPRE por último
    # para não capturar URLs como "excluir-material", "editar-aluno" etc.
    path('<str:instrumento_slug>/', views.detalhe_curso, name='detalhe_curso'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)