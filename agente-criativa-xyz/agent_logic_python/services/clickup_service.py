import os
import requests
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

class ClickUpService:
    """
    Serviço para integração com a API do ClickUp CRM
    """
    
    def __init__(self):
        self.api_token = os.getenv("CLICKUP_API_TOKEN")
        self.team_id = os.getenv("CLICKUP_TEAM_ID", "90131707178")
        self.space_id = os.getenv("CLICKUP_SPACE_ID", "90137167172")
        self.folder_id = os.getenv("CLICKUP_FOLDER_ID", "90139078968")
        self.list_id = os.getenv("CLICKUP_LIST_ID", "901315684298")
        
        self.base_url = "https://api.clickup.com/api/v2"
        self.headers = {
            "Authorization": self.api_token,
            "Content-Type": "application/json"
        }
        
        # Mapeamento dos IDs dos campos personalizados
        self.custom_fields = {
            "company": "5e0e786d-3445-41bc-9d2b-35eb4ef7afa1",
            "email": "bcf972ff-4b92-4db9-8794-2e25db6c70bf",
            "phone": "9aa55830-6f47-4172-aa3f-3a4930812c9b",
            "estimated_value": "5c603f3a-2e95-469c-b20b-23d9bcbd1e3f",
            "last_contact": "e41827b5-f0bb-4e43-986f-7a1befcb3c24",
            "meeting_date": "d073af77-6cff-4843-a36c-4e25dc801362",
            "meeting_link": "489cab94-f228-4e18-a4f4-2d7f890c34a9",
            "protocol": "8b5e8588-fec5-41b1-a484-974783e7d664",
            "service_type": "5f847a5b-f337-473e-8b21-5ec4b78c6346",
            "opportunity_stage": "77ebedc4-f480-4397-bf56-d691e9f884f1",
            "opportunity_type": "b85c6017-344e-42d4-ad70-9c33ba8b6613",
            "email_sent": "ffb30e97-571f-4b9c-b2a6-350bb32294e8"
        }
        
        # Mapeamento dos status (Opportunity Stage)
        self.stage_mapping = {
            "novo_lead": 0,           # 🆕 Novo Lead
            "coletando_dados": 1,     # 🔎 Coletando_dados
            "dados_completos": 2,     # ✅ Dados Completo
            "agendamento_pendente": 3, # 📅 Agendamento Pendente
            "agendado": 4,            # Agendado
            "reuniao_realizada": 5,   # ✅ Reunião Realizada
            "convertido": 6,          # 💵 Convertido
            "perdido": 7              # ❌ Perdido
        }
        
        # Mapeamento dos tipos de serviço
        self.service_mapping = {
            "Design": "81eb9cdc-465f-4485-9437-3b9059be5374",      # Curativo (adaptar para Design)
            "Site": "376b2f92-d3a6-42ce-be3e-624837f4d7e8",       # Retirada de pontos (adaptar para Site)
            "Social Media": "6d3874d6-6095-40f4-b485-3007703c1b73" # Furo humanizado (adaptar para Social Media)
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Faz uma requisição para a API do ClickUp
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=self.headers)
            elif method.upper() == "POST":
                response = requests.post(url, headers=self.headers, json=data or {})
            elif method.upper() == "PUT":
                response = requests.put(url, headers=self.headers, json=data or {})
            else:
                raise ValueError(f"Método HTTP não suportado: {method}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Erro na requisição para ClickUp: {e}")
            return {"error": str(e)}

    def create_lead_task(self, client_data: Dict[str, Any]) -> Dict:
        """
        Cria uma nova task no ClickUp com os dados do cliente
        
        Args:
            client_data: Dicionário com dados do cliente
                {
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
        """
        
        # Prepara os campos personalizados
        custom_fields = []
        
        # Nome do cliente (usado no título da task)
        task_name = f"Lead: {client_data.get('nome', 'Cliente')} - {client_data.get('servico', 'Serviço')}"
        
        # Descrição da task
        description = f"""
**Novo Lead via WhatsApp Bot**

**Cliente:** {client_data.get('nome', 'N/A')}
**E-mail:** {client_data.get('email', 'N/A')}
**WhatsApp:** {client_data.get('whatsapp', 'N/A')}
**Serviço:** {client_data.get('servico', 'N/A')}
**Protocolo:** {client_data.get('protocolo', 'N/A')}

**Agendamento:**
- Data: {client_data.get('agendamento', {}).get('data', 'N/A')}
- Horário: {client_data.get('agendamento', {}).get('horario', 'N/A')}
- Link Meet: {client_data.get('agendamento', {}).get('link_meet', 'N/A')}

**Data de Criação:** {datetime.now().strftime('%d/%m/%Y %H:%M')}
        """.strip()
        
        # Adiciona campos personalizados
        if client_data.get('email'):
            custom_fields.append({
                "id": self.custom_fields["email"],
                "value": client_data['email']
            })
        
        if client_data.get('whatsapp'):
            custom_fields.append({
                "id": self.custom_fields["phone"],
                "value": client_data['whatsapp']
            })
        
        if client_data.get('servico') and client_data['servico'] in self.service_mapping:
            custom_fields.append({
                "id": self.custom_fields["service_type"],
                "value": self.service_mapping[client_data['servico']]
            })
        
        if client_data.get('protocolo'):
            custom_fields.append({
                "id": self.custom_fields["protocol"],
                "value": client_data['protocolo']
            })
        
        if client_data.get('agendamento', {}).get('data'):
            custom_fields.append({
                "id": self.custom_fields["meeting_date"],
                "value": client_data['agendamento']['data']
            })
        
        if client_data.get('agendamento', {}).get('link_meet'):
            custom_fields.append({
                "id": self.custom_fields["meeting_link"],
                "value": client_data['agendamento']['link_meet']
            })
        
        # Define o status inicial como "Novo Lead"
        custom_fields.append({
            "id": self.custom_fields["opportunity_stage"],
            "value": self.stage_mapping["novo_lead"]
        })
        
        # Define o tipo de oportunidade como "Service Inquiry"
        custom_fields.append({
            "id": self.custom_fields["opportunity_type"],
            "value": 0  # Service Inquiry
        })
        
        # Marca e-mail como não enviado
        custom_fields.append({
            "id": self.custom_fields["email_sent"],
            "value": False
        })
        
        # Dados da task
        task_data = {
            "name": task_name,
            "description": description,
            "status": "new",  # Status padrão da lista
            "custom_fields": custom_fields
        }
        
        # Cria a task
        endpoint = f"/list/{self.list_id}/task"
        result = self._make_request("POST", endpoint, task_data)
        
        if "error" not in result:
            print(f"✅ Task criada no ClickUp com sucesso! ID: {result.get('id')}")
            return {
                "success": True,
                "task_id": result.get('id'),
                "task_url": result.get('url'),
                "message": "Lead criado com sucesso no CRM"
            }
        else:
            print(f"❌ Erro ao criar task no ClickUp: {result['error']}")
            return {
                "success": False,
                "error": result['error'],
                "message": "Erro ao criar lead no CRM"
            }

    def update_task_stage(self, task_id: str, stage: str) -> Dict:
        """
        Atualiza o estágio (Opportunity Stage) de uma task
        
        Args:
            task_id: ID da task no ClickUp
            stage: Estágio desejado (ex: "coletando_dados", "agendado", etc.)
        """
        
        if stage not in self.stage_mapping:
            return {
                "success": False,
                "error": f"Estágio inválido: {stage}",
                "message": "Estágio não reconhecido"
            }
        
        stage_value = self.stage_mapping[stage]
        
        custom_fields = [{
            "id": self.custom_fields["opportunity_stage"],
            "value": stage_value
        }]
        
        task_data = {
            "custom_fields": custom_fields
        }
        
        endpoint = f"/task/{task_id}"
        result = self._make_request("PUT", endpoint, task_data)
        
        if "error" not in result:
            print(f"✅ Estágio da task {task_id} atualizado para: {stage}")
            return {
                "success": True,
                "task_id": task_id,
                "stage": stage,
                "message": f"Estágio atualizado para {stage}"
            }
        else:
            print(f"❌ Erro ao atualizar estágio da task {task_id}: {result['error']}")
            return {
                "success": False,
                "error": result['error'],
                "message": "Erro ao atualizar estágio"
            }

    def update_task_agreement(self, task_id: str, agreement_data: Dict) -> Dict:
        """
        Atualiza os dados de agendamento de uma task
        
        Args:
            task_id: ID da task no ClickUp
            agreement_data: Dados do agendamento
                {
                    "data": "2024-01-15",
                    "horario": "14:00",
                    "link_meet": "https://meet.google.com/xyz123",
                    "protocolo": "123456"
                }
        """
        
        custom_fields = []
        
        if agreement_data.get('data'):
            custom_fields.append({
                "id": self.custom_fields["meeting_date"],
                "value": agreement_data['data']
            })
        
        if agreement_data.get('link_meet'):
            custom_fields.append({
                "id": self.custom_fields["meeting_link"],
                "value": agreement_data['link_meet']
            })
        
        if agreement_data.get('protocolo'):
            custom_fields.append({
                "id": self.custom_fields["protocol"],
                "value": agreement_data['protocolo']
            })
        
        if not custom_fields:
            return {
                "success": False,
                "error": "Nenhum dado de agendamento fornecido",
                "message": "Dados insuficientes para atualização"
            }
        
        task_data = {
            "custom_fields": custom_fields
        }
        
        endpoint = f"/task/{task_id}"
        result = self._make_request("PUT", endpoint, task_data)
        
        if "error" not in result:
            print(f"✅ Dados de agendamento da task {task_id} atualizados")
            return {
                "success": True,
                "task_id": task_id,
                "message": "Dados de agendamento atualizados"
            }
        else:
            print(f"❌ Erro ao atualizar agendamento da task {task_id}: {result['error']}")
            return {
                "success": False,
                "error": result['error'],
                "message": "Erro ao atualizar agendamento"
            }

    def mark_email_sent(self, task_id: str) -> Dict:
        """
        Marca que o e-mail de confirmação foi enviado
        """
        
        custom_fields = [{
            "id": self.custom_fields["email_sent"],
            "value": True
        }]
        
        task_data = {
            "custom_fields": custom_fields
        }
        
        endpoint = f"/task/{task_id}"
        result = self._make_request("PUT", endpoint, task_data)
        
        if "error" not in result:
            print(f"✅ E-mail marcado como enviado para task {task_id}")
            return {
                "success": True,
                "task_id": task_id,
                "message": "E-mail marcado como enviado"
            }
        else:
            print(f"❌ Erro ao marcar e-mail como enviado: {result['error']}")
            return {
                "success": False,
                "error": result['error'],
                "message": "Erro ao marcar e-mail como enviado"
            }

    def get_task_by_protocol(self, protocol: str) -> Optional[Dict]:
        """
        Busca uma task pelo protocolo
        
        Args:
            protocol: Código do protocolo (6 dígitos)
        """
        
        # Busca todas as tasks da lista
        endpoint = f"/list/{self.list_id}/task"
        result = self._make_request("GET", endpoint)
        
        if "error" in result:
            print(f"❌ Erro ao buscar tasks: {result['error']}")
            return None
        
        # Procura pela task com o protocolo específico
        for task in result.get('tasks', []):
            for field in task.get('custom_fields', []):
                if field.get('id') == self.custom_fields["protocol"] and field.get('value') == protocol:
                    return task
        
        return None

    def get_tasks_by_stage(self, stage: str) -> List[Dict]:
        """
        Busca todas as tasks de um determinado estágio
        
        Args:
            stage: Estágio desejado (ex: "novo_lead", "agendado", etc.)
        """
        
        if stage not in self.stage_mapping:
            print(f"❌ Estágio inválido: {stage}")
            return []
        
        stage_value = self.stage_mapping[stage]
        
        # Busca todas as tasks da lista
        endpoint = f"/list/{self.list_id}/task"
        result = self._make_request("GET", endpoint)
        
        if "error" in result:
            print(f"❌ Erro ao buscar tasks: {result['error']}")
            return []
        
        # Filtra as tasks pelo estágio
        filtered_tasks = []
        for task in result.get('tasks', []):
            for field in task.get('custom_fields', []):
                if field.get('id') == self.custom_fields["opportunity_stage"] and field.get('value') == stage_value:
                    filtered_tasks.append(task)
                    break
        
        return filtered_tasks

    def get_all_tasks(self) -> List[Dict]:
        """
        Busca todas as tasks da lista
        """
        
        endpoint = f"/list/{self.list_id}/task"
        result = self._make_request("GET", endpoint)
        
        if "error" in result:
            print(f"❌ Erro ao buscar tasks: {result['error']}")
            return []
        
        return result.get('tasks', [])

    def delete_task(self, task_id: str) -> Dict:
        """
        Deleta uma task (use com cuidado!)
        """
        
        endpoint = f"/task/{task_id}"
        result = self._make_request("DELETE", endpoint)
        
        if "error" not in result:
            print(f"✅ Task {task_id} deletada com sucesso")
            return {
                "success": True,
                "task_id": task_id,
                "message": "Task deletada com sucesso"
            }
        else:
            print(f"❌ Erro ao deletar task {task_id}: {result['error']}")
            return {
                "success": False,
                "error": result['error'],
                "message": "Erro ao deletar task"
            }

# Instância global do serviço
clickup_service = ClickUpService()

# Funções de conveniência para uso direto
def create_lead(client_data: Dict[str, Any]) -> Dict:
    """Cria um novo lead no ClickUp"""
    return clickup_service.create_lead_task(client_data)

def update_stage(task_id: str, stage: str) -> Dict:
    """Atualiza o estágio de uma task"""
    return clickup_service.update_task_stage(task_id, stage)

def update_agreement(task_id: str, agreement_data: Dict) -> Dict:
    """Atualiza os dados de agendamento"""
    return clickup_service.update_task_agreement(task_id, agreement_data)

def mark_email_sent(task_id: str) -> Dict:
    """Marca e-mail como enviado"""
    return clickup_service.mark_email_sent(task_id)

def find_task_by_protocol(protocol: str) -> Optional[Dict]:
    """Busca task pelo protocolo"""
    return clickup_service.get_task_by_protocol(protocol)

def get_tasks_by_stage(stage: str) -> List[Dict]:
    """Busca tasks por estágio"""
    return clickup_service.get_tasks_by_stage(stage)

def get_all_tasks() -> List[Dict]:
    """Busca todas as tasks"""
    return clickup_service.get_all_tasks()
