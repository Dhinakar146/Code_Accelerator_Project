import time
import gradio as gr
from config import *
from utils.chain import generate_response
from utils.document_loader import get_pages
from utils.similarity_search import get_data


# variables
pages = []


def process_doc(pdf_path):
    """This function process input pdf file document from gradio"""
    global pages
    pages = get_pages(pdf_path.name)


def bot_response(question: str, pages: list) -> str:
    """This function generates response message for chatbot"""

    # getting similar data
    data = get_data(pages, question)

    # generating response
    response = generate_response(data, question)

    return response


def respond(message, chat_history):
    """This function generates response message for chatbot"""
    global pages
    bot_message = bot_response(message, pages)
    chat_history.append((message, bot_message))
    time.sleep(2)
    return "", chat_history


with gr.Blocks() as interface:

    # title
    gr.Markdown('''# Code Accelerator Project''')

    # upload section
    upload_pdf = gr.File(file_types=['.pdf'], label="Upload PDF File")
    upload_pdf.upload(process_doc, inputs=[upload_pdf])

    # chatbot section
    chatbot = gr.Chatbot(label="Chatbot")

    # message section
    msg = gr.Textbox(label="Enter Question")

    # clear button
    clear = gr.ClearButton([msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

interface.launch()
