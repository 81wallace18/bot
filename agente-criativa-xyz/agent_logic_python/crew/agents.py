from crewai import Agent
from crewai_tools import MCPServerAdapter

# Parâmetros MCP (ajustar URLs conforme docker-compose)
google_calendar_server_params = {
    "url": "http://localhost:8001/mcp",
    "transport": "streamable-http"
}
clickup_server_params = {
    "url": "http://localhost:8002/mcp",
    "transport": "streamable-http"
}

def get_agents():
    """
    Retorna instâncias dos agentes CrewAI com suas tools MCP.
    """
    with MCPServerAdapter(google_calendar_server_params) as google_calendar_tools, \
         MCPServerAdapter(clickup_server_params) as clickup_tools:

        calendar_manager = Agent(
            role='Gerente de Agenda',
            goal='Gerenciar eventos e disponibilidade no Google Agenda',
            backstory='Especialista em organização de tempo e reuniões.',
            tools=google_calendar_tools,
            verbose=True
        )

        task_manager = Agent(
            role='Gerente de Tarefas',
            goal='Criar, atualizar e acompanhar tarefas no ClickUp',
            backstory='Profissional organizado para garantir execução de tarefas.',
            tools=clickup_tools,
            verbose=True
        )

        return calendar_manager, task_manager 