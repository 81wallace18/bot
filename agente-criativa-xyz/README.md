docker compose up --build -d
docker ps
docker logs -f agente-criativa-xyz-whatsapp_handler-1

# 🚀 Agente Virtual - Agência Criativa XYZ

Este projeto implementa um agente virtual inteligente para atendimento via WhatsApp, integração com ClickUp CRM e Google Calendar, orquestrado por CrewAI. A infraestrutura é baseada em microsserviços Python (FastAPI) e Node.js, com deploy via Docker Compose.

---

## 📦 Instalação Rápida (Docker Compose)

### 1. Pré-requisitos
- Docker e Docker Compose instalados
- Git

### 2. Clone o repositório
```bash
git clone <seu-repositorio>
cd agente-criativa-xyz
```

### 3. Configure as variáveis de ambiente
```bash
cp docker.env.example docker.env
nano docker.env  # Preencha com seus tokens e IDs
```

### 4. Build e deploy dos containers
```bash
chmod +x build.sh
./build.sh
```

### 5. Primeira execução
- O WhatsApp Handler pedirá autenticação via QR Code no terminal.
- Acesse a API Python: http://localhost:8000/docs
- Acesse o WhatsApp Handler: http://localhost:3000

---

## 🧠 Estrutura do Projeto

```
agent_logic_python/   # Lógica do agente (Python, FastAPI, CrewAI)
whatsapp_handler_node/ # Handler WhatsApp (Node.js)
docker-compose.yml    # Orquestração dos serviços
build.sh              # Script de build automatizado
docker.env            # Variáveis de ambiente (NUNCA commite)
```

---

## ⚙️ Configuração de Ambiente

Edite o arquivo `docker.env` com suas credenciais:

```
CLICKUP_API_TOKEN=seu_token_pessoal_aqui
CLICKUP_TEAM_ID=90131707178
CLICKUP_SPACE_ID=90137167172
CLICKUP_FOLDER_ID=90139078968
CLICKUP_LIST_ID=901315684298
GOOGLE_CALENDAR_CREDENTIALS_FILE=/app/credentials.json
```

---

## 🐳 Comandos Docker Úteis

- Subir tudo: `./build.sh` ou `docker compose up --build -d`
- Ver status: `docker compose ps`
- Logs: `docker compose logs -f`
- Parar: `docker compose down`
- Acessar container: `docker compose exec agent_logic bash`

---

## 🧩 CrewAI: Execução e Desenvolvimento

- O fluxo principal é orquestrado por CrewAI (ver `agent_logic_python/crew/`)
- Para rodar crews/flows customizados, use o CLI do CrewAI:
  ```bash
  # Instale o CLI se desejar (opcional)
  pip install crewai
  # Ou use o comando oficial se estiver usando uv
  # uv tool install crewai
  ```
- Para rodar manualmente:
  ```bash
  docker compose exec agent_logic bash
  python main.py
  ```

---

## 📝 Notas Importantes

- **Primeira execução:** O WhatsApp precisa de autenticação QR Code
- **Credenciais:** Nunca commite arquivos `.env` ou `credentials.json`
- **Volumes:** O código é montado como volume para hot reload
- **Logs:** Use `docker compose logs -f` para monitorar

---

## 🌐 URLs dos Serviços
- **API Python:** http://localhost:8000
- **Docs FastAPI:** http://localhost:8000/docs
- **WhatsApp Handler:** http://localhost:3000

---

## 📚 Referências
- [CrewAI Docs](https://docs.crewai.com/)
- [ClickUp API](https://developer.clickup.com/)
- [Google Calendar MCP](https://github.com/nspady/google-calendar-mcp)
- [ClickUp MCP](https://github.com/taazkareem/clickup-mcp-server)

---

## 🛠️ Troubleshooting
- Erro de permissão: `sudo chmod +x build.sh`
- Porta em uso: `sudo netstat -tulpn | grep :8000`
- Erro de build: `docker compose logs agent_logic`
- Instalar dependências manualmente:
  ```bash
  docker compose exec agent_logic pip install -r requirements.txt
  ```

---

**Pronto! Seu agente virtual está rodando e pronto para atender clientes via WhatsApp, registrar leads no ClickUp e agendar reuniões no Google Calendar.**
