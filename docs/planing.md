# 📋 PLANO DE EXECUÇÃO ATUALIZADO - AGENTE AGENDADOR COM CREWAI, MCP, CLICKUP E GOOGLE CALENDAR

## 🎯 OBJETIVO
Implementar um agente virtual robusto, seguro e escalável, utilizando CrewAI para orquestração de agentes, MCP para integração com ClickUp e Google Calendar, e Docker Compose para deploy seguro.

---

## 🏗️ ARQUITETURA ATUALIZADA

### **Microsserviços**
- **Handler WhatsApp (Node.js):** Já funcional, responsável pela interface com o usuário.
- **Lógica do Agente (Python):** Agora baseada em CrewAI, com agentes especializados e integração via MCP.

### **Estrutura de Pastas Recomendada**
```
agent_logic_python/
├── main.py
├── agent.py
├── crew/
│   ├── agents.py
│   ├── tasks.py
│   └── crew.py
├── tools/
│   ├── protocol_tool.py
│   └── date_tool.py
├── mcp/
│   ├── google_calendar.py
│   └── clickup.py
├── services/
│   ├── clickup_service.py
│   ├── calendar_service.py
│   └── email_service.py
├── utils.py
├── requirements.txt
└── .env
```

---

## 🔗 INTEGRAÇÃO COM MCP

- **Servidores MCP**:
  - Google Calendar: [nspady/google-calendar-mcp](https://github.com/nspady/google-calendar-mcp)
  - ClickUp: [taazkareem/clickup-mcp-server](https://github.com/taazkareem/clickup-mcp-server)
- **Orquestração**: Docker Compose, com segredos montados via `/run/secrets/`.
- **Segurança**: Nunca expor segredos em variáveis de ambiente ou código. Usar HTTPS em produção.

---

## 🧠 CREWAI: AGENTES E TAREFAS

- **Agentes**:
  - Gerente de Agenda (Google Calendar MCP)
  - Gerente de Tarefas (ClickUp MCP)
- **Ferramentas (Tools)**:
  - Protocolo aleatório (6 dígitos)
  - Manipulação de datas
- **Tasks**:
  - Coleta de dados do cliente
  - Criação de tarefa no ClickUp
  - Sugestão e agendamento de horários no Google Calendar
  - Confirmação e envio de protocolo/link

---

## 🚀 PLANO DE IMPLEMENTAÇÃO

### **Fase 1: Infraestrutura**
- Refatorar `agent_logic_python` para a nova estrutura.
- Adicionar dependências: `crewai`, `crewai_tools`, `mcp`, etc.
- Configurar Docker Compose para os MCPs e agente Python.

### **Fase 2: Integração MCP**
- Subir servidores MCP do Google Calendar e ClickUp via Docker.
- Implementar adapters MCP no Python (`mcp/google_calendar.py`, `mcp/clickup.py`).
- Testar conexão e autenticação.

### **Fase 3: CrewAI**
- Definir agentes e tarefas em `crew/`.
- Integrar tools customizadas.
- Orquestrar fluxo de atendimento completo.

### **Fase 4: Testes e Segurança**
- Testes unitários e de integração.
- Garantir que segredos estão protegidos.
- Validar fluxo end-to-end via WhatsApp.

---

## ✅ CRITÉRIOS DE SUCESSO

- [ ] Fluxo completo via WhatsApp, CrewAI e MCP.
- [ ] Integração ClickUp e Google Calendar 100% via MCP.
- [ ] Segurança de segredos garantida.
- [ ] Documentação e exemplos de uso atualizados.

---

## 📚 REFERÊNCIAS

- [Relatório Gemini: Docker, MCP e CrewAI](docs/relatorio_gemini_docker_mcp_crewia.md)
- [Revisão e próximos passos](docs/review_planning.md)
- [Arquitetura detalhada](configs/arquitetura_projeto_gemini.md)
- [Google Calendar MCP](https://github.com/nspady/google-calendar-mcp)
- [ClickUp MCP](https://github.com/taazkareem/clickup-mcp-server)

---

**Próximo passo:** Refatorar a estrutura do `agent_logic_python` e iniciar a configuração dos MCPs e CrewAI.
