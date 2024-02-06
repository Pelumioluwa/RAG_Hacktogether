# -*- coding: utf-8 -*-
import streamlit as st
# from langchain.agents import initialize_agent, AgentType
# from langchain.callbacks import StreamlitCallbackHandler
# from langchain.chat_models import ChatOpenAI
# from langchain.tools import DuckDuckGoSearchRun

## from langchain.embeddings import OpenAIEmbeddings
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import PromptTemplate

import ingest

def qa_llm(data):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(data, embedding=embeddings)
    
    template = """You are a Deloitte chatbot. Provide succinct, professional answers to the questions asked.
    Context:
    {context}
    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""

    PROMPT = PromptTemplate(
        input_variables=["chat_history", "question", "context"],
        template=template
    )

    llm = ChatOpenAI(temperature=0.7, model_name="gpt-4")

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
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": PROMPT}
            )

# Main section streamlit run /Users/sabrinarenna/Documents/GitHub/RAG_Hacktogether/app/app.py
def main():

    # Sidebar
    with st.sidebar:
        st.sidebar.image("app/Sample logo.png", width=200)  # Replace with your logo
        openai_api_key = st.text_input("OpenAI API Key", key="langchain_search_api_key_openai", type="password")
        st.markdown("## Choose your subject")
        option = st.selectbox(
            'What subject do you need help with?',
            ('Calculus 1', 'Physics', 'Computer Science', 'Finance'))
        print(option) # For debugging

        st.write('You selected:', option)

        st.markdown("## Choose your language")
        languages = ["English", "Spanish", "French"]
        language = st.selectbox('What language do you want to study in?', languages)

    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input(placeholder="Who won the Women's U.S. Open in 2018?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        if not openai_api_key:
            st.info("Please add your OpenAI API key to continue.")
            st.stop()

        # llm = ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key, streaming=True)
        # search = DuckDuckGoSearchRun(name="Search")
        # search_agent = initialize_agent([search], llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, handle_parsing_errors=True)
        # with st.chat_message("assistant"):
        #     st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
        #     response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
        #     st.session_state.messages.append({"role": "assistant", "content": response})
        #     st.write(response)
        
        # start with logic to load the pdf
        data = ingest.context(option)
        response = qa_llm(data)

if __name__ == '__main__':
    main()
