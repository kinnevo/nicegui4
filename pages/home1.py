from nicegui import ui, app

@ui.page('/home1')
def home1():
    with ui.column().classes('w-full items-center'):
        ui.label('Prepara tu exploración al Silicon Valley').classes('text-h3 q-mb-md')
        ui.label('Explora en forma colaborativa tu experiencia de planear una visita al Silicon Valley').classes('text-h5 q-mb-md')
        
        with ui.row().classes('w-full items-center'):

            # Left column with text
            with ui.column().classes('w-2/5'):  # Takes up 50% of the width
                ui.label('Conversa con Lucy, nuestra guía y mentora que te ayudará a descubrir como hacer mas valiosa y productiva tu próxima visita al Silicon Valley').classes('text-body1 q-mb-md text-left')            
                ui.label('Durante una conversación de descubrimiento generas ideas y material, al igual que otros participantes, que como tu quieren vivir la experiencia de un viaje a la innovación.').classes('text-body1 q-mb-md text-left')            
                ui.label('Al final de tu conversación, que puede ser una o varias conversaciones. Te compartiremos el resumen de cada conversación y un reporte de los puntos de interés y experiencias que los otros participantes que podrían ser tus compañeros de viaje quieren experimentar.').classes('text-body1 q-mb-md text-left')    
                ui.label('Este resumen, en colaboración con nuestro equipo de expertos es un material de referencia para construir tu agenda y abrir la mente que hará a tu viaje ser un viaje de aprendizaje y exploración.').classes('text-body1 q-mb-md text-left')            

            # Right column with image
            with ui.column().classes('w-2/5'):  # Takes up 50% of the width
                ui.image('static/visit_sv_cover.jpeg').classes('w-full rounded-lg shadow-lg')

        
        ui.label('Inicia tu experiencia ahora mismos y crear tu futuro innovando.').classes('text-h6 q-mb-md')

        with ui.row().classes('w-full items-center'):
            ui.button('Admin').classes('text-h5 q-mb-md').on_click(lambda: ui.navigate.to('/admin'))
            ui.button('Vamonos  ...').classes('text-h5 q-mb-md').on_click(lambda: ui.navigate.to('/page1'))
            ui.button('Planear  ...').classes('text-h5 q-mb-md').on_click(lambda: ui.navigate.to('/chat'))


