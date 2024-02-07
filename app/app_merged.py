import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import ingest
import os
import openai
import requests

def qa_llm(data, prompt):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(data, embedding=embeddings)

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
    try:
        # Sidebar
        with st.sidebar:
            st.image("Sample logo.png", width=180)  # Replace with your logo
            st.markdown("# Please enter your OpenAI API KEY", unsafe_allow_html=True)
            api_key = st.text_input("", type="password")
            openai.api_key = api_key

            st.markdown("<h2 style='font-size:smaller;margin-top:-20px;'>Choose your subject</h2>", unsafe_allow_html=True)
            subjects = ["Calculus 1", "Physics 1", "Finance", "History"]
            subject = st.selectbox("", subjects)

            st.markdown("<h2 style='font-size:smaller;margin-top:-20px;'>Upload Your Own PDF</h2>", unsafe_allow_html=True)
            pdf_file = st.file_uploader("", type=['pdf'])

            st.markdown("<h2 style='font-size:smaller;margin-top:-20px;'>Enter a WebPage URL</h2>", unsafe_allow_html=True)
            url = st.text_input("")

            st.markdown("<h2 style='font-size:smaller;margin-top:-20px;'>Select the Language for Responses</h2>", unsafe_allow_html=True)
            languages = ["English", "Spanish", "French", "German", "Italian", "Portuguese", "Chinese (Simplified)", "Japanese", "Hindi", "Yoruba", "Russian"]
            language = st.selectbox("", languages)

        # Check if any input is activated
        if 'input_activated' not in st.session_state:
            st.session_state.input_activated = False

        if subject or pdf_file or url:
            st.session_state.input_activated = True

        # If input is activated and language is selected, activate chat functionality
        if st.session_state.input_activated and language:
            # Remove all other elements and start chat functionality
            st.empty()
            if "messages" not in st.session_state:
                st.session_state["messages"] = [
                    {"role": "assistant", "content": "Hi, I'm a chatbot trained in first year university concepts. Ask select a topic and ask me question to learn with me."}
                ]

            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).write(msg["content"])

            if prompt := st.chat_input(placeholder="What's a derivative?"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.chat_message("user").write(prompt)

                data = ingest.context(subject)
                response = qa_llm(data, prompt)

                with st.chat_message("assistant"):
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    st.write(response)
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    main()