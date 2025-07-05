import random
from crewai_tools import BaseTool

class ProtocolTool(BaseTool):
    name = "gerar_protocolo"
    description = "Gera um protocolo aleatório de 6 dígitos para confirmação de atendimento."

    def _run(self, *args, **kwargs):
        return str(random.randint(100000, 999999)) 