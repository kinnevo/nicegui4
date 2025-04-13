from nicegui import ui, app
from utilities.utils import initialize_users, update_user_status

@ui.page('/admin')
def admin_page():
    with ui.column().classes('w-full items-center'):
        ui.label('Welcome to SV Exploration Admin Page!').classes('text-h4 q-mb-md')

        with ui.column().classes('w-full items-center'):
            ui.label('List of Users').classes('text-h5 q-my-md text-center')

        # Create table reference
        table = None

        def refresh_table():
            nonlocal table
            if table:
                table.rows = list(app.storage.general.get('user_list', {}).values())
                table.update()

        def rebuild_users():
            app.storage.general['user_list'] = initialize_users()
            ui.notify('User list has been rebuilt')
            refresh_table()
            ui.run_javascript('window.dispatchEvent(new Event("admin-page-update"))')

        def reset_users():
            for user in app.storage.general['user_list'].values():
                user['logged'] = False
                user['time_logged'] = None
            ui.notify('All users have been reset')
            refresh_table()
            ui.run_javascript('window.dispatchEvent(new Event("admin-page-update"))')

        with ui.row().classes('w-full justify-center gap-4 q-mb-md'):
            ui.button('Rebuild User List', on_click=rebuild_users).classes('bg-green-500 text-white')
            ui.button('Reset All Users', on_click=reset_users).classes('bg-red-500 text-white')

        with ui.card().classes('w-full max-w-3xl mx-auto shadow-lg'):
            columns = [
                {'name': 'username', 'label': 'User Name', 'field': 'username'},
                {'name': 'time_logged', 'label': 'Date & Time', 'field': 'time_logged'},
                {'name': 'logged', 'label': 'Logged', 'field': 'logged'}
            ]
            
            # Store table reference
            table = ui.table(
                columns=columns,
                rows=list(app.storage.general.get('user_list', {}).values()),
            )

        # # Add event listener for updates from other pages
        # ui.add_body_html('''
        #     <script>
        #     window.addEventListener('admin-page-update', function() {
        #         window.location.reload();
        #     });
        #     </script>
        # ''')

        ui.separator().classes('w-full q-my-md')
        ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')

def logout_session(username):
    # Trigger admin page refresh when button is clicked
    ui.run_javascript('window.dispatchEvent(new Event("admin-page-update"))')
    
    def confirm_logout():
        # Update user status in the pool
        update_user_status(username, False)
        # Trigger admin page refresh after status update
        ui.run_javascript('window.dispatchEvent(new Event("admin-page-update"))')
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
