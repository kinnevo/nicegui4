import uuid
import datetime
import random
from datetime import datetime, timedelta
from nicegui import app, ui
# Initialize list of 25 sample users with conversation histories
def initialize_users():
    users = {}
    
    for _ in range(25):    
        username = f"user_{str(uuid.uuid4())}"
        
        # Create user entry
        users[username] = {
            "username": username,
            "time_logged": None,
            "logged": False
        }
    
    return users

# get a user from the pool
def find_user_from_pool():
    for username, user_data in app.storage.general['user_list'].items():
        if not user_data.get('logged', False):
            user_data['logged'] = True
            user_data['time_logged'] = datetime.now().isoformat()

            # Update global storage
            app.storage.general['user_list'][username] = user_data
            return username
    return None

# update the status of a user
def update_user_status(username, status):
    app.storage.general['user_list'][username]['logged'] = status
    if status == True:
        app.storage.general['user_list'][username]['time_logged'] = datetime.now().isoformat()
    else:
        app.storage.general['user_list'][username]['time_logged'] = None
