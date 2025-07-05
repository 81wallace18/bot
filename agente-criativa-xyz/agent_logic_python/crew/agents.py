from crewai import Agent
from crewai_tools import MCPServerAdapter

# Parâmetros para se conectar ao contêiner do Google Calendar MCP
# Usamos o nome do serviço do docker-compose como hostname
google_calendar_server_params = {
    "url": "http://google_calendar_mcp:8001/mcp",
    "transport": "streamable-http"
}

def get_agents():
    """
    Retorna instâncias dos agentes CrewAI com suas tools MCP.
    """
    with MCPServerAdapter(google_calendar_server_params) as google_calendar_tools:

        calendar_manager = Agent(
            role='Gerente de Agenda',
            goal='Gerenciar eventos e disponibilidade no Google Agenda usando as ferramentas disponíveis',
            backstory='Especialista em organização de tempo e reuniões.',
            tools=google_calendar_tools, # As ferramentas são carregadas dinamicamente do MCP
            verbose=True
        )

        # Você pode adicionar outros agentes aqui, se necessário
        # Por exemplo, um agente para o ClickUp, se você tiver um MCP para ele

        return calendar_manager