# **Guia de Configuração: Autenticação de APIs e Deploy com Proxy Reverso**

Este guia detalha o processo para autenticar seu agente virtual com as APIs do **Google Calendar** e **ClickUp**, e como expor seu serviço local à internet de forma segura usando um túnel SSH e Nginx como proxy reverso em uma VPS.

---

## **Parte 1: Autenticação com as APIs**

### **A. Autenticação com a API do Google Calendar (OAuth 2.0)**

Para que o Google aceite requisições do seu aplicativo, especialmente vindo de um domínio público, você precisa registrar seu app e obter credenciais do tipo "Aplicativo da Web".

#### **Passo 1-3: Configuração Inicial no Google Cloud**

Siga os passos detalhados anteriormente para:
1.  **Criar um Projeto** no [Google Cloud Platform](https://console.cloud.google.com/).
2.  **Ativar a "Google Calendar API"** na Biblioteca de APIs.
3.  **Configurar a "Tela de consentimento OAuth"**, selecionando "Externo", preenchendo os dados do app e adicionando seu próprio e-mail como **Usuário de Teste**.

#### **Passo 4 (Atualizado): Criar Credenciais OAuth 2.0 para um App Web**

1.  No painel do Google Cloud, navegue até **"APIs e serviços" > "Credenciais"**.
2.  Clique em **"+ CRIAR CREDENCIAIS"** e selecione **"ID do cliente OAuth"**.
3.  No campo "Tipo de aplicativo", selecione **"Aplicativo da Web"**.
4.  Dê um nome para a credencial (ex: "Agente Virtual - Produção").
5.  Em **"URIs de redirecionamento autorizados"**, clique em **"+ ADICIONAR URI"**. Adicione o URI que receberá o callback de autorização do Google. Este URI deve apontar para o seu domínio público.
    -   Exemplo: `https://agendador.ecossystem.solutions/oauth2callback`
6.  Clique em **"CRIAR"**.
7.  Uma janela aparecerá. Clique no botão **"FAZER O DOWNLOAD DO JSON"**.
8.  Renomeie o arquivo baixado para `credentials.json` e coloque-o na pasta raiz do seu serviço Python (`agent_logic_python/`).

> **AVISO DE SEGURANÇA:** Adicione `credentials.json` e `token.json` (que será gerado depois) ao seu arquivo `.gitignore` para nunca enviá-los a um repositório.

---

### **B. Autenticação com a API do ClickUp (Token Pessoal)**

A autenticação com o ClickUp é mais direta e baseada em um token pessoal.

#### **1. Obter o Token da API**

1.  Faça login na sua conta do ClickUp.
2.  Clique no seu avatar no canto inferior esquerdo e vá para **"Apps"**.
3.  Na seção **"API Token"**, gere e copie seu token pessoal.

#### **2. Armazenar o Token de Forma Segura**

Crie e configure um arquivo `.env` na pasta `agent_logic_python/` para armazenar suas chaves secretas.

```env
# agent_logic_python/.env

CLICKUP_API_TOKEN="pk_xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
CLICKUP_LIST_ID="12345678" # ID da lista do ClickUp onde as tarefas serão criadas
```

#### **3. Usar o Token no Código**

Instale a biblioteca `python-dotenv` (`pip install python-dotenv`) para carregar essas variáveis no seu serviço.

**Exemplo para `clickup_service.py`:**

```python
# agent_logic_python/services/clickup_service.py
import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")
CLICKUP_API_URL = "[https://api.clickup.com/api/v2](https://api.clickup.com/api/v2)"

def create_lead_task(task_name, description):
    """Cria uma nova tarefa no ClickUp."""
    if not CLICKUP_API_TOKEN or not CLICKUP_LIST_ID:
        print("Erro: Credenciais do ClickUp não configuradas no arquivo .env")
        return None

    url = f"{CLICKUP_API_URL}/list/{CLICKUP_LIST_ID}/task"
    headers = {
        "Authorization": CLICKUP_API_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "name": task_name,
        "description": description,
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()  # Lança erro para status HTTP 4xx/5xx
        print("Tarefa criada no ClickUp com sucesso!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao criar tarefa no ClickUp: {e}")
        return None
```

---

## **Parte 2: Túnel SSH e Configuração do Nginx na VPS**

Esta configuração permite que seu serviço, rodando localmente, seja acessado de forma segura através do seu domínio.

#### **Passo 1: Criar o Túnel SSH Reverso (no seu PC Local)**

Execute este comando no terminal do seu computador para expor a porta local `8000` na porta `8080` da sua VPS.

```bash
# Sintaxe: ssh -R <porta_remota_vps>:localhost:<porta_local> <usuario>@<ip_da_vps>
ssh -R 8080:localhost:8000 seu_usuario@ip_da_sua_vps
```
*Mantenha este terminal aberto enquanto o serviço estiver em uso.*

#### **Passo 2: Configurar o Nginx como Proxy Reverso (na sua VPS)**

1.  **Crie o arquivo de configuração do Nginx:**
    ```bash
    sudo nano /etc/nginx/sites-available/agendador.ecossystem.solutions
    ```

2.  **Cole o conteúdo abaixo.** Ele redireciona HTTP para HTTPS e envia o tráfego para o túnel SSH.

    ```nginx
    server {
        listen 80;
        server_name agendador.ecossystem.solutions;

        # Redireciona permanentemente para a versão HTTPS
        location / {
            return 301 https://$host$request_uri;
        }
    }

    server {
        listen 443 ssl;
        server_name agendador.ecossystem.solutions;

        # Caminhos dos certificados SSL (serão gerados pelo Certbot)
        ssl_certificate /etc/letsencrypt/live/agendador.ecossystem.solutions/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/agendador.ecossystem.solutions/privkey.pem;
        include /etc/letsencrypt/options-ssl-nginx.conf;
        ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

        location / {
            # Envia a requisição para a porta onde o túnel SSH está escutando
            proxy_pass http://localhost:8080; 
            
            # Cabeçalhos essenciais para o proxy reverso
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }
    ```

3.  **Ative a configuração e verifique a sintaxe:**
    ```bash
    sudo ln -s /etc/nginx/sites-available/agendador.ecossystem.solutions /etc/nginx/sites-enabled/
    sudo nginx -t
    ```

#### **Passo 3: Obter Certificado SSL com Certbot (Let's Encrypt)**

1.  **Instale o Certbot e o plugin para Nginx:**
    ```bash
    sudo apt update
    sudo apt install certbot python3-certbot-nginx
    ```

2.  **Execute o Certbot para obter e instalar o certificado:**
    ```bash
    sudo certbot --nginx -d agendador.ecossystem.solutions
    ```
    Siga as instruções na tela. O Certbot ajustará sua configuração do Nginx automaticamente.

3.  **Reinicie o Nginx para aplicar todas as mudanças:**
    ```bash
    sudo systemctl restart nginx
    ```

Com tudo configurado, qualquer requisição para `https://agendador.ecossystem.solutions` será seguramente redirecionada pela sua VPS até o serviço Python rodando no seu computador.