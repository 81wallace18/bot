from crewai import Crew, Process
from .agents import get_agents
from .tasks import get_tasks

def run_crew(user_id: str, message: str, conversation_state: dict = None):
    """
    Orquestra a execução da CrewAI para o fluxo de atendimento completo.
    
    Args:
        user_id: ID do usuário no WhatsApp
        message: Mensagem recebida
        conversation_state: Estado atual da conversa
    
    Returns:
        Resultado da execução da crew
    """
    
    # Inicializa estado se não fornecido
    if conversation_state is None:
        conversation_state = {"stage": "initial", "data": {}}
    
    # Obtém os agentes especializados
    agents = get_agents()
    
    # Obtém as tasks para o fluxo
    tasks = get_tasks(agents, user_id, message, conversation_state)
    
    # Cria a crew com todos os agentes
    crew = Crew(
        agents=list(agents.values()),  # Todos os agentes
        tasks=tasks,
        process=Process.sequential,  # Executa tasks em sequência
        verbose=True
    )
    
    # Executa a crew
    result = crew.kickoff()
    
    return {
        "result": result,
        "conversation_state": conversation_state,
        "agents_used": list(agents.keys())
    } 