# 🐳 Docker Setup - Agente Criativa XYZ

Este documento explica como configurar e executar o projeto usando Docker Compose.

## 📋 Pré-requisitos

- Docker instalado
- Docker Compose instalado
- Git

## 🚀 Execução Rápida

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd agente-criativa-xyz
```

### 2. Configure as variáveis de ambiente
```bash
# Copie o arquivo de exemplo
cp docker.env.example docker.env

# Edite o arquivo com suas credenciais
nano docker.env
```

### 3. Execute o build
```bash
# Usando o script automatizado
./build.sh

# Ou manualmente
docker compose up --build -d
```

## 🔧 Configuração Detalhada

### Variáveis de Ambiente (docker.env)

```env
# ClickUp CRM
CLICKUP_API_TOKEN=seu_token_pessoal_aqui
CLICKUP_TEAM_ID=90131707178
CLICKUP_SPACE_ID=90137167172
CLICKUP_FOLDER_ID=90139078968
CLICKUP_LIST_ID=901315684298

# Google Calendar (opcional)
GOOGLE_CALENDAR_CREDENTIALS_FILE=/app/credentials.json
```

### Estrutura dos Containers

- **agent_logic** (Python/FastAPI): Porta 8000
  - Lógica do agente virtual
  - Integração com ClickUp e Google Calendar
  - API REST para comunicação

- **whatsapp_handler** (Node.js): Porta 3000
  - Interface com WhatsApp Web
  - Comunicação com o agente Python

## 📊 Comandos Úteis

### Verificar status
```bash
docker compose ps
```

### Ver logs
```bash
# Todos os serviços
docker compose logs -f

# Serviço específico
docker compose logs -f agent_logic
docker compose logs -f whatsapp_handler
```

### Parar serviços
```bash
docker compose down
```

### Rebuild após mudanças
```bash
docker compose down
docker compose up --build -d
```

### Acessar container
```bash
# Python container
docker compose exec agent_logic bash

# Node.js container
docker compose exec whatsapp_handler bash
```

## 🌐 URLs dos Serviços

- **Agent Logic API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **WhatsApp Handler**: http://localhost:3000

## 🔍 Troubleshooting

### Erro de permissão
```bash
sudo chmod +x build.sh
```

### Erro de porta em uso
```bash
# Verificar portas em uso
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :3000

# Parar processo que está usando a porta
sudo kill -9 <PID>
```

### Erro de build do Python
```bash
# Limpar cache do Docker
docker system prune -a

# Rebuild sem cache
docker compose build --no-cache
```

### Erro de dependências
```bash
# Verificar logs do build
docker compose logs agent_logic

# Acessar container e instalar manualmente
docker compose exec agent_logic pip install -r requirements.txt
```

## 📝 Notas Importantes

1. **Primeira execução**: O WhatsApp precisará de autenticação via QR Code
2. **Credenciais**: Nunca commite arquivos `.env` ou `credentials.json`
3. **Volumes**: Os volumes permitem desenvolvimento em tempo real
4. **Logs**: Use `docker compose logs -f` para monitorar em tempo real

## 🔒 Segurança

- As credenciais são carregadas via arquivo `docker.env`
- O arquivo `.env` está no `.dockerignore` para não ser incluído na imagem
- Use secrets do Docker em produção para credenciais sensíveis

## 📚 Próximos Passos

1. Configure suas credenciais no `docker.env`
2. Execute `./build.sh`
3. Acesse http://localhost:8000/docs para testar a API
4. Configure o WhatsApp Web via QR Code
5. Teste o fluxo completo do agente 