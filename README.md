# gptScholar

Welcome to the GitHub repository of our app called **gptScholar** which we designed for the [AI-Chat-App-Hack](https://github.com/microsoft/AI-Chat-App-Hack), organized by Microsoft. **gptScholar** is a chatbot that aims to provide a platform for 1st year undergrad students to get assistance with their courses. The application uses technologies like Streamlit for the user interface, OpenAI's GPT-4 Turbo model for generating responses, and Python libraries such as langchain_openai and langchain_community for natural language processing tasks. With **gptScholar**, students can upload PDF files, enter URLs to webpages, or select specific subjects such as Calculus 1, Physics, Computer Science, or Finance. The chatbot then processes the input data, extracts relevant information, and provides answers and insights tailored to the user's queries. Whether it's seeking explanations for academic concepts, clarifying doubts, or exploring innovative solutions, gptScholar offers a convenient and efficient platform to support students' educational endeavors.

![Icon](gpt_scholar.png)

## Product Overview

**gptScholar** is a Streamlit application deployed on **Microsoft Azure**, designed to facilitate the evaluation of various concepts and topics using Large Language Models (LLMs). Leveraging the powerful GPT-4 Turbo model, the application provides insights and answers to users' questions across different domains.

One of the unique features of **gptScholar** is its implementation of the **RAG (Retriever Augmented Generation)** architecture, enhancing the efficiency and accuracy of responses. The Retriever component helps in retrieving relevant information from the input data, the Answer Generator generates candidate answers based on the retrieved information, and the Generator fine-tunes the answers to provide contextually accurate responses.

**gptScholar** offers multilingual support. Students can enter their queries in any language, and the application will provide responses in the selected language from the dropdown. This feature enhances accessibility and accommodates users from diverse linguistic backgrounds.

Users interact with the application by either uploading PDF files, entering URLs to webpages, or selecting specific subjects of interest. The application then processes the input data, extracts relevant information using the RAG architecture, and utilizes the GPT-4 Turbo model to generate responses.

The application's versatility allows users to explore various subjects, seek clarification on complex topics, or simply engage in educational interactions powered by AI technology. While gptScholar is primarily designed for academic purposes, its functionality extends beyond academia. Users can upload PDFs or website URLs and ask questions related to the content provided, regardless of its origin.

Whether you're a student seeking explanations for academic concepts, a professional looking for insights into specific domains, or simply curious about a wide range of topics, **gptScholar** offers a convenient platform to satisfy your informational needs.

## Sample Product Use Cases

- **Academic Evaluation**: Students and researchers can utilize gptScholar to evaluate various academic concepts and topics, gaining insights and answers across different domains.

- **Professional Research**: Professionals across industries can use gptScholar to conduct research, gather insights, and seek clarification on specific topics relevant to their field.
  
- **Language Learning**: Language learners can leverage the multilingual support of gptScholar to practice reading comprehension, understanding of complex texts and writing in different languages.

- **Fact-Checking**: Journalists, fact-checkers, and individuals interested in verifying information can employ gptScholar to quickly access reliable information from various pdfs or weblinks.

- **Personal Interest Exploration**: Individuals can explore a wide range of topics and quickly retrieve information from pdfs and weblinks.

## Project Structure

The project consists of the following files:

- **app.py**: This file contains the main script that runs the Streamlit application. It handles user interactions, file uploads, and the evaluation of business ideas using the GPT-4 Turbo model.
  
- **ingest.py**: This script provides functions for loading data, including PDF documents and webpages, for analysis. It preprocesses the data to prepare it for evaluation.
  
- **pdf_upload.py**: This script is responsible for extracting text content from PDF files. It preprocesses the text to remove unwanted characters and normalizes whitespace.
  
- **translate_response.py**: This script handles the translation of responses into different languages using the OpenAI API. It interacts with the GPT-4 Turbo model to generate translated responses.

- **cosmodb**: This folder includes scripts for setting up database on CosmosDB, uploading data to CosmosDB, setting up indexer on Azure AI search and connecting CosmosDB with Azure AI search for ease of interaction and data pipeline
  
- **speech_to_text.py**: This script receives query from users in form of spoken words and passes it into the chatbot. It receives speech in 4 languages: English, Italian, French and Hindi.

## Demo

Check out a short demo of our project on YouTube:

[![Demo Video](https://img.youtube.com/vi/O2Pb5XlDMCM/0.jpg)](https://www.youtube.com/watch?v=O2Pb5XlDMCM)
 

## Access the App 

To access the application, visit: [hackapp.eastus.azurecontainer.io](hackapp.eastus.azurecontainer.io)


## Teammates

This project was developed by MMAI Students of Schulich School of Business:

| Name             | Email                  | Socials                                      |
|------------------|------------------------|-------------------------------------------------------|
| Pelumioluva Abiola| pelumi@schulich.yorku.ca| [LinkedIn](https://www.linkedin.com/in/pelumioluwa-abiola-a136bbab/)      |
| Sabrina Renna    | srenna@schulich.yorku.ca | [LinkedIn](https://www.linkedin.com/in/sabrinarenna/)               |
| Sushmit Richard  | sushmit9@schulich.yorku.ca | [LinkedIn](https://www.linkedin.com/in/sushmitrichard/)        |

Feel free to reach out to any of us for inquiries or collaborations!
