import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import ingest
import os

# API KEY: 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
# streamlit run /Users/sabrinarenna/Documents/GitHub/RAG_Hacktogether/app/app_merged.py

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
    # Sidebar
    with st.sidebar:
        st.image("app/gptlearner.png", width=250)  # Replace with your logo
        openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
        # Set the API key as an environment variable
        os.environ["OPENAI_API_KEY"] = openai_api_key            

        subjects = ['Calculus 1', 'Physics', 'Computer Science', 'Finance']
        subject = st.selectbox("Choose your subject", subjects)

        pdf_file = st.file_uploader("Upload Your Own PDF", type=['pdf'])

        url = st.text_input("Enter a WebPage", placeholder="https://www.yourtopic.com")

        st.markdown("## Select the Language for Responses")
        languages = ["English", "Spanish", "French"]
        language = st.selectbox("", languages)

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