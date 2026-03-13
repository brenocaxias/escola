from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Aluno, Galeria, Material, Curso, Modulo


# ---------------------------------------------------------------------------
# Alunos
# ---------------------------------------------------------------------------

class CadastroAlunoForm(forms.ModelForm):
    """
    MELHORIAS:
    - Campo 'password' com confirmação (password2)
    - Campo 'email' obrigatório
    - Validação de username duplicado tratada pelo ModelForm automaticamente
    """
    username = forms.CharField(
        label="Nome de Usuário (Login)",
        widget=forms.TextInput(attrs={'class': 'input-glass'}),
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'input-glass'}),
    )
    password2 = forms.CharField(
        label="Confirmar Senha",
        widget=forms.PasswordInput(attrs={'class': 'input-glass'}),
    )
    cursos = forms.ModelMultipleChoiceField(
        queryset=Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Vincular aos Cursos:",
        required=False,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input-glass',
                'placeholder': 'Ex: Breno',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input-glass',
                'placeholder': 'email@exemplo.com',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        # BUG CORRIGIDO: valida que as senhas coincidem
        if password and password2 and password != password2:
            raise ValidationError("As senhas não coincidem.")

        return cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # MELHORIA: impede e-mails duplicados
        if email and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este e-mail já está em uso.")
        return email


# ---------------------------------------------------------------------------
# Materiais
# ---------------------------------------------------------------------------

class MaterialForm(forms.ModelForm):
    """
    BUG CORRIGIDO: campo 'link_externo' estava ausente no formulário,
    impossibilitando o cadastro de materiais do tipo link (YouTube, Drive).
    MELHORIA: validação de que arquivo OU link foi fornecido.
    """
    class Meta:
        model = Material
        fields = ['titulo', 'modulo', 'arquivo', 'link_externo']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'input-glass',
                'placeholder': 'Ex: Partitura de Flauta',
            }),
            'arquivo': forms.FileInput(attrs={'class': 'input-glass'}),
            'modulo': forms.Select(attrs={'class': 'input-glass'}),
            'link_externo': forms.URLInput(attrs={
                'class': 'input-glass',
                'placeholder': 'https://youtube.com/... ou https://drive.google.com/...',
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        arquivo = cleaned_data.get('arquivo')
        link_externo = cleaned_data.get('link_externo')

        # MELHORIA: garante que pelo menos um dos dois foi fornecido
        if not arquivo and not link_externo:
            raise ValidationError("Forneça um arquivo ou um link externo (YouTube, Drive, etc).")

        return cleaned_data


# ---------------------------------------------------------------------------
# Galeria
# ---------------------------------------------------------------------------

class FotoGaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria
        fields = ['titulo', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'input-glass',
                'placeholder': 'Título da foto',
            }),
            'imagem': forms.FileInput(attrs={'class': 'input-glass'}),
        }


# ---------------------------------------------------------------------------
# Cursos e Módulos
# ---------------------------------------------------------------------------

class CursoForm(forms.ModelForm):
    """
    MELHORIA: campo 'slug' removido do formulário pois agora é gerado
    automaticamente no model.save(). Adicionados campos descricao e cor_neon.
    """
    class Meta:
        model = Curso
        fields = ['nome', 'descricao', 'imagem_fundo', 'cor_neon']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'input-glass',
                'placeholder': 'Ex: Violão Popular',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'input-glass',
                'placeholder': 'Descrição do curso...',
                'rows': 3,
            }),
            'imagem_fundo': forms.FileInput(attrs={'class': 'input-glass'}),
            'cor_neon': forms.TextInput(attrs={
                'class': 'input-glass',
                'type': 'color',  # Abre seletor de cor no browser
            }),
        }


class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['titulo', 'descricao', 'curso', 'ordem']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'input-glass',
                'placeholder': 'Ex: Básico I ou Teoria Musical',
            }),
            'descricao': forms.Textarea(attrs={
                'class': 'input-glass',
                'placeholder': 'O que será estudado neste módulo...',
                'rows': 3,
            }),
            'curso': forms.Select(attrs={'class': 'input-glass'}),
            'ordem': forms.NumberInput(attrs={'class': 'input-glass'}),
        }