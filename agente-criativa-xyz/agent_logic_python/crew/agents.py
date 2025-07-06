from crewai import Agent
from crewai.tools import MCPServerAdapter
from tools.protocol_tool import ProtocolTool
from tools.date_tool import DateTool
from tools.contact_tool import ContactTool

# Parâmetros para MCPs
google_calendar_server_params = {
    "url": "http://google_calendar_mcp:8001/mcp",
    "transport": "streamable-http"
}

clickup_server_params = {
    "url": "http://clickup_mcp:8002/mcp", 
    "transport": "streamable-http"
}

def get_agents():
    """
    Retorna instâncias dos agentes CrewAI com integração MCP + Tools customizadas.
    """
    
    # Tools customizadas (lógica local)
    custom_tools = [
        ProtocolTool(),
        DateTool(), 
        ContactTool()
    ]
    
    # Agente de Coleta de Dados
    data_collector = Agent(
        role='Coletor de Dados',
        goal='Extrair e validar informações de contato do cliente',
        backstory='Especialista em análise de mensagens e extração de dados de contato.',
        tools=custom_tools,
        verbose=True
    )
    
    # Agente de Gestão CRM (usando MCP ClickUp)
    with MCPServerAdapter(clickup_server_params) as clickup_tools:
        crm_manager = Agent(
            role='Gerente de CRM',
            goal='Gerenciar leads e tasks no ClickUp CRM',
            backstory='Especialista em gestão de pipeline de vendas e leads.',
            tools=clickup_tools + custom_tools,  # MCP + Tools customizadas
            verbose=True
        )
    
    # Agente de Agendamento (usando MCP Google Calendar)
    with MCPServerAdapter(google_calendar_server_params) as calendar_tools:
        scheduler = Agent(
            role='Agente de Agendamento',
            goal='Gerenciar agenda e criar eventos no Google Calendar',
            backstory='Especialista em otimização de horários e disponibilidade.',
            tools=calendar_tools + custom_tools,  # MCP + Tools customizadas
            verbose=True
        )
    
    # Agente de Comunicação (usando serviço local)
    communication_agent = Agent(
        role='Agente de Comunicação',
        goal='Enviar confirmações e e-mails de forma profissional',
        backstory='Especialista em comunicação clara e eficaz.',
        tools=custom_tools,  # Apenas tools customizadas
        verbose=True
    )
    
    return {
        'data_collector': data_collector,
        'crm_manager': crm_manager, 
        'scheduler': scheduler,
        'communication': communication_agent
    }