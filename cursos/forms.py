from django import forms 
from django.contrib.auth.models import User 
from .models import Aluno, Galeria,Material,Curso, Modulo

class AlunoForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','first_name','email','password']
class CadastroAlunoForm(forms.ModelForm):
    username= forms.CharField(label="Nome de Usuário (Login)", widget=forms.TextInput(attrs={'class':'input-glass'}))
    password= forms.CharField(label="Senha Temporária", widget=forms.PasswordInput(attrs={'class':'input-glass'}))

    cursos=forms.ModelMultipleChoiceField(
        queryset= Curso.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Vincular aos Cursos:"
    )
    class Meta:
        model = User
        fields = ['username', 'first_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-glass'}),
            'first_name': forms.TextInput(attrs={'class': 'input-glass', 'placeholder': 'Ex: Breno'}),
            'email': forms.EmailInput(attrs={'class': 'input-glass', 'placeholder': 'email@exemplo.com'}),
            'password': forms.PasswordInput(attrs={'class': 'input-glass'}),
        }
class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['titulo', 'arquivo', 'modulo']
        
        # Widgets para o estilo Glassmorphism da EMG
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'input-glass', 
                'placeholder': 'Ex: Partitura de Flauta'
            }),
            'arquivo': forms.FileInput(attrs={
                'class': 'input-glass'
            }),
            'modulo': forms.Select(attrs={
                'class': 'input-glass'
            }),
        }
class FotoGaleriaForm(forms.ModelForm):
    class Meta:
        model = Galeria # TROQUE FotoGaleria por Galeria
        fields = ['titulo', 'imagem']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-glass', 'placeholder': 'Título da foto'}),
            'imagem': forms.FileInput(attrs={'class': 'input-glass'}),
        }
class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['nome', 'slug', 'imagem_fundo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'input-glass', 'placeholder': 'Ex: Violão Popular'}),
            'slug': forms.TextInput(attrs={'class': 'input-glass', 'placeholder': 'ex-violao-popular'}),
            'imagem_fundo': forms.FileInput(attrs={'class': 'input-glass'}),
        }
class ModuloForm(forms.ModelForm):
    class Meta:
        model = Modulo # Verifique se o nome do seu model é Modulo
        fields = ['titulo','descricao', 'curso']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'input-glass', 'placeholder': 'Ex: Básico I ou Teoria Musical'}),
            'descricao': forms.Textarea(attrs={'class': 'input-glass', 'placeholder': 'O que será estudado neste módulo...', 'rows': 3}),
            'curso': forms.Select(attrs={'class': 'input-glass'}),
        }