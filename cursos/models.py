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
    ordem = models.PositiveIntegerField(default=1)

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
    ordem = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['ordem']
        verbose_name = "Aula"
        verbose_name_plural = "Aulas"

    def __str__(self):
        return self.titulo


class Material(models.Model):

    TIPO_CHOICES = [
        ('pdf',    'PDF / Partitura'),
        ('video',  'Vídeo (MP4)'),
        ('imagem', 'Imagem'),
        ('link',   'Link externo (YouTube / Drive)'),
        ('outro',  'Outro arquivo'),
    ]

    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='materiais')
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(
        max_length=10,
        choices=TIPO_CHOICES,
        default='outro',
        help_text="Escolha o tipo do material para exibição correta na plataforma."
    )
    arquivo = models.FileField(
        upload_to='materiais/',
        null=True,
        blank=True
    )
    link_externo = models.URLField(max_length=500, null=True, blank=True,
                                   help_text="Link do YouTube ou Google Drive (compartilhado)")
    data_upload = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.arquivo and not self.link_externo:
            raise ValidationError("O material precisa ter um arquivo ou um link externo.")
        if self.tipo == 'link' and not self.link_externo:
            raise ValidationError("Para o tipo 'Link externo', preencha o campo Link externo.")

    @property
    def tipo_arquivo(self):
        return self.tipo

    @property
    def url_corrigida(self):
        """
        Retorna a URL do arquivo.
        Com AWS_QUERYSTRING_AUTH=True no settings, o django-storages
        gera automaticamente URLs assinadas com validade de 1 hora.
        """
        if not self.arquivo:
            return None
        return self.arquivo.url

    @property
    def embed_url(self):
        """Converte links do YouTube e Google Drive para formato embed."""
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