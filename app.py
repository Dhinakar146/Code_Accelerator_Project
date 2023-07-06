import os
import tempfile
import streamlit as st
from streamlit_chat import message
from utils.chain import generate_response
from utils.document_loader import get_pages
from utils.similarity_search import get_data
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="HugChat - An LLM-powered Streamlit app")

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 Code Accelerator Project')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - Langchain
    - Openai
    - Streamlit

    💡 Note: API key required!
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ for Data CoE')
    api_key = st.text_input(label='Enter API Key')

os.environ['OPENAI_API_KEY'] = api_key

uploaded_file = st.file_uploader("Choose a pdf file", type=['pdf'])
if uploaded_file is not None:
    # To read file as bytes:
    temp_dir = tempfile.TemporaryDirectory()
    temp_file_path = os.path.join(temp_dir.name, uploaded_file.name)
    with open(temp_file_path, "wb") as temp_file:
        temp_file.write(uploaded_file.read())
    pages = get_pages(temp_file_path)

# Generate empty lists for generated and past.
# generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]
# past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()


# User input
# Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text


# Applying the user input box
with input_container:
    user_input = get_text()


# Response output
# Function for taking user prompt as input followed by producing AI generated responses
def generate_response_st(question):
    """This function generates response"""

    # getting similar data
    data = get_data(pages, question)

    # generating response
    response = generate_response(data, question)

    return response


# Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response_st(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)

    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))
