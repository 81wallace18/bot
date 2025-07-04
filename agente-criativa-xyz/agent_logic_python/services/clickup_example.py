"""
Exemplo de uso do ClickUp Service
Este arquivo demonstra como usar as funções do clickup_service.py
"""

from clickup_service import (
    create_lead, 
    update_stage, 
    update_agreement, 
    mark_email_sent,
    find_task_by_protocol,
    get_tasks_by_stage,
    get_all_tasks
)

def exemplo_criar_lead():
    """Exemplo de como criar um novo lead"""
    
    # Dados do cliente
    client_data = {
        "nome": "João Silva",
        "email": "joao@email.com",
        "whatsapp": "5511999998888",
        "servico": "Design",
        "protocolo": "123456",
        "agendamento": {
            "data": "2024-01-15",
            "horario": "14:00",
            "link_meet": "https://meet.google.com/xyz123"
        }
    }
    
    # Cria o lead no ClickUp
    result = create_lead(client_data)
    
    if result["success"]:
        print(f"✅ Lead criado com sucesso!")
        print(f"   Task ID: {result['task_id']}")
        print(f"   URL: {result['task_url']}")
        return result["task_id"]
    else:
        print(f"❌ Erro ao criar lead: {result['error']}")
        return None

def exemplo_atualizar_estagio(task_id: str):
    """Exemplo de como atualizar o estágio de uma task"""
    
    # Atualiza para "coletando_dados"
    result = update_stage(task_id, "coletando_dados")
    
    if result["success"]:
        print(f"✅ Estágio atualizado para: {result['stage']}")
    else:
        print(f"❌ Erro ao atualizar estágio: {result['error']}")

def exemplo_atualizar_agendamento(task_id: str):
    """Exemplo de como atualizar dados de agendamento"""
    
    agreement_data = {
        "data": "2024-01-20",
        "horario": "15:30",
        "link_meet": "https://meet.google.com/abc456",
        "protocolo": "789012"
    }
    
    result = update_agreement(task_id, agreement_data)
    
    if result["success"]:
        print(f"✅ Agendamento atualizado com sucesso!")
    else:
        print(f"❌ Erro ao atualizar agendamento: {result['error']}")

def exemplo_marcar_email_enviado(task_id: str):
    """Exemplo de como marcar e-mail como enviado"""
    
    result = mark_email_sent(task_id)
    
    if result["success"]:
        print(f"✅ E-mail marcado como enviado!")
    else:
        print(f"❌ Erro ao marcar e-mail: {result['error']}")

def exemplo_buscar_por_protocolo():
    """Exemplo de como buscar uma task pelo protocolo"""
    
    protocol = "123456"
    task = find_task_by_protocol(protocol)
    
    if task:
        print(f"✅ Task encontrada!")
        print(f"   Nome: {task['name']}")
        print(f"   ID: {task['id']}")
        print(f"   URL: {task['url']}")
        return task
    else:
        print(f"❌ Task não encontrada para o protocolo: {protocol}")
        return None

def exemplo_buscar_por_estagio():
    """Exemplo de como buscar tasks por estágio"""
    
    stage = "novo_lead"
    tasks = get_tasks_by_stage(stage)
    
    print(f"📊 Tasks no estágio '{stage}': {len(tasks)}")
    
    for task in tasks:
        print(f"   - {task['name']} (ID: {task['id']})")
    
    return tasks

def exemplo_buscar_todas():
    """Exemplo de como buscar todas as tasks"""
    
    tasks = get_all_tasks()
    
    print(f"📊 Total de tasks: {len(tasks)}")
    
    for task in tasks:
        print(f"   - {task['name']} (ID: {task['id']})")
    
    return tasks

def fluxo_completo_exemplo():
    """Exemplo de fluxo completo do agente"""
    
    print("🚀 Iniciando fluxo completo do agente...")
    
    # 1. Cliente inicia conversa
    print("\n1️⃣ Cliente inicia conversa...")
    
    # 2. Coleta dados do cliente
    print("\n2️⃣ Coletando dados do cliente...")
    client_data = {
        "nome": "Maria Santos",
        "email": "maria@email.com",
        "whatsapp": "551188887777",
        "servico": "Site",
        "protocolo": "654321"
    }
    
    # 3. Cria lead no ClickUp
    print("\n3️⃣ Criando lead no ClickUp...")
    result = create_lead(client_data)
    
    if not result["success"]:
        print("❌ Falha no fluxo - erro ao criar lead")
        return
    
    task_id = result["task_id"]
    
    # 4. Atualiza estágio para "dados_completos"
    print("\n4️⃣ Atualizando estágio para 'dados_completos'...")
    update_stage(task_id, "dados_completos")
    
    # 5. Cliente escolhe horário
    print("\n5️⃣ Cliente escolhe horário...")
    agreement_data = {
        "data": "2024-01-25",
        "horario": "10:00",
        "link_meet": "https://meet.google.com/def789",
        "protocolo": "654321"
    }
    
    # 6. Atualiza agendamento
    print("\n6️⃣ Atualizando agendamento...")
    update_agreement(task_id, agreement_data)
    
    # 7. Atualiza estágio para "agendado"
    print("\n7️⃣ Atualizando estágio para 'agendado'...")
    update_stage(task_id, "agendado")
    
    # 8. Envia e-mail de confirmação
    print("\n8️⃣ Enviando e-mail de confirmação...")
    mark_email_sent(task_id)
    
    print("\n✅ Fluxo completo finalizado com sucesso!")
    print(f"   Task ID: {task_id}")
    print(f"   Protocolo: {client_data['protocolo']}")

if __name__ == "__main__":
    # Descomente a função que deseja testar
    
    # exemplo_criar_lead()
    # exemplo_buscar_por_protocolo()
    # exemplo_buscar_por_estagio()
    # exemplo_buscar_todas()
    fluxo_completo_exemplo() 