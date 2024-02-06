import streamlit as st

# Sidebar
st.sidebar.image("app/Sample logo.png", width=200)  # Replace with your logo
st.sidebar.button("Environment")
chat_button = st.sidebar.button("Chat")

# Main section
st.markdown("# Please enter your OpenAI API KEY")
api_key = st.text_input("", type="password")

st.markdown("## Choose your subject")
col1, col2 = st.columns(2)
with col1:
    calc_button = st.button("Calculus 1")
    fin_button = st.button("Finance")
with col2:
    phys_button = st.button("Physics 1")
    hist_button = st.button("History")

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

if calc_button or phys_button or fin_button or hist_button or pdf_file or url:
    st.session_state.input_activated = True

# If input is activated and language is selected, activate chat functionality
if st.session_state.input_activated and language:
    # Remove all other elements and start chat functionality
    st.empty()
    st.write("Chat functionality goes here")