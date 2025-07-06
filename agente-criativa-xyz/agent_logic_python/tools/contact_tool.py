import re
from crewai_tools import BaseTool
from typing import Dict, Optional

class ContactTool(BaseTool):
    name = "extrair_contato"
    description = "Extrai informações de contato (nome, email, telefone) de mensagens de texto."

    def _run(self, mensagem: str) -> Dict:
        """
        Extrai informações de contato de uma mensagem de texto.
        
        Args:
            mensagem: Texto da mensagem para análise
            
        Returns:
            Dict com informações extraídas
        """
        resultado = {
            "nome": None,
            "email": None,
            "telefone": None,
            "confianca": 0.0
        }
        
        # Padrões para extração
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+55\s?)?(\(?\d{2}\)?\s?)?(\d{4,5}-?\d{4})'
        
        # Extrair email
        email_match = re.search(email_pattern, mensagem)
        if email_match:
            resultado["email"] = email_match.group()
            resultado["confianca"] += 0.3
        
        # Extrair telefone
        phone_match = re.search(phone_pattern, mensagem)
        if phone_match:
            resultado["telefone"] = phone_match.group()
            resultado["confianca"] += 0.3
        
        # Tentar extrair nome (heurística simples)
        # Procura por palavras que começam com maiúscula e não são muito comuns
        palavras = mensagem.split()
        possiveis_nomes = []
        
        for palavra in palavras:
            # Remove pontuação
            palavra_limpa = re.sub(r'[^\w\s]', '', palavra)
            
            # Verifica se começa com maiúscula e tem pelo menos 2 letras
            if (palavra_limpa and 
                palavra_limpa[0].isupper() and 
                len(palavra_limpa) >= 2 and
                palavra_limpa.lower() not in ['eu', 'meu', 'minha', 'sou', 'estou', 'quero', 'preciso', 'gostaria']):
                possiveis_nomes.append(palavra_limpa)
        
        if possiveis_nomes:
            # Pega o primeiro nome encontrado
            resultado["nome"] = possiveis_nomes[0]
            resultado["confianca"] += 0.2
        
        # Se encontrou pelo menos uma informação, aumenta confiança
        if any([resultado["nome"], resultado["email"], resultado["telefone"]]):
            resultado["confianca"] = min(resultado["confianca"], 1.0)
        
        return resultado 