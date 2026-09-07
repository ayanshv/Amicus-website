
from nicegui import ui, run, app

from components.background import image_bg
from components.navbar import navbar
from components.footer import footer
from components.config import icon_src

from backend.pdf_reader import extract_pdf
from backend.analyze import analyze_document
from backend.text_extract import extract_text_from_image

import io


@ui.page('/analyze')
def analyze():
    image_bg()
    navbar()

    with ui.column().classes('max-w-4xl mx-auto mt-40 w-full px-4'):
        ui.button('← Back to Home', on_click=lambda: ui.navigate.to('/')).props('flat').classes('amicus-back mb-4 self-start px-5 py-2 rounded-full text-white font-medium transition-all duration-300').style('background-color: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2);')
        ui.html("""
            <div style="text-align:center; margin-bottom: 1.8rem;">
                <div class="eyebrow text-white">Analysis tool</div>
                <h2 style="font-family: 'Fraunces', serif; font-weight: 500; font-size: clamp(2rem,4vw,2.8rem); color: #ffffff; letter-spacing:-0.03em; margin:0.4rem 0 0.4rem;">Decode your document</h2>
                <p class="text-white">Ask a question, choose a language, and upload to begin.</p>
            </div>
        """, sanitize=False)
        with ui.tabs().classes('w-full justify-center') as tabs:
            tab_analyze = ui.tab('Analyze')
            tab_about = ui.tab('About us')

        with ui.tab_panels(tabs, value=tab_analyze).classes('w-full bg-transparent'):

            with ui.tab_panel(tab_analyze):
                question_input = ui.input('Ask a specific question about your document (optional)').classes('w-full mb-6').props('rounded outlined dark label-color="white" input-class="text-white" color="white"')

                with ui.card().classes('amicus-card w-full p-8'):
                    with ui.row().classes('w-full justify-between items-center mb-6'):
                        with ui.row().classes('items-center gap-4'):
                            ui.image(icon_src).classes('w-12 h-12 rounded-xl')
                            ui.label('Plain-language analysis').classes('text-2xl font-bold font-serif text-white')

                        language_select = ui.select(
                            options=["English", "Spanish (Español)", "French (Français)", "Chinese (中文)",
                        "Arabic (العربية)", "Russian (Русский)", "Portuguese (Português)",
                        "Hindi (हिन्दी)", "Bengali (বাংলা)", "Japanese (日本語)", "German (Deutsch)",
                        "Korean (한국어)", "Italian (Italiano)", "Dutch (Nederlands)", "Turkish (Türkçe)",
                        "Vietnamese (Tiếng Việt)", "Polish (Polski)", "Ukrainian (Українська)",
                        "Romanian (Română)", "Greek (Ελληνικά)", "Czech (Čeština)", "Swedish (Svenska)",
                        "Hungarian (Magyar)", "Finnish (Suomi)", "Dansk (Danish)", "Norwegian (Norsk)",
                        "Catalan (Català)", "Indonesian (Bahasa Indonesia)", "Malay (Bahasa Melayu)",
                        "Thai (ไทย)", "Hebrew (עברית)", "Bulgarian (Български)", "Croatian (Hrvatski)",
                        "Estonian (Eesti)", "Gujarati (ગુજરાતી)", "Kannada (ಕನ್ನಡ)", "Latvian (Latviešu)",
                        "Lithuanian (Lietuvių)", "Malayalam (മലയാളം)", "Marathi (मराठी)",
                        "Slovak (Slovenčina)", "Slovenian (Slovenščina)", "Swahili (Kiswahili)",
                        "Tamil (தமிழ்)", "Telugu (తెలుగు)", "Urdu (اردو)", "Serbian (Српски)",
                        "Filipino (Filipino)", "Icelandic (Íslenska)", "Amharic (አማርኛ)",
                        "Armenian (Հայերեն)", "Azerbaijani (Azərbaycan dili)", "Basque (Euskara)",
                        "Galician (Galego)", "Georgian (ქართული)", "Kazakh (Қазақ тілі)",
                        "Khmer (ខ្Khmer)", "Lao (ລາວ)", "Macedonian (Македонски)", "Mongolian (Монгол)",
                        "Nepali (नेपाली)", "Sinhala (සිංහල)", "Albanian (Shqip)", "Bosnian (Bosanski)",
                        "Uzbek (Oʻzbekcha)", "Zulu (isiZulu)", "Afrikaans (Afrikaans)"],
                            value=None,
                            label="Language *"
                        ).props('outlined label-color="white"').classes('w-48 amicus-select rounded-xl')

                    upload_container = ui.column().classes('w-full')
                    with upload_container:
                        ui.label('Upload Document (PDF) or take a Photo').classes(
                            'font-bold text-white/70 mt-4'
                        )

                        with ui.card().classes(
                            'w-full p-8 border-2 border-dashed border-white/30 rounded-2xl '
                            'bg-white/5 backdrop-blur-md flex flex-col items-center justify-center '
                            'text-center cursor-pointer hover:border-white/60 hover:bg-white/10 '
                            'transition-all group'
                        ):
                            ui.html(
                                '<div style="font-size: 2.5rem; color: #ffffff; margin-bottom: 1rem;" '
                                'class="group-hover:scale-110 transition-transform">'
                                '<i class="fa-solid fa-cloud-arrow-up"></i></div>',
                                sanitize=False
                            )

                            ui.label('Drop your legal document here').classes(
                                'text-xl font-bold text-white mb-1'
                            ).style("font-family: 'Fraunces', serif;")

                            ui.label('Supports PDF and images up to 20MB').classes(
                                'text-sm text-white/70 mb-4'
                            )

                            ui.upload(
                                on_upload=lambda e: process_file(e),
                                auto_upload=True,
                                max_file_size=20_000_000,
                            ).props(
                                'accept=".pdf, image/*" flat bordered hide-upload-btn'
                            ).classes(
                                'w-full'
                            )

                            
                    loading_container = ui.column().classes('w-full items-center justify-center py-12').style('display: none;')
                    with loading_container:
                        ui.spinner('dots', size='4em', color='#8AB4FF')
                        ui.label('Analyzing document...').classes('text-lg font-bold text-white mt-4 font-serif')
                        ui.label('This usually takes a few seconds.').classes('text-white/60 text-sm mt-1')

                    result_container = ui.column().classes('w-full mt-2 p-2 bg-transparent').style('display: none;')
                    with result_container:
                        result_markdown = ui.markdown().classes('amicus-markdown w-full')
                        ui.button('Analyze another document', on_click=lambda: reset_ui()).props('outline rounded').classes('mt-8 amicus-ghost-btn')

                    def reset_ui():
                        result_container.style('display: none;')
                        upload_container.style('display: flex;')
                        result_markdown.set_content('')

                    async def process_file(e):
                        if not language_select.value:
                            ui.notify(
                                'Please select your preferred language before uploading a document.',
                                type='warning'
                            ).classes('amicus-warning')
                            return
                        try:
                            upload_container.style('display: none;')
                            loading_container.style('display: flex;')

                            file_content = await e.file.read()
                            is_pdf = e.file.name.lower().endswith('.pdf')
                            file_obj = io.BytesIO(file_content)

                            if is_pdf:
                                extracted_text = await run.io_bound(extract_pdf, file_obj)
                            else:
                                extracted_text = await run.io_bound(extract_text_from_image, file_obj)

                            if extracted_text and extracted_text.strip():
                                final_result = await run.io_bound(
                                    analyze_document,
                                    extracted_text,
                                    question_input.value,
                                    language_select.value
                                )
                                result_markdown.set_content(final_result)
                            else:
                                ui.notify('No readable text found in this file.', type='negative')
                                result_markdown.set_content("❌ No readable text found.")

                        except Exception as exc:
                            error_message = str(exc)

                            if '503' in error_message and 'UNAVAILABLE' in error_message:
                                friendly_message = """
                        ### Amicus is a little busy right now

                        Our AI is experiencing unusually high demand.

                        Please wait a moment and try uploading your document again.

                        Your document was not successfully analyzed.
                        """
                                ui.notify(
                                    'Amicus is temporarily busy. Please try again in a moment.',
                                    type='warning'
                                )
                                result_markdown.set_content(friendly_message)

                            else:
                                ui.notify(
                                    'Something went wrong while analyzing your document.',
                                    type='negative'
                                )
                                result_markdown.set_content(
                                    "**We couldn't analyze your document right now.**\n\n"
                                    "Please try again in a moment."
                                )
                        finally:
                            loading_container.style('display: none;')
                            result_container.style('display: flex;')

                    ui.html("""
                        <div style="display: flex; align-items: center; justify-content: center; gap: 12px; margin-top: 2rem; color: #ffffff; background: rgba(255,255,255,0.12); border-radius: 18px; padding: 16px 22px; font-size: 0.95rem; border: 1px solid rgba(255,255,255,0.25);">
                            <i class="fa-solid fa-shield-halved" style="color: #8AB4FF;"></i>
                            <span><b style="color:#ffffff;">Bank-grade encryption</b> · documents deleted after analysis</span>
                        </div>
                    """, sanitize=False)

            with ui.tab_panel(tab_about):
                with ui.column().classes('max-w-2xl mx-auto text-center mt-8'):
                    ui.label('Our mission').classes('eyebrow text-white')
                    ui.label('Language should never stand between you and justice.').classes('text-4xl font-bold text-white mt-2 mb-6').style("font-family: 'Fraunces', serif;")
                    ui.markdown("""
                        Navigating the American legal system can be overwhelming, especially when
                        language barriers stand in the way of justice.

                        For residents with Limited English Proficiency, a simple misunderstanding of
                        legal documents or complex political jargon can lead to unintended legal trouble
                        and compromised due process.

                        Our platform bridges this critical gap by empowering you to:
                        * **Fully understand** your rights.
                        * **Easily decode** complicated legal language.
                        * **Confidently plan** your next steps.
                    """).classes('amicus-markdown text-lg leading-relaxed text-left')

    footer()