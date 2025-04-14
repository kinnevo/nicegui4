from nicegui import ui, app
import requests
import json
from datetime import datetime
import os
from typing import List, Optional
import uuid
from dotenv import load_dotenv
from utilities.database import user_db
from utilities.utils import find_user_from_pool, update_user_status

#example of linkk
#        ui.link('Share Your Dreams', '/chat').props('flat color=primary')


# Load environment variables
load_dotenv()

# LangFlow connection settings
BASE_API_URL = os.environ.get("BASE_API_URL")
FLOW_ID = os.environ.get("FLOW_ID")
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
ENDPOINT = os.environ.get("ENDPOINT")

def run_flow(message: str, history: Optional[List[dict]] = None) -> dict:
    """Run the LangFlow with the given message and conversation history."""
    api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT}"
    
    # Get the current session ID and username from storage
    session_id = app.storage.browser.get('session_id', str(uuid.uuid4()))
    username = app.storage.browser.get('username', 'User')
    
    if history and len(history) > 0:
        formatted_history = json.dumps(history, 
                                     ensure_ascii=False)
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
            "conversation_history": formatted_history,
            "user": username,
            "session_id": session_id
        }
    else:
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
            "user": username,
            "session_id": session_id
        }

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()
        return response_data
    except Exception as e:
        raise e



"""Add a message to the conversation history."""
def add_to_history(role: str, content: str, agent: str = "Unknown User", session_id: str = ""):
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent
    } 
    app.storage.browser['conversation_history'].append(message)

def display_conversation(conversation_history_txt, chat_display):
    # Build the complete content
    content = ""
    for message in conversation_history_txt:
        content += f'**{message["role"]}:** {message["content"]}\n\n'
    # Set the content once
    chat_display.content = content


def send_message(chat_display, message_input, session_id):
    if not message_input.value:
        return
    
    # Add user message and update display
    add_to_history(role='user', content=message_input.value, agent=app.storage.browser.get("username", "Unknown User"), session_id=session_id)
    display_conversation(app.storage.browser['conversation_history'], chat_display)
    
    # Get and add assistant response
    response = run_flow(message_input.value)
    add_to_history(role='assistant', content=response["outputs"][0]["outputs"][0]["results"]["message"]["text"], agent=app.storage.browser.get("username", "Unknown User"), session_id=session_id)
    display_conversation(app.storage.browser['conversation_history'], chat_display)
    
    # Clear input
    message_input.value = ''
    
    # Save conversation to database
    save_db()

    #print(app.storage.browser['conversation_history'])
    #print(f"Assistant: {app.storage.browser['conversation_history']}")



@ui.page('/chat')
def chat_page():
    session_id = str(uuid.uuid4())
    app.storage.browser['session_id'] = session_id
    app.storage.browser['conversation_history'] = []

    username = find_user_from_pool()
    app.storage.browser['username'] = username

    if username == -1:    
        with ui.dialog() as error_dialog:
            with ui.card():
                ui.label(f'No users available at this time, try again later').classes('text-h6 q-mb-md')
                with ui.row().classes('w-full justify-end gap-2'):
                    ui.button('Go Back', on_click=lambda: ui.navigate.to('/')).classes('bg-gray-500 text-white')
        error_dialog.open()


    # Main content
    with ui.column().classes('w-full max-w-5xl mx-auto p-4'):
        ui.label('Interactive Visit Planning Chat').classes('text-h4 q-mb-md')
        
        # Header with user info
        with ui.row().classes('w-full bg-gray-100 p-4 rounded-lg'):
            ui.label(f'User: {app.storage.browser.get("username")}').classes('text-lg')
            ui.label(f'Session: {app.storage.browser["session_id"]}').classes('text-lg')
        
        # Chat display
        chat_display = ui.markdown('').classes('w-full h-64 border rounded-lg p-4 overflow-auto')
        
        # Message input
        message_input = ui.textarea('Type your message here...').classes('w-full h-64')
        

        # Send button
        ui.button('Send', on_click=lambda: send_message(chat_display, message_input, session_id)).classes('w-full')
        
        with ui.row().classes('w-full max-w-5xl mx-auto p-2 justify-center gap-4'):
            ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
            ui.button('Logout', on_click=logout_session).classes('bg-blue-500 text-white')
            #ui.button('Download a Files', on_click=download_file).classes('bg-blue-500 text-white')
            #ui.button('Save DB', on_click=save_db).classes('bg-blue-500 text-white')

def logout_session():
    def confirm_logout():
        update_user_status(app.storage.browser['username'], False)
        
        # Navigate to home page
        ui.navigate.to('/')
        dialog.close()

    with ui.dialog() as dialog:
        with ui.card():
            ui.label('Are you sure you want to logout?').classes('text-h6 q-mb-md')
            with ui.row().classes('w-full justify-end gap-2'):
                ui.button('Yes', on_click=confirm_logout).classes('bg-red-500 text-white')
                ui.button('No', on_click=dialog.close).classes('bg-gray-500 text-white')
    dialog.open()


def download_file():
    import json
    from datetime import datetime
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{app.storage.browser.get('username', 'user')}_{timestamp}.json"
    
    # Convert conversation history to JSON string with double quotes
    content = json.dumps(app.storage.browser['conversation_history'], 
                        ensure_ascii=False, 
                        indent=2)
    
    # Create download link
    ui.download(content.encode('utf-8'), filename)

def save_db():
    session_id = app.storage.browser['session_id']
    username = app.storage.browser.get('username', 'Unknown User')
    # Convert to JSON string with double quotes
    conversation = json.dumps(app.storage.browser['conversation_history'], 
                            ensure_ascii=False, 
                            indent=2)
    
    # Check if conversation exists
    existing_conversation = user_db.get_conversation(session_id)
    
    if existing_conversation:
        # Update existing conversation
        success = user_db.update_conversation(session_id, conversation)
        ui.notify('Conversation updated' if success else 'Update failed')
    else:
        # Create new conversation
        success = user_db.create_conversation(session_id, username, conversation)
        ui.notify('Conversation saved' if success else 'Save failed')
