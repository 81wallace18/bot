from crewai import Task

def get_tasks(agents, user_id: str, message: str, conversation_state: dict):
    """
    Retorna as tasks CrewAI para o fluxo de atendimento completo.
    
    Args:
        agents: Dicionário com os agentes especializados
        user_id: ID do usuário no WhatsApp
        message: Mensagem recebida
        conversation_state: Estado atual da conversa
    """
    
    # Task 1: Análise inicial e extração de dados
    analyze_message_task = Task(
        description=(
            f"Analise a mensagem do usuário {user_id}: '{message}'. "
            "Extraia informações de contato disponíveis (nome, email, telefone) "
            "e identifique o que ainda precisa ser coletado. "
            "Estado atual da conversa: {conversation_state}"
        ),
        agent=agents['data_collector'],
        expected_output='Dicionário com dados extraídos e informações faltantes.'
    )
    
    # Task 2: Coleta de dados faltantes
    collect_data_task = Task(
        description=(
            "Com base na análise anterior, identifique quais informações ainda precisam "
            "ser coletadas do cliente e formule perguntas específicas para obtê-las. "
            "Seja cordial e profissional."
        ),
        agent=agents['data_collector'],
        expected_output='Lista de perguntas para coletar dados faltantes.'
    )
    
    # Task 3: Criação/atualização no ClickUp
    create_lead_task = Task(
        description=(
            "Crie ou atualize o lead no ClickUp CRM com os dados coletados. "
            "Use as ferramentas do MCP ClickUp para gerenciar a task. "
            "Se for um novo lead, crie uma nova task. "
            "Se for atualização, busque pela task existente e atualize."
        ),
        agent=agents['crm_manager'],
        expected_output='Confirmação da task criada/atualizada no ClickUp com ID.'
    )
    
    # Task 4: Verificação de disponibilidade
    check_availability_task = Task(
        description=(
            "Verifique a disponibilidade no Google Calendar para os próximos 7 dias. "
            "Identifique 3 horários disponíveis (manhã, tarde, meio-dia) "
            "e sugira opções para o cliente."
        ),
        agent=agents['scheduler'],
        expected_output='Lista de 3 horários disponíveis com datas e horários.'
    )
    
    # Task 5: Criação do evento
    create_event_task = Task(
        description=(
            "Com base na escolha do cliente, crie o evento no Google Calendar. "
            "Use as ferramentas do MCP Google Calendar para criar o evento "
            "com link da reunião e detalhes apropriados."
        ),
        agent=agents['scheduler'],
        expected_output='Confirmação do evento criado com link da reunião.'
    )
    
    # Task 6: Geração de protocolo e confirmação
    confirmation_task = Task(
        description=(
            "Gere um protocolo único de 6 dígitos e prepare a confirmação final. "
            "Use as ferramentas disponíveis para gerar o protocolo e "
            "formular uma mensagem de confirmação profissional."
        ),
        agent=agents['communication'],
        expected_output='Protocolo gerado e mensagem de confirmação.'
    )
    
    return [
        analyze_message_task,
        collect_data_task, 
        create_lead_task,
        check_availability_task,
        create_event_task,
        confirmation_task
    ] 