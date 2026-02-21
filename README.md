# 🎵 Plataforma Escola de Música

Sistema de gestão de cursos e materiais de apoio para alunos e coordenadores, desenvolvido com Django e otimizado para alojamento no Railway com armazenamento de media no Cloudinary.

## 🚀 Funcionalidades

- **Gestão de Cursos:** Organização por Módulos, Aulas e Materiais.
- **Área do Aluno:** Visualização de conteúdos específicos dos cursos matriculados.
- **Materiais Dinâmicos:** Suporte para:
  - Ficheiros PDF (Visualização integrada).
  - Vídeos (Alojados ou via YouTube).
  - Links Externos (Google Drive, etc).
- **Painel Administrativo:** Interface completa para gestão de alunos e matrículas.
- **Galeria de Fotos:** Espaço para eventos e fotos da escola.

## 🛠️ Tecnologias Utilizadas

- **Backend:** Python / Django 5.x
- **Base de Dados:** MySQL (Railway)
- **Media & Assets:** Cloudinary (Armazenamento em nuvem)
- **Frontend:** HTML5, CSS3 (Glassmorphism design), FontAwesome.
- **Deploy:** Railway.app

## 📦 Configuração Local

1. **Clonar o repositório:**
   ```bash
   git clone [https://github.com/seu-utilizador/nome-do-repo.git](https://github.com/seu-utilizador/nome-do-repo.git)
   cd nome-do-repo
2. **Criar e ativar o ambiente virtual:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   .venv\Scripts\activate     # Windows
3. **Instalar as dependências:**
   ```bash
   pip install -r requirements.txt
4. **Configurar o .env:**
   ```bash
   DEBUG=True
   SECRET_KEY=sua_chave_secreta
   CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
   DATABASE_URL=postgres://user:pass@host:port/dbname
5. **Executar as migrações:**
   ```bash
   python manage.py migrate
6. **Iniciar o servidor:**
   ```bash
   python manage.py runserver
