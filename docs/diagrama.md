```mermaid
flowchart TD
    subgraph WhatsApp
        A[Chat wpp]
        A --> B[Receber solicitação de atendimento]
        B --> B1[Mostrar opções de serviço]
        A --> C[Coletar dados]
        C --> C1[Nome Email telefone]
        A --> D[Retornar Protocolo]
        D --> D1[Mostrar opções de data]
    end
    
    A --> E[Agente IA]
    E --> F[Tools]
    F --> F1[MCP de datas]
    F --> F2[gerador de protocolo]
    E --> G[Enviar email de confirmação]
    E --> H[Consulta disponibilidade]
    E --> I[Adicionar cliente ao CRM]
    G --> J[Send Mail]
    H --> K[google Agenda]
    I --> L[clickup api]
    
    %% Relacionamentos principais
    A -.->|Fluxo de mensagens| E
    E -.->|Responde no WhatsApp| A
    
    classDef ext fill:#fff,stroke:#333,stroke-width:2px;
    class J,K,L ext;