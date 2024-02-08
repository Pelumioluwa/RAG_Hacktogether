import streamlit as st
from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import ingest
import os

# streamlit run /Users/sabrinarenna/Documents/GitHub/RAG_Hacktogether/app/app_merged.py

def qa_llm(data, prompt):
    embeddings = OpenAIEmbeddings()
    #vectorstore = FAISS.from_documents(data, embedding=embeddings)
    vectorstore = Chroma.from_documents(data, embedding=embeddings)

    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview")

    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'
    )

    conversation_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(),
            memory=memory,
            return_source_documents=True)
    
    result = conversation_chain({"question": prompt})

    return result["answer"]

def main():
    # Initialize session state if not already initialized
    if 'input_method' not in st.session_state:
        st.session_state.input_method = None

    # Sidebar
    with st.sidebar:
        st.image("gptlearner.png", width=250)  # Replace with your logo
        st.markdown("<div style='font-size:medium; font-weight:bold; margin-bottom:-50px; margin-top:0px;'>Enter your OpenAI API Key</div>", unsafe_allow_html=True)
        openai_api_key = st.text_input("", key="langchain_search_api_key_openai", type="password")
        # Set the API key as an environment variable
        os.environ["OPENAI_API_KEY"] = openai_api_key            

        st.markdown("<div style='font-size:medium; font-weight:bold; margin-bottom:-50px; margin-top:0px;'>Choose your subject</div>", unsafe_allow_html=True)
        subjects = ['Calculus 1', 'Physics', 'Computer Science', 'Finance']
        subject = st.selectbox("", subjects) if st.session_state.input_method is None else None

        # PDF file uploader
        st.markdown("<div style='font-size:medium; font-weight:bold; margin-bottom:-50px; margin-top:0px;'>or Upload Your Own PDF</div>", unsafe_allow_html=True)
        pdf_file = st.file_uploader("", type=['pdf']) if st.session_state.input_method is None else None
        # "Read PDF" button
        read_pdf_button = st.button('Read PDF')  # always render the button
        if pdf_file and read_pdf_button:
            st.session_state.input_method = 'pdf'
            # Read the PDF file and send it to the LLM
            data = ingest.context(pdf_file.getvalue())

        # URL input field
        st.markdown("<div style='font-size:medium; font-weight:bold; margin-bottom:-50px; margin-top:0px;'>or Enter a WebPage</div>", unsafe_allow_html=True)
        url = st.text_input("", placeholder="https://www.yourtopic.com") if st.session_state.input_method is None else None
        # "Read URL" button
        read_url_button = st.button('Read URL')  # always render the button
        if url and read_url_button:
            st.session_state.input_method = 'url'
            # Read the webpage and send it to the LLM
            data = ingest.context(url)

        st.markdown("<div style='font-size:medium; font-weight:bold; margin-bottom:-50px; margin-top:0px;'>Select the Language for Responses</div>", unsafe_allow_html=True)
        languages = ["English", "Spanish", "French"]
        language = st.selectbox("", languages)

        if st.session_state.input_method == 'subject':
            data = ingest.context(subject)
        elif st.session_state.input_method == 'pdf':
            data = ingest.context(pdf_file.getvalue())  # assuming ingest.context can handle a PDF file
        elif st.session_state.input_method == 'url':
            data = ingest.context(url)  # assuming ingest.context can handle a URL

    # Check if any input is activated
    if 'input_activated' not in st.session_state:
        st.session_state.input_activated = False

    if subject or pdf_file or url:
        st.session_state.input_activated = True

    # If input is activated and language is selected, activate chat functionality
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot trained in first year university concepts. Ask select a topic and ask me question to learn with me."}
    ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="What's a derivative?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        data = ingest.context(subject)
        response = qa_llm(data, prompt)

        with st.chat_message("assistant"):
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.write(response)


if __name__ == '__main__':
    main()
