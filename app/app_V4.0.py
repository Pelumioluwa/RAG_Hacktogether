import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import pdf_upload
import ingest
import scrape
import translate_response
import os

# streamlit run /Users/sabrinarenna/Documents/GitHub/RAG_Hacktogether/app/app_V4.0.py

# Function to perform question answering using OpenAI LLM with given data
def qa_llm(data, prompt):
    # Initialize OpenAI embeddings and Chroma vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_documents(data, embedding=embeddings)

    # Initialize ChatOpenAI model
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview")

    # Initialize conversation memory
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'
    )

    # Initialize conversational retrieval chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=True
    )
    
    # Get response from the model
    result = conversation_chain({"question": prompt})

    return result["answer"]

# Function to read user PDF and send it to the LLM for question answering
def qa_pdf_llm(data, prompt):
    # Initialize OpenAI embeddings and Chroma vector store
    embeddings = OpenAIEmbeddings()
    vectorstore = Chroma.from_texts([page['page_content'] for page in data], embedding=embeddings)

    # Initialize ChatOpenAI model
    llm = ChatOpenAI(temperature=0, model_name="gpt-4-turbo-preview")

    # Initialize conversation memory
    memory = ConversationBufferMemory(
        memory_key='chat_history',
        return_messages=True,
        output_key='answer'
    )

    # Initialize conversational retrieval chain
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever(),
        memory=memory,
        return_source_documents=True
    )
    
    # Get response from the model
    result = conversation_chain({"question": prompt})

    return result["answer"]

def main():
    # Initialize session state if not already initialized
    if 'input_method' not in st.session_state:
        st.session_state.input_method = None
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = "English"  # Default language

    # Sidebar
    with st.sidebar:
        st.image("gpt_scholar.png", width=250)  # Replace with your logo

        # OpenAI API Key input field
        openai_api_key = st.text_input("Enter your OpenAI API Key", key="langchain_search_api_key_openai", type="password")
        # Set the API key as an environment variable
        os.environ["OPENAI_API_KEY"] = openai_api_key            

        # Subject input field
        subjects = ['','Calculus 1', 'Physics', 'Computer Science', 'Finance']
        subject = st.selectbox("Select A Subject", subjects) 

        # PDF file uploader
        pdf_file = st.file_uploader("Upload Your Own PDF", type=['pdf']) 
        # "Read PDF" button
        read_pdf_button = st.button('Read PDF')  
        if pdf_file and read_pdf_button:
            st.session_state.input_method = 'pdf'           
                    
        # URL input field
        url = st.text_input("Enter a Webpage", placeholder="https://www.yourtopic.com") 
        # "Read URL" button
        read_url_button = st.button('Read URL')  
        if url and read_url_button:
            st.session_state.input_method = 'url'
        
        # Language selection
        languages = ["English", "Spanish", "French","Hindi","Chinese","Arabic","Russian","Portuguese","Japanese","German","Korean","Italian","Turkish","Dutch"]
        st.session_state.selected_language  = st.selectbox("Select the Language for Responses", languages)

    # Check if any input is activated
    if 'input_activated' not in st.session_state:
        st.session_state.input_activated = False

    if subject or pdf_file or url:
        st.session_state.input_activated = True

    # If input is activated and language is selected, activate chat functionality
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a chatbot trained in first year university concepts. Select a topic and ask me question to learn with me. I can also read PDFs and Webpages and answer questions about them."}
    ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])
    
    if st.session_state.input_method == 'subject':
        data = ingest.context(subject)

    elif st.session_state.input_method == 'pdf':
        pdf_data = pdf_file.read()
        pdf_filename = pdf_file.name  # Get the name of the uploaded PDF file
        st.info(f"PDF File '{pdf_filename}' Read Successfully. Ask your question now!")

        # Read the PDF file and send it to the LLM            
        data = pdf_upload.extract_text_from_pdf(pdf_data)
   
    elif st.session_state.input_method == 'url':
        st.info(f"URL Read Successfully. Ask your question now!")
        data = scrape.scrape_web(url)

    if prompt := st.chat_input(placeholder="What's a derivative?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        if st.session_state.input_method == 'subject':
            response = qa_llm(data, prompt)
      
        elif st.session_state.input_method == 'pdf':
            response = qa_pdf_llm(data, prompt)

        elif st.session_state.input_method == 'url':
            response = qa_llm(data, prompt)

        translated_response = translate_response.translate(response, st.session_state.selected_language)
        with st.chat_message("assistant"):
            st.session_state.messages.append({"role": "assistant", "content": translated_response})
            st.write(translated_response)
    

if __name__ == '__main__':
    main()
