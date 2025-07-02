# 🎙️ Transcrição de Reuniões

Uma aplicação web completa para transcrever gravações de reuniões com identificação automática de falantes e edição manual dos nomes dos participantes.

## ✨ Funcionalidades

- **Upload de Arquivos**: Suporte para formatos M4A, MP3, WAV, MP4, AVI, MOV
- **Transcrição Automática**: Utiliza OpenAI Whisper para transcrição precisa em português
- **Identificação de Falantes**: Detecta automaticamente diferentes falantes na gravação
- **Edição Manual**: Interface para editar e personalizar os nomes dos participantes
- **Resumo Inteligente**: Gera automaticamente resumo dos pontos principais da reunião
- **Exportação**: Baixa a transcrição completa em formato texto
- **Interface Responsiva**: Funciona perfeitamente em desktop e mobile

## 🚀 Deploy no Render

### Pré-requisitos
- Conta no [Render](https://render.com)
- Repositório Git com o código

### Passos para Deploy

1. **Faça upload do código para um repositório Git** (GitHub, GitLab, etc.)

2. **Acesse o Render Dashboard**
   - Vá para [render.com](https://render.com)
   - Faça login na sua conta

3. **Criar novo Web Service**
   - Clique em "New +"
   - Selecione "Web Service"
   - Conecte seu repositório Git

4. **Configurar o serviço**
   - **Name**: `transcricao-reunioes`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python src/main.py`
   - **Plan**: Free (ou escolha um plano pago para melhor performance)

5. **Variáveis de ambiente** (opcional)
   - `PYTHON_VERSION`: `3.11.0`

6. **Deploy**
   - Clique em "Create Web Service"
   - Aguarde o build e deploy (pode levar alguns minutos)

### Configuração Automática

O projeto inclui um arquivo `render.yaml` que configura automaticamente o deploy. Basta conectar o repositório e o Render detectará as configurações.

## 🛠️ Desenvolvimento Local

### Instalação

```bash
# Clone o repositório
git clone <seu-repositorio>
cd transcricao-reunioes

# Ative o ambiente virtual
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt
```

### Executar localmente

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Executar aplicação
python src/main.py
```

A aplicação estará disponível em `http://localhost:5000`

## 📋 Dependências Principais

- **Flask**: Framework web
- **OpenAI Whisper**: Transcrição de áudio
- **PyDub**: Processamento de áudio
- **Flask-CORS**: Suporte a CORS
- **Torch/TorchAudio**: Backend para Whisper

## 🎯 Como Usar

1. **Acesse a aplicação** no navegador
2. **Faça upload** do arquivo de áudio da reunião
3. **Aguarde o processamento** (pode levar alguns minutos dependendo do tamanho)
4. **Visualize a transcrição** com falantes identificados automaticamente
5. **Edite os nomes** dos participantes conforme necessário
6. **Revise o resumo** dos pontos principais
7. **Exporte** a transcrição completa

## ⚠️ Limitações

- **Tamanho máximo**: 100MB por arquivo
- **Formatos suportados**: M4A, MP3, WAV, MP4, AVI, MOV
- **Idioma**: Otimizado para português brasileiro
- **Performance**: Processamento pode ser lento no plano gratuito do Render

## 🔧 Estrutura do Projeto

```
transcricao-reunioes/
├── src/
│   ├── main.py              # Aplicação principal Flask
│   ├── routes/
│   │   ├── transcricao.py   # Rotas da API de transcrição
│   │   └── user.py          # Rotas de usuário (template)
│   ├── models/              # Modelos do banco de dados
│   ├── static/
│   │   └── index.html       # Interface web
│   └── database/            # Banco de dados SQLite
├── venv/                    # Ambiente virtual Python
├── requirements.txt         # Dependências Python
├── render.yaml             # Configuração do Render
└── README.md               # Este arquivo
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🆘 Suporte

Se encontrar problemas:

1. Verifique se todas as dependências estão instaladas
2. Confirme que o arquivo de áudio está em formato suportado
3. Verifique os logs do Render para erros de deploy
4. Para arquivos muito grandes, considere comprimir o áudio antes do upload

---

Desenvolvido com ❤️ para facilitar a transcrição de reuniões de trabalho.

