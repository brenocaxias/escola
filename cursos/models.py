from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.text import slugify


class Curso(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    descricao = models.TextField()
    imagem_fundo = models.ImageField(upload_to='cursos/capas/', null=True, blank=True)
    cor_neon = models.CharField(max_length=7, default="#8A2BE2")
    data_criacao = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.nome)
            slug = base_slug
            counter = 1
            while Curso.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

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
    ordem = models.PositiveIntegerField(default=1, help_text="Ordem de exibição dentro do módulo")

    class Meta:
        ordering = ['ordem']
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"

    def __str__(self):
        return self.titulo


class Material(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='materiais')
    titulo = models.CharField(max_length=200)
    arquivo = models.FileField(upload_to='materiais/', null=True, blank=True)
    link_externo = models.URLField(max_length=500, null=True, blank=True,
                                   help_text="Link do YouTube ou Google Drive (compartilhado)")
    data_upload = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.arquivo and not self.link_externo:
            raise ValidationError("O material precisa ter um arquivo ou um link externo.")

    @property
    def tipo_arquivo(self):
        if self.link_externo:
            return 'link'
        if not self.arquivo:
            return 'outro'

        nome = str(self.arquivo.name).lower()
        url = str(self.arquivo.url).lower()

        # PDF
        if nome.endswith('.pdf'):
            return 'pdf'

        # Vídeo — extensão ou caminho Cloudinary
        if any(nome.endswith(ext) for ext in ['.mp4', '.mov', '.webm']):
            return 'video'
        if '/video/' in url:
            return 'video'

        # Imagem — extensão ou caminho Cloudinary
        # Cloudinary não preserva extensão na URL pública,
        # então /image/upload/ é o sinal mais confiável
        if any(nome.endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.webp', '.gif']):
            return 'imagem'
        if '/image/upload/' in url:
            return 'imagem'

        return 'outro'

    @property
    def url_corrigida(self):
        """Garante que PDFs do Cloudinary sejam servidos como raw, não como imagem."""
        if not self.arquivo:
            return None
        url = self.arquivo.url
        if self.tipo_arquivo == 'pdf' and '/image/upload/' in url:
            return url.replace('/image/upload/', '/raw/upload/')
        return url

    @property
    def embed_url(self):
        """
        Converte URLs do YouTube e Google Drive para formato embed.
        YouTube: https://www.youtube.com/watch?v=ID  ->  https://www.youtube.com/embed/ID
        Drive:   https://drive.google.com/file/d/ID/view  ->  .../preview
        """
        if not self.link_externo:
            return ''
        url = self.link_externo

        if 'youtube.com/watch' in url:
            video_id = url.split('v=')[-1].split('&')[0]
            return f'https://www.youtube.com/embed/{video_id}'

        if 'youtu.be/' in url:
            video_id = url.split('youtu.be/')[-1].split('?')[0]
            return f'https://www.youtube.com/embed/{video_id}'

        if 'drive.google.com' in url:
            return url.replace('/view', '/preview').replace('/edit', '/preview')

        return url

    def __str__(self):
        return self.titulo


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
        return self.titulo if self.titulo else f"Foto {self.id}"