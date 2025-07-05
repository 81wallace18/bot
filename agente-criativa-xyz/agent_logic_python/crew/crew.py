from crewai import Crew, Process
from .agents import get_agents
from .tasks import get_tasks

def run_crew(user_id, message):
    """
    Orquestra a execução da CrewAI para o fluxo de atendimento.
    """
    calendar_manager, task_manager = get_agents()
    tasks = get_tasks(calendar_manager, task_manager, user_id, message)
    crew = Crew(
        agents=[calendar_manager, task_manager],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )
    result = crew.kickoff()
    return result 