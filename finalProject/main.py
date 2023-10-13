from typing import List, Tuple

from langchain.chains import ConversationChain
from langchain.chat_models import ChatOpenAI

from nicegui import Client, ui

OPENAI_API_KEY = "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"  # TODO: set your OpenAI API key here

llm = ConversationChain(llm=ChatOpenAI(model_name='gpt-3.5-turbo', openai_api_key='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'))


messages: List[Tuple[str, str]] = [('HydroBud', 'Hello! I am HydroBud, a specialized AI chatbot created to enhance water sanitation systems. How can I be of assistance to you?')]
thinking: bool = False

@ui.refreshable
async def chat_messages() -> None:
    for name, text in messages:
        ui.chat_message(text=text, name=name, sent=name == 'You')
    if thinking:
        ui.spinner(size='3rem').classes('self-center')
    await ui.run_javascript('window.scrollTo(0, document.body.scrollHeight)', respond=False)




@ui.page('/')
async def main(client: Client):
    async def send() -> None:
        global thinking
        user_message = text.value
        messages.append(('You', user_message))
        thinking = True
        text.value = ''
        chat_messages.refresh()

        # Add your specific prompt here
        water_conservation_prompt = "Specifically reply with questions related to water conservation, otherwise say I cant help you with that" + user_message
        response = await llm.arun(water_conservation_prompt)
        messages.append(('Bot', response))
        thinking = False
        chat_messages.refresh()

    anchor_style = r'a:link, a:visited {color: inherit !important; text-decoration no;text-decoration:none; font-weight: 500}'
    ui.add_head_html(f'<style>{anchor_style}</style>')
    await client.connected()

    with ui.column().classes('w-full max-w-2xl mx-auto items-stretch'):
        await chat_messages()

    with ui.footer().classes('bg-white'), ui.column().classes('w-full max-w-3xl mx-auto my-6'):
        with ui.row().classes('w-full no-wrap items-center'):
            placeholder = 'message' if OPENAI_API_KEY != 'not-set' else \
                'Please provide your OPENAI key in the Python script first!'
            text = ui.input(placeholder=placeholder).props('rounded outlined input-class=mx-3') \
                .classes('w-full self-center').on('keydown.enter', send)


ui.run(title='Chat with GPT-3 (example)')