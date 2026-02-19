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
    arquivo = models.FileField(upload_to='materiais/') # Removi o 'pdf' do caminho para não confundir
    data_upload = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.modulo.titulo}"

    @property
    def tipo_arquivo(self):
        try:
            # Pega a URL completa que o Cloudinary gera
            url = self.arquivo.url.lower()
            nome_no_banco = str(self.arquivo.name).lower()
            
            # 1. PRIORIDADE MÁXIMA: Se tiver "pdf" em qualquer lugar, É PDF.
            if 'pdf' in url or 'pdf' in nome_no_banco:
                return 'pdf'
                
            # 2. VÍDEOS:
            if any(ext in url for ext in ['.mp4', '.mov', '.webm']) or '/video/' in url:
                return 'video'
                
            # 3. IMAGENS: Só vai chegar aqui se não for PDF nem Vídeo
            if any(ext in url for ext in ['.jpg', '.jpeg', '.png', '.webp']) or '/image/' in url:
                return 'imagem'
                
        except Exception as e:
            print(f"Erro ao identificar arquivo: {e}")
            
        return 'pdf' # Se tudo falhar, assume PDF (que é o mais comum para materiais)

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

