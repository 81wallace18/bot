import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Optional

class EmailService:
    """
    Serviço para envio de e-mails de confirmação
    Este serviço é mantido mesmo com MCPs pois é lógica de negócio específica
    """
    
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.email = os.getenv("EMAIL_USER", "")
        self.password = os.getenv("EMAIL_PASSWORD", "")
        
    def send_confirmation_email(self, client_data: Dict, protocol: str, meeting_link: str) -> Dict:
        """
        Envia e-mail de confirmação de agendamento
        """
        try:
            # Cria mensagem
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = client_data['email']
            msg['Subject'] = f"Confirmação de Agendamento - Protocolo {protocol}"
            
            # Corpo do e-mail
            body = f"""
            Olá {client_data['nome']},
            
            Seu agendamento foi confirmado com sucesso!
            
            📋 **Detalhes do Agendamento:**
            - Protocolo: {protocol}
            - Serviço: {client_data['servico']}
            - Data: {client_data['agendamento']['data']}
            - Horário: {client_data['agendamento']['horario']}
            - Link da Reunião: {meeting_link}
            
            📅 **Link para adicionar ao seu calendário:**
            {meeting_link}
            
            Aguardamos você!
            
            Equipe Agência Criativa XYZ
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Envia e-mail
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            
            return {
                "success": True,
                "message": f"E-mail enviado para {client_data['email']}",
                "protocol": protocol
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": "Erro ao enviar e-mail"
            }

# Instância global
email_service = EmailService()

def send_confirmation_email(client_data: Dict, protocol: str, meeting_link: str) -> Dict:
    """Função de conveniência"""
    return email_service.send_confirmation_email(client_data, protocol, meeting_link) 