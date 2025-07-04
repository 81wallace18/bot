Claro, aqui está toda a documentação da arquitetura formatada como um único bloco de código Markdown, pronta para ser copiada e colada em um arquivo `README.md`.

````markdown
# **Arquitetura do Projeto: Agente Virtual com Node.js e Python**

Esta arquitetura define a estrutura de um agente virtual que utiliza Node.js para a comunicação com o WhatsApp e Python para toda a lógica de negócio, seguindo um modelo de microsserviços.

## **Visão Geral: Microsserviços via API REST**

A solução é dividida em dois serviços independentes que se comunicam através de uma API REST local.

  - ### 🐍 **Serviço 1: Agent Logic (Python)**

      - **Responsabilidade**: Servir como o "cérebro" do agente. Ele contém toda a inteligência e lógica do negócio, gerencia o estado da conversa, processa as solicitações, conecta-se a serviços externos (**ClickUp**, Google Calendar) e formula as respostas.
      - **Tecnologias Principais**: `FastAPI` (para a API), `requests` (para a API do ClickUp), `google-api-python-client` (para Google Calendar), `uvicorn` (servidor web).

  - ### 🟩 **Serviço 2: WhatsApp Handler (Node.js)**

      - **Responsabilidade**: Atuar como a "ponte" de comunicação com o WhatsApp. Sua única função é receber mensagens do usuário, encaminhá-las para o serviço Python, aguardar a resposta e enviá-la de volta ao usuário no WhatsApp.
      - **Tecnologias Principais**: `whatsapp-web.js`, `axios` (para as chamadas HTTP).

-----

## **Fluxo de Comunicação**

O fluxo de uma única interação do usuário ocorre da seguinte forma:

1.  O **Usuário** envia uma mensagem (ex: "Quero um orçamento") via WhatsApp.
2.  O serviço **Node.js** (`whatsapp-web.js`) captura essa mensagem.
3.  O Node.js extrai o texto (`message.body`) e o ID do usuário (`message.from`).
4.  Ele faz uma requisição `POST` para o serviço **Python** no endpoint `http://localhost:8000/process-message`, enviando um JSON:
    ```json
    {
      "user_id": "5511999998888@c.us",
      "message": "Quero um orçamento"
    }
    ```
5.  O serviço **Python** (`FastAPI`) recebe a requisição e aciona a lógica do agente, que verifica o estado da conversa para aquele `user_id`.
6.  O agente executa as ações necessárias (consultar dados, **criar uma tarefa no ClickUp**, gerar horários, etc.).
7.  Após o processamento, o Python formula a(s) resposta(s) e retorna um JSON para o serviço Node.js:
    ```json
    {
      "replies": [
        "Agendamento confirmado para 10/07 às 15h.",
        "O link para a reunião é: [https://meet.google.com/xyz123](https://meet.google.com/xyz123)",
        "Sua solicitação foi registrada no protocolo: 482910"
      ]
    }
    ```
8.  O serviço **Node.js** recebe essa resposta.
9.  Ele itera sobre a lista de `replies` e envia cada mensagem, em ordem, de volta para o **Usuário** no WhatsApp usando `client.sendMessage()`.

-----

## **Estrutura de Pastas e Arquivos**

Recomenda-se uma estrutura de monorepo para facilitar o gerenciamento do projeto.

```bash
/agente-criativa-xyz/
|
├── 📂 agent_logic_python/
|   ├── main.py                # Ponto de entrada da API com FastAPI, define o endpoint /process-message
|   ├── agent.py               # Cérebro do agente, gerencia estados e a lógica da conversa
|   ├── services/
|   |   ├── clickup_service.py # Funções para interagir com a API do ClickUp (criar tarefa, logar agendamento)
|   |   └── calendar_service.py# Funções para verificar horários (simulado ou real via Google Calendar API)
|   ├── utils.py               # Funções utilitárias (ex: gerar protocolo aleatório)
|   ├── requirements.txt       # Dependências Python (fastapi, uvicorn, requests, etc.)
|   └── .env                   # Arquivo para guardar chaves de API, IDs do ClickUp (Listas, Espaços) e outras configurações
|
├── 📂 whatsapp_handler_node/
|   ├── index.js               # Lógica principal do Node.js, inicialização do cliente wwebjs e listeners
|   └── package.json           # Dependências Node.js (whatsapp-web.js, axios)
|
├── 📜 docker-compose.yml       # (Opcional, mas recomendado) Para iniciar ambos os serviços com um único comando
|
└── 📜 README.md                # Instruções de setup, execução e teste do projeto
````

-----

## **Detalhes da Implementação**

### **🐍 Python: `agent_logic_python`**

  - **`main.py`**: Define o servidor web com `FastAPI` e expõe um único endpoint `POST /process-message` que recebe o `user_id` e a `message`.
  - **`agent.py`**:
      - Mantém um dicionário global (ou uma conexão com Redis/banco de dados) para gerenciar o estado da conversa de cada usuário.
      - Exemplo de objeto de estado:
        ```python
        conversation_state = {
            "5511999998888@c.us": {
                "state": "AWAITING_EMAIL", # Estado atual da conversa
                "data": {                  # Dados já coletados
                    "name": "Carlos"
                }
            }
        }
        ```
      - Contém a função `handle_message(user_id, message)` com a máquina de estados (`if/elif/else` baseado no `state`) que direciona o fluxo da conversa.
  - **`services/`**: Módulos que abstraem a comunicação com APIs externas. Por exemplo, **`clickup_service.py`** terá uma função `create_lead_task(data)` que recebe os dados do lead e **cria uma nova tarefa no ClickUp via API**, tratando a autenticação.

### **🟩 Node.js: `whatsapp_handler_node`**

  - **`index.js`**:
      - Inicializa o cliente do `whatsapp-web.js`.
      - Gerencia o evento `qr` para permitir o login via QR Code no terminal.
      - O listener `client.on('message', async (message) => { ... })` é o núcleo do serviço.
      - Dentro do listener, ele executa uma chamada com `axios` para o serviço Python, sempre dentro de um bloco `try...catch` para lidar com falhas de comunicação (ex: o serviço Python está offline).
      - Ao receber a resposta, envia as mensagens para o usuário de forma assíncrona.

<!-- end list -->

