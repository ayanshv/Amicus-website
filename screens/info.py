from nicegui import ui, app, run

from components.background import image_bg
from components.navbar import navbar
from components.footer import footer



@ui.page('/info')
def info():
    image_bg()
    navbar()

    with ui.column().classes('max-w-4xl mx-auto mt-40 w-full px-4'):
        ui.button('← Back to Home', on_click=lambda: ui.navigate.to('/')).props('flat').classes('amicus-back mb-4 self-start px-5 py-2 rounded-full text-white font-medium transition-all duration-300').style('background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);')

        ui.label('Use cases').classes('eyebrow text-white')
        ui.label('Not sure where to start?').classes('text-4xl font-bold text-white mt-2').style("font-family: 'Fraunces', serif;")
        ui.label('Upload or snap a photo of any of these to see plain-language guidance.').classes('text-lg text-white/70 mb-8')

        with ui.row().classes('w-full grid grid-cols-1 md:grid-cols-3 gap-6'):
            with ui.card().classes('feature-card rounded-2xl p-6'):
                ui.html('<div class="feature-icon"><i class="fa-solid fa-house"></i></div>', sanitize=False)
                ui.label('Lease agreements').classes('text-xl font-bold mb-2 font-serif text-white')
                ui.label('Understand your renting rights, deposit terms, and hidden fees.').classes('text-white/70')

            with ui.card().classes('feature-card rounded-2xl p-6'):
                ui.html('<div class="feature-icon"><i class="fa-solid fa-briefcase"></i></div>', sanitize=False)
                ui.label('Employment contracts').classes('text-xl font-bold mb-2 font-serif text-white')
                ui.label('Decode non-competes, termination clauses, and benefits.').classes('text-white/70')

            with ui.card().classes('feature-card rounded-2xl p-6'):
                ui.html('<div class="feature-icon"><i class="fa-solid fa-plane-departure"></i></div>', sanitize=False)
                ui.label('Immigration forms').classes('text-xl font-bold mb-2 font-serif text-white')
                ui.label('Clarify confusing government jargon and your next steps.').classes('text-white/70')

        ui.label('FAQ').classes('eyebrow mt-16')
        ui.label('Frequently asked questions').classes('text-4xl font-serif font-bold text-white mt-2').style("font-family: 'Fraunces', serif;")

        with ui.expansion('How accurate is the AI analysis?', icon='help_outline').classes('w-full amicus-glass mb-4 text-lg'):
            ui.label("Our AI is trained on vast amounts of legal data to provide accurate summaries. However, it is an informational companion, not a replacement for a certified lawyer.").classes('p-4 text-white/70')

        with ui.expansion('Do you save my legal documents?', icon='lock').classes('w-full amicus-glass mb-4 text-lg'):
            ui.label("No. Your privacy is our top priority. Documents are analyzed in real time and immediately deleted from our servers once the analysis is complete.").classes('p-4 text-white/70')

        with ui.expansion('What languages are supported?', icon='language').classes('w-full amicus-glass mb-4 text-lg'):
            ui.label("We currently support over 65 languages. Just select your preferred language from the dropdown in the Analyze tool.").classes('p-4 text-white/70')

    footer()