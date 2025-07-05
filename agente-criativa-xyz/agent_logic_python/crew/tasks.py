from crewai import Task

def get_tasks(calendar_manager, task_manager, user_id, message):
    """
    Retorna as tasks CrewAI para o fluxo de atendimento.
    """
    create_calendar_event_task = Task(
        description=(
            f"Agende um horário para o usuário {user_id} com base na mensagem: '{message}'. "
            "Sugira 3 horários disponíveis e crie o evento no Google Calendar."
        ),
        agent=calendar_manager,
        expected_output='Confirmação do evento criado com detalhes.'
    )

    create_clickup_task = Task(
        description=(
            f"Crie uma tarefa no ClickUp para o usuário {user_id} com base na mensagem: '{message}'."
        ),
        agent=task_manager,
        expected_output='Confirmação da tarefa criada com ID e detalhes.'
    )

    return [create_calendar_event_task, create_clickup_task] 