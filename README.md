# gptScholar

Welcome to the GitHub repository of our app called **gptScholar** which we designed by [AI-CHAT-APP-HACK](https://github.com/microsoft/AI-Chat-App-Hack), organized by Microsoft. **gptScholar** is a chatbot that aims to provide a platform for 1st year undergrad students to get assistance with their courses. The application The application uses technologies like Streamlit for the user interface, OpenAI's GPT-4 Turbo model for generating responses, and Python libraries such as langchain_openai and langchain_community for natural language processing tasks. With gptScholar, students can upload PDF files, enter URLs to webpages, or select specific subjects such as Calculus 1, Physics, Computer Science, or Finance. The chatbot then processes the input data, extracts relevant information, and provides answers and insights tailored to the user's queries. Whether it's seeking explanations for academic concepts, clarifying doubts, or exploring innovative solutions, gptScholar offers a convenient and efficient platform to support students' educational endeavors.

![Icon](gpt_scholar.png)

## Product Overview

**gptScholar** is a Streamlit application deployed on **Microsoft Azure**, designed to facilitate the evaluation of various concepts and topics using Large Language Models (LLMs). Leveraging the powerful GPT-4 Turbo model, the application provides insights and answers to users' questions across different domains.

Users interact with the application by either uploading PDF files, entering URLs to webpages, or selecting specific subjects of interest. The application then processes the input data, extracts relevant information, and utilizes the GPT-4 Turbo model to generate responses.

One of the unique features of **gptScholar** is its multilingual support. Students can enter their queries in any language, and the application will provide responses in the selected language from the dropdown. This feature enhances accessibility and accommodates users from diverse linguistic backgrounds.

Upon uploading a PDF file or entering a URL, users can ask questions related to the content, and the application provides answers based on the analysis performed by the GPT-4 Turbo model. Additionally, users can select specific subjects, such as Calculus 1, Physics, Computer Science, or Finance, to receive information and answers tailored to those topics.

The application's versatility allows users to explore various subjects, seek clarification on complex topics, or simply engage in educational interactions powered by AI technology.

Whether you're a student seeking explanations for academic concepts, a professional looking for insights into specific domains, or simply curious about a wide range of topics, **gptScholar** offers a convenient platform to satisfy your informational needs.

## Project Structure

The project consists of the following Python files:

- **App.py**: This file contains the main script that runs the Streamlit application. It handles user interactions, file uploads, and the evaluation of business ideas using the GPT-4 Turbo model.
  
- **Ingest.py**: This script provides functions for loading data, including PDF documents and webpages, for analysis. It preprocesses the data to prepare it for evaluation.
  
- **Pdf_upload.py**: This script is responsible for extracting text content from PDF files. It preprocesses the text to remove unwanted characters and normalizes whitespace.
  
- **Translate_response.py**: This script handles the translation of responses into different languages using the OpenAI API. It interacts with the GPT-4 Turbo model to generate translated responses.

## Access the App 

To access the application, visit: [hackapp.eastus.azurecontainer.io](hackapp.eastus.azurecontainer.io)


## Teammates

This project was developed by the following team members:

| Name             | Email                  | Socials                                      |
|------------------|------------------------|-------------------------------------------------------|
| Pelumioluva Abiola| pelumi@schulich.yorku.ca| [LinkedIn](https://www.linkedin.com/in/pelumioluwa-abiola-a136bbab/)      |
| Sabrina Renna    | srenna@schulich.yorku.ca | [LinkedIn](https://www.linkedin.com/in/sabrinarenna/)               |
| Sushmit Richard  | sushmit9@schulich.yorku.ca | [Twitter](https://www.linkedin.com/in/sushmitrichard/)        |


