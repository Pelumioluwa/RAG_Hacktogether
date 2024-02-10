from openai import OpenAI  # Assuming this is the OpenAI API
import streamlit as st

def translate(response, language):
    # Initialize the OpenAI client
    client = OpenAI()

    # Construct the prompt with placeholders for response and language
    prompt = f"Translate the following text into {language}: {response}"

    try:
        # Create the assistant with the specific instructions for translation
        assistant = client.beta.assistants.create(
            instructions=prompt,
            model="gpt-4-turbo-preview"
        )

        # Generate translation using the assistant
        thread = client.beta.threads.create(
            messages=[{"role": "user", "content": prompt}]
        )

        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Wait for the translation to complete
        while run.status != "completed":
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        # Retrieve the translated response
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        translated_response = messages.data[0].content[0].text.value

        # Check if a valid translation is received
        if translated_response and isinstance(translated_response, str):
            return translated_response
        else:
            raise ValueError("Empty or invalid response received from the language model.")

    except Exception as e:
        # Handle any errors that occur during translation
        st.error(f"An error occurred during translation: {e}")
        return "Error occurred during translation"
