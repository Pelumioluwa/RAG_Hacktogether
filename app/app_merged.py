import streamlit as st
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
import ingest
import os

def qa_llm(data, prompt):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(data, embedding=embeddings)

    llm = ChatOpenAI(temperature=0, model_name="gpt-4")

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
        st.image("Sample logo.png", width=200)  # Replace with your logo
        st.markdown("# Please enter your OpenAI API KEY")
        api_key = st.text_input("", type="password")

        st.markdown("## Choose your subject")
        subjects = ["Calculus 1", "Physics 1", "Finance", "History"]
        subject = st.selectbox("", subjects)

        st.markdown("## Upload Your Own PDF")
        pdf_file = st.file_uploader("", type=['pdf'])

        st.markdown("## Enter a WebPage")
        url = st.text_input("")

        st.markdown("## Select the Language for Responses")
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
        st.write("Chat functionality goes here")

        if "messages" not in st.session_state:
            st.session_state["messages"] = [
                {"role": "assistant", "content": "Hi, I'm a chatbot trained in first year university concepts. Ask select a topic and ask me question to learn with me."}
            ]

        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])

        if prompt := st.chat_input(placeholder="What's a derivative?"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.chat_message("user").write(prompt)

            if not api_key:
                st.info("Please add your OpenAI API key to continue.")
                st.stop()

            data = ingest.context(subject)
            response = qa_llm(data, prompt)

            with st.chat_message("assistant"):
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.write(response)

if __name__ == '__main__':
    main()