# 📋 PLANO DE EXECUÇÃO - AGENTE AGENDADOR COM CLICKUP CRM

## 🎯 OBJETIVO
Implementar um agente virtual funcional para a "Agência Criativa XYZ" que utiliza o ClickUp como CRM, seguindo os requisitos do teste técnico.

## 📊 ANÁLISE DO ESTADO ATUAL

### ✅ **O QUE JÁ ESTÁ IMPLEMENTADO:**

#### **Infraestrutura Base (bot/)**
- **WhatsApp Bot Funcional** (`main.js`):
  - ✅ Cliente WhatsApp Web conectado com autenticação persistente
  - ✅ API REST para envio de mensagens (`/send-message`)
  - ✅ Interface web para QR Code (`/qr`)
  - ✅ Status da conexão (`/status`)
  - ✅ Sistema de logout (`/logout`)
  - ✅ Tratamento de erros e middleware
  - ✅ Servidor Express rodando na porta 3000

- **Script Python** (`python.py`):
  - ✅ Função para envio de mensagens automáticas
  - ✅ Integração com a API do WhatsApp bot
  - ✅ Sistema de monitoramento de tempo
  - ✅ Estrutura para envio de mensagens urgentes

- **Configuração de Ambiente** (`env.example`):
  - ✅ Template completo com todas as variáveis necessárias
  - ✅ Configurações para ClickUp, Google Calendar, Email
  - ✅ Estrutura organizada por seções

#### **Estrutura do Projeto (agente-criativa-xyz/)**
- ✅ **Arquitetura definida** com separação de responsabilidades:
  - `agent_logic_python/` - Lógica do agente em Python (estrutura criada)
  - `whatsapp_handler_node/` - Handler do WhatsApp em Node.js (estrutura criada)
  - `docker-compose.yml` - Containerização (vazio)
  - `README.md` - Documentação (vazio)

#### **Documentação e Configuração**
- ✅ **Arquitetura detalhada** (`configs/arquitetura_projeto_gemini.md`):
  - ✅ Fluxo de comunicação entre Node.js e Python via API REST
  - ✅ Estrutura de microsserviços bem definida
  - ✅ Especificação de endpoints e payloads
  - ✅ Gerenciamento de estado da conversa

- ✅ **Guia de Autenticação** (`configs/auth.md`):
  - ✅ Configuração OAuth 2.0 para Google Calendar
  - ✅ Configuração de token para ClickUp
  - ✅ Deploy com túnel SSH e Nginx
  - ✅ Configuração SSL com Let's Encrypt

### ❌ **O QUE PRECISA SER IMPLEMENTADO:**

#### **Lógica do Agente (agente-criativa-xyz/agent_logic_python/)**
- ❌ **API FastAPI** (`main.py`) - Endpoint `/process-message`
- ❌ **Fluxo de conversação** (`agent.py`) - Captura de dados do cliente
- ❌ **Integração com ClickUp** (`services/clickup_service.py`) - Salvamento de dados no CRM
- ❌ **Sistema de agendamento** (`services/calendar_service.py`) - Verificação de disponibilidade
- ❌ **Funções auxiliares** (`utils.py`) - Geração de protocolo, formatação
- ❌ **Dependências Python** (`requirements.txt`) - FastAPI, requests, etc.

#### **Handler do WhatsApp (agente-criativa-xyz/whatsapp_handler_node/)**
- ❌ **Processamento de mensagens** (`index.js`) - Interpretação de entrada
- ❌ **Integração com lógica Python** - Comunicação via API REST
- ❌ **Gerenciamento de estado** - Controle do fluxo de conversa
- ❌ **Dependências Node.js** (`package.json`) - whatsapp-web.js, axios

#### **Serviços de Integração**
- ❌ **ClickUp Service** - API para CRM (estrutura criada, mas vazia)
- ❌ **Calendar Service** - Verificação de disponibilidade (estrutura criada, mas vazia)
- ❌ **Email Service** - Envio de confirmações (não criado)

## 🚀 PLANO DE IMPLEMENTAÇÃO REVISADO

### **FASE 1: Lógica do Agente Python (3-4 horas)**
1. **Implementar API FastAPI:**
   - `main.py` - Servidor FastAPI com endpoint `/process-message`
   - `requirements.txt` - Dependências necessárias

2. **Criar lógica do agente:**
   - `agent.py` - Máquina de estados para fluxo de conversação
   - `utils.py` - Funções auxiliares (geração de protocolo, formatação)

3. **Implementar serviços de integração:**
   - `services/clickup_service.py` - Integração com ClickUp CRM
   - `services/calendar_service.py` - Verificação de horários disponíveis
   - `services/email_service.py` - Envio de e-mails de confirmação

### **FASE 2: Handler WhatsApp Node.js (2-3 horas)**
1. **Implementar processamento de mensagens:**
   - `index.js` - Handler principal do WhatsApp com whatsapp-web.js
   - `package.json` - Dependências Node.js
   - Integração com a lógica Python via API REST

2. **Configurar comunicação entre serviços:**
   - Tratamento de erros e fallbacks
   - Gerenciamento de estado da conversa

### **FASE 3: Integração e Testes (2-3 horas)**
1. **Integrar todos os componentes:**
   - Testar fluxo completo end-to-end
   - Ajustar lógica de negócio
   - Implementar validações

2. **Configurar ambiente:**
   - Docker Compose funcional
   - Variáveis de ambiente
   - Documentação de uso

## 🔧 IMPLEMENTAÇÃO DETALHADA

### **Fluxo de Conversação (Conforme Teste Técnico):**
```
1. Cliente inicia: "Olá, gostaria de um serviço"
2. Agente pergunta: "Qual seu nome?"
3. Cliente responde: "João Silva"
4. Agente pergunta: "Qual seu e-mail?"
5. Cliente responde: "joao@email.com"
6. Agente pergunta: "Que tipo de serviço? (Design/Site/Social Media)"
7. Cliente escolhe: "Design"
8. Agente salva no ClickUp e sugere 3 horários
9. Cliente escolhe horário
10. Agente confirma com link Meet e protocolo
```

### **Estrutura de Dados:**
```json
{
  "cliente": {
    "nome": "João Silva",
    "email": "joao@email.com",
    "servico": "Design",
    "protocolo": "123456",
    "agendamento": {
      "data": "2024-01-15",
      "horario": "14:00",
      "link_meet": "https://meet.google.com/xyz123"
    }
  }
}
```

### **Estados da Conversa:**
```python
conversation_states = {
    "INIT": "Aguardando primeira mensagem",
    "AWAITING_NAME": "Aguardando nome do cliente",
    "AWAITING_EMAIL": "Aguardando e-mail do cliente", 
    "AWAITING_SERVICE": "Aguardando tipo de serviço",
    "AWAITING_SCHEDULE_CHOICE": "Aguardando escolha de horário",
    "COMPLETED": "Agendamento finalizado"
}
```

## 📝 ESTRUTURA FINAL DO PROJETO

```
bot/
├── main.js                    ✅ WhatsApp Bot API
├── python.py                  ✅ Script de monitoramento
├── env.example               ✅ Configurações
└── teste.js                  ✅ Teste com IA

agente-criativa-xyz/
├── agent_logic_python/
│   ├── main.py               ❌ API FastAPI
│   ├── agent.py              ❌ Lógica do agente
│   ├── utils.py              ❌ Funções auxiliares
│   ├── requirements.txt      ❌ Dependências Python
│   ├── .env                  ❌ Variáveis de ambiente
│   └── services/
│       ├── calendar_service.py    ❌ Google Calendar
│       ├── clickup_service.py     ❌ ClickUp CRM
│       └── email_service.py       ❌ Envio de e-mails
├── whatsapp_handler_node/
│   ├── index.js              ❌ Handler WhatsApp
│   └── package.json          ❌ Dependências Node
├── docker-compose.yml        ❌ Containerização
└── README.md                 ❌ Documentação

docs/
├── ✅ TESTE TÉCNICO.md       ✅ Requisitos
└── planing.md               ✅ Este documento

configs/
├── arquitetura_projeto_gemini.md  ✅ Arquitetura
└── auth.md                        ✅ Autenticação
```

## 🎯 CRITÉRIOS DE SUCESSO (Conforme Teste Técnico)

### Funcionalidades obrigatórias:
- [ ] Cliente inicia conversa e fornece dados (nome, e-mail, serviço)
- [ ] Dados são salvos no ClickUp CRM (substituindo Google Sheets)
- [ ] Sistema sugere 3 horários disponíveis
- [ ] Cliente escolhe horário e recebe confirmação
- [ ] Protocolo de 6 dígitos é gerado
- [ ] Link fictício do Google Meet é fornecido
- [ ] Fluxo completo funcional via WhatsApp

### Funcionalidades diferenciais:
- [ ] E-mail de confirmação é enviado
- [ ] Histórico de atendimentos é consultável
- [ ] Sistema funciona de forma estável
- [ ] Deploy em produção com SSL

## 🚨 PRÓXIMOS PASSOS IMEDIATOS

### **PRIORIDADE ALTA (Hoje):**
1. **Implementar `main.py`** - API FastAPI com endpoint `/process-message`
2. **Implementar `agent.py`** - Máquina de estados para conversação
3. **Implementar `services/clickup_service.py`** - Integração ClickUp
4. **Implementar `services/calendar_service.py`** - Verificação de horários
5. **Criar `requirements.txt`** - Dependências Python

### **PRIORIDADE MÉDIA (Amanhã):**
1. **Implementar `index.js`** - Handler do WhatsApp
2. **Criar `package.json`** - Dependências Node.js
3. **Implementar `utils.py`** - Funções auxiliares
4. **Implementar `services/email_service.py`** - Envio de confirmações
5. **Testar fluxo completo** - Validação end-to-end

### **PRIORIDADE BAIXA (Próximos dias):**
1. **Configurar `docker-compose.yml`** - Containerização
2. **Documentação completa** - README e instruções
3. **Configurar deploy** - Túnel SSH e Nginx
4. **Vídeo demonstrativo** - Apresentação do funcionamento

## 📋 CHECKLIST DE ENTREGA (Conforme Teste Técnico)

- [ ] Fluxo completo funcionando via WhatsApp
- [ ] Integração com ClickUp ativa (substituindo Google Sheets)
- [ ] Captura de dados do cliente (nome, e-mail, serviço)
- [ ] Sugestão de 3 horários disponíveis
- [ ] Confirmação com link Meet e protocolo
- [ ] Testes passando
- [ ] Documentação completa
- [ ] Instruções de configuração
- [ ] Exemplo de uso
- [ ] (Opcional) E-mail de confirmação
- [ ] (Opcional) Vídeo demonstrativo

## 🎯 **ESTADO ATUAL: 40% CONCLUÍDO**

**Progresso:**
- ✅ Infraestrutura base: 100%
- ✅ Documentação e arquitetura: 100%
- ❌ Lógica do agente: 0%
- ❌ Integrações: 0%
- ❌ Handler WhatsApp: 0%
- ❌ Testes e documentação: 0%

**Tempo estimado restante: 7-10 horas**

## 🔄 **DIFERENÇAS DA INFRAESTRUTURA EXISTENTE**

### **Vantagens da Infraestrutura Atual:**
- ✅ WhatsApp Bot já funcional e testado
- ✅ API REST para envio de mensagens
- ✅ Autenticação persistente
- ✅ Interface web para QR Code
- ✅ Script Python para monitoramento

### **Adaptações Necessárias:**
- 🔄 **Reutilizar** `main.js` como base para o handler WhatsApp
- 🔄 **Adaptar** `python.py` para integrar com a nova lógica do agente
- 🔄 **Manter** estrutura de autenticação e QR Code
- 🔄 **Adicionar** processamento de mensagens recebidas

### **Estratégia de Implementação:**
1. **Copiar** `main.js` para `agente-criativa-xyz/whatsapp_handler_node/index.js`
2. **Adicionar** listener para mensagens recebidas
3. **Implementar** comunicação com serviço Python
4. **Manter** funcionalidades existentes (QR, status, logout)
