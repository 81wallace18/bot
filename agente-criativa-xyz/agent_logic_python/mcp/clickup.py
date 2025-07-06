from crewai.tools import MCPServerAdapter

clickup_server_params = {
    "url": "http://localhost:8002/mcp",
    "transport": "streamable-http"
}

def get_clickup_tools():
    return MCPServerAdapter(clickup_server_params) 