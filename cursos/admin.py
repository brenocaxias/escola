from django.contrib import admin
from .models import Curso, Modulo, Aula, Material, Aluno, Galeria

# --- INLINES (Para editar tudo em uma tela só) ---

class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1
    show_change_link = True

class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1

class MaterialInline(admin.TabularInline):
    model = Material
    fields = ('titulo', 'arquivo', 'link_externo') # Adicionado campo de link aqui
    extra = 1

# --- CONFIGURAÇÕES DO ADMIN ---

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cor_neon', 'data_criacao')
    prepopulated_fields = {'slug': ('nome',)}
    inlines = [ModuloInline]

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'curso', 'ordem')
    list_filter = ('curso',)
    inlines = [AulaInline, MaterialInline]

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'modulo', 'tipo_arquivo', 'data_upload')
    list_filter = ('modulo__curso', 'modulo')
    search_fields = ('titulo',)
    # Organiza os campos no formulário de edição individual
    fields = ('modulo', 'titulo', 'arquivo', 'link_externo')

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_cursos')
    search_fields = ('user__username', 'user__first_name', 'user__email')
    filter_horizontal = ('cursos_matriculados',)
    
    def get_cursos(self, obj):
        return ", ".join([c.nome for c in obj.cursos_matriculados.all()])
    get_cursos.short_description = 'Cursos Matriculados'

@admin.register(Galeria)
class GaleriaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data_postagem')

# Registros individuais (opcionais, mas úteis)
admin.site.register(Aula)