from django.db import models
from django.contrib.auth.models import User
import os

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descricao = models.TextField()
    imagem_fundo = models.ImageField(upload_to='cursos/capas/', null=True, blank=True)
    cor_neon = models.CharField(max_length=7, default="#8A2BE2")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(null=True, blank=True)
    ordem = models.PositiveIntegerField(default=1, help_text="Ordem de exibição (1, 2, 3...)")

    class Meta:
        ordering = ['ordem']
        verbose_name = "Módulo"
        verbose_name_plural = "Módulos"

    def __str__(self):
        return f"{self.curso.nome} - {self.titulo}"

class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='aulas')
    titulo = models.CharField(max_length=200)
    conteudo_texto = models.TextField()
    video_url = models.URLField(blank=True)
    
    def __str__(self):
        return self.titulo

class Material(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='materiais')
    titulo = models.CharField(max_length=200)
    arquivo = models.FileField(upload_to='materiais/', null=True, blank=True)
    link_externo = models.URLField(max_length=500, null=True, blank=True, help_text="Link do YouTube ou Google Drive (compartilhado)")
    data_upload = models.DateTimeField(auto_now_add=True)

    @property
    def tipo_arquivo(self):
        if self.link_externo:
            return 'link'
        if not self.arquivo:
            return 'outro'

        nome_arquivo = str(self.arquivo.name).lower()
        url_completa = str(self.arquivo.url).lower()
        
        # Se for PDF, vamos garantir que a URL não aponte para /image/
        if nome_arquivo.endswith('.pdf') or 'pdf' in url_completa:
            return 'pdf'
        
        if any(nome_arquivo.endswith(ext) for ext in ['.mp4', '.mov', '.webm']) or '/video/' in url_completa:
            return 'video'
            
        if any(nome_arquivo.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp']):
            return 'imagem'
                
        return 'outro'

    @property
    def url_corrigida(self):
        """Garante que PDFs do Cloudinary sejam tratados como ficheiros e não imagens"""
        if not self.arquivo:
            return ""
        url = self.arquivo.url
        if self.tipo_arquivo == 'pdf' and '/image/upload/' in url:
            # Troca 'image' por 'raw' na URL do Cloudinary para PDFs
            return url.replace('/image/upload/', '/raw/upload/')
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