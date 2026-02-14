from django.contrib import admin
from .models import Curso,Aula,Material,Aluno

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    #Isso faz o slug ser preenchido automaticamente enquanto escreve o nome
    prepopulated_fields={'slug':('nome',)}
    list_display=('nome','cor_neon','data_criacao')
@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display=('user','get_cursos')
    search_fields=('user__username','user_first_name')
    filter_horizontal=('cursos_matriculados',)
    
    def get_cursos(self,obj):
        return",".join([c.nome for c in obj.cursos_matriculados.all()])
    get_cursos.short_description= 'Cursos Matriculados'
admin.site.register(Aula)
admin.site.register(Material)
from .models import Galeria # Ou o nome que você deu ao modelo da vitrine

@admin.register(Galeria)
class GaleriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_postagem')