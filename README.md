# FakePinterest 📌

Projeto desenvolvido para simular a experiência de um pequeno Pinterest, focado no upload, visualização e organização de imagens.

## 🚀 Tecnologias Utilizadas

- **Python + Flask** (Backend)
- **HTML + Jinja2** (Templates)
- **CSS** (Estilização)
- **JavaScript** (Upload dinâmico e animações)
- **SQLite** (Banco de dados leve)
- **Pillow (PIL)** (Tratamento de imagens)

## 🎯 Funcionalidades Principais

- Upload de imagens organizadas em subpastas por usuário (`static/fotos_posts/usuario_X/`).
- Correção automática de extensões suspeitas para `.jpg`.
- Upload via formulário Ajax + preview da imagem antes do envio.
- Organização dinâmica das imagens no feed, simulando estilo Pinterest.
- Animações suaves de carregamento das imagens.
- Exclusão de imagens que remove tanto do banco de dados quanto do sistema de arquivos.
- Mensagens visuais (flash) para feedback de ações.
- Separação de templates em componentes e páginas para melhor manutenção.

## 🛠 Como rodar localmente

```bash
git clone https://github.com/carlosmorais-git/ProjetoFakePinterest.git
cd ProjetoFakePinterest
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows
pip install -r requirements.txt
flask --app projeto run --debug

- Crie a estrutura static/fotos_posts/ caso não exista.
- As imagens serão organizadas automaticamente conforme os uploads.



📢 Observações Finais:

Esse projeto foi uma grande oportunidade de aprendizado sobre:

- Organização de uploads com Flask
- Gerenciamento real de arquivos no servidor
- Separação de responsabilidades entre frontend e backend
- Tomada de decisões para manter a estabilidade do projeto

Obrigado por acompanhar essa jornada! 🚀
```
