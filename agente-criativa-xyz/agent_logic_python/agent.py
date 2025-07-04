conversation_state = {}

def handle_message(user_id: str, message: str):
    """Handles incoming messages and manages conversation state."""
    # Get or initialize the user's state
    state = conversation_state.get(user_id, {"state": "START", "data": {}})
    
    print(f"Processing message from {user_id} in state {state['state']}: {message}")
    
    # --- State Machine Logic (Basic Example) ---
    if state['state'] == "START":
        if "orçamento" in message.lower():
            state['state'] = "AWAITING_NAME"
            response = "Olá! Para começar seu orçamento, qual é o seu nome?"
        else:
            response = "Olá! Sou seu agente virtual. Como posso ajudar hoje?"
            
    elif state['state'] == "AWAITING_NAME":
        state['data']['name'] = message
        state['state'] = "AWAITING_EMAIL"
        response = f"Obrigado, {message}. E qual o seu melhor e-mail para contato?"
        
    elif state['state'] == "AWAITING_EMAIL":
        state['data']['email'] = message
        state['state'] = "PROCESSING_REQUEST"
        # In a real scenario, you would call a service here (e.g., create ClickUp task)
        # For now, just acknowledge and reset state
        print(f"Received contact info: {state['data']}")
        response = "Recebi seus dados! Vou processar sua solicitação e em breve entraremos em contato."
        state = {"state": "START", "data": {}} # Reset state
        
    # --- End of State Machine Logic ---
        
    # Update the conversation state
    conversation_state[user_id] = state
    
    # Return the response(s) in the expected format
    return {"replies": [response]}
