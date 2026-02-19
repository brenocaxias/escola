from django.db import models
from django.contrib.auth.models import User
import os

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descricao = models.TextField()
    imagem_fundo = models.ImageField(upload_to='cursos/capas/', null=True, blank=True) # ADICIONAR ESTA LINHA
    cor_neon = models.CharField(max_length=7, default="#8A2BE2")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

# --- NOVA CLASSE MÓDULO ---
class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True) # ADICIONAR ESTA LINHA
    ordem = models.PositiveIntegerField(default=1, help_text="Ordem de exibição (1, 2, 3...)")

    class Meta:
        ordering = ['ordem'] # Isso faz os módulos aparecerem na sequência certa
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"

    def __str__(self):
        return f"{self.curso.nome} - {self.titulo}"

class Aula(models.Model):
    # Mudamos de Curso para Modulo
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='aulas')
    titulo = models.CharField(max_length=200)
    conteudo_texto = models.TextField()
    video_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.titulo

class Material(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='materiais')
    titulo = models.CharField(max_length=200)
    # Arquivo opcional para quando for link
    arquivo = models.FileField(upload_to='materiais/', null=True, blank=True)
    # Campo para links do YouTube, Drive, etc.
    link_externo = models.URLField(max_length=500, null=True, blank=True, help_text="Link do YouTube ou Google Drive (compartilhado)")
    data_upload = models.DateTimeField(auto_now_add=True)

    @property
    def tipo_arquivo(self):
        if self.link_externo:
            return 'link'
        
        nome_banco = str(self.arquivo.name).lower() if self.arquivo else ""
        url_completa = str(self.arquivo.url).lower() if self.arquivo else ""
        
        if 'pdf' in nome_banco or 'pdf' in url_completa:
            return 'pdf'
        if any(ext in nome_banco for ext in ['.mp4', '.mov', '.webm']) or '/video/' in url_completa:
            return 'video'
        if any(ext in nome_banco for ext in ['.jpg', '.jpeg', '.png', '.webp']) or '/image/' in url_completa:
            return 'imagem'
        return 'outro'

    @property
    def embed_url(self):
        """Converte links normais em links de embed"""
        if not self.link_externo:
            return None
        
        url = self.link_externo
        # YouTube
        if 'youtube.com/watch?v=' in url:
            return url.replace('watch?v=', 'embed/')
        if 'youtu.be/' in url:
            video_id = url.split('/')[-1]
            return f"https://www.youtube.com/embed/{video_id}"
        # Google Drive
        if 'drive.google.com' in url:
            return url.replace('/view', '/preview')
        
        return url

class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cursos_matriculados = models.ManyToManyField(Curso, blank=True)
    
    def __str__(self):
        return self.user.username

class Galeria(models.Model):
    titulo = models.CharField(max_length=100, blank=True)
    imagem = models.ImageField(upload_to='galeria/')
    data_postagem = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Fotos da Galeria'
        
    def __str__(self):
        return self.titulo if self.titulo else f"foto {self.id}"

