from crewai_tools import BaseTool
from datetime import datetime, timedelta

class DateTool(BaseTool):
    name = "formatar_data"
    description = "Formata datas e converte expressões como 'amanhã às 15h' para o formato ISO."

    def _run(self, texto_data: str):
        # Placeholder: retorna a data/hora atual para demonstração
        return datetime.now().isoformat() 