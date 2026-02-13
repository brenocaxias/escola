from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static
urlpatterns = [
    # Isso aceita /cursos/violao, /cursos/piano, /cursos/bateria...
    
    path('login-sucesso/', views.login_sucesso,name='login_sucesso'),
    path('painel-gestao', views.painel_coordenador,name='painel_coordenador'),
    path('', views.index, name='index'),
    path('painel-gestao/cadastrar-aluno/', views.cadastrar_aluno, name='cadastrar_aluno'),
    path('painel-gestao/upload-material/', views.upload_material, name='upload_material'),
    path('<str:instrumento_slug>/', views.detalhe_curso, name='detalhe_curso'),
    path('excluir-material/<int:material_id>/', views.excluir_material, name='excluir_material'),
    path('editar-aluno/<int:aluno_id>/', views.editar_aluno, name='editar_aluno'),
    path('excluir-aluno/<int:aluno_id>/', views.excluir_aluno, name='excluir_aluno'),
    path('editar-material/<int:material_id>/', views.editar_material, name='editar_material'),
    path('gestao/galeria/', views.gerenciar_galeria, name='gerenciar_galeria'),
    path('gestao/galeria/excluir/<int:foto_id>/', views.excluir_foto, name='excluir_foto'),
]
# ESSA LINHA É O SEGREDO:
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)