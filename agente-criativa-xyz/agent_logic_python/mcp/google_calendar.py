from crewai.tools import MCPServerAdapter

google_calendar_server_params = {
    "url": "http://localhost:8001/mcp",
    "transport": "streamable-http"
}

def get_google_calendar_tools():
    return MCPServerAdapter(google_calendar_server_params) 