
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import re
from langchain_community.embeddings import HuggingFaceEmbeddings
import json
from dotenv import dotenv_values

config = dotenv_values('app/credentials.env')

huggingface_token = config['huggingface_token']


#clean loaded text
def preprocess(text):
    # Remove '\xa0' (non-breaking space)
    text = re.sub(r'\xa0', ' ', text)

    # Remove '\n' (newlines)
    text = re.sub(r'\n', ' ', text)

    # Remove consecutive dots ('.....') with just one dot
    text = re.sub(r'\.{2,}', '', text)

    # Remove '\uf0b7'
    text = re.sub(r'\uf0b7', ' ', text)

    # Remove consecutive spaces
    text = re.sub(r' +', ' ', text)

    return text

#load data from pdf files
def load_pdf(path):
    document = []
    page_contents = []
    reader = PdfReader(path)
    number_of_pages = len(reader.pages)

    #read each page on the pdf file 
    for i in range(0, number_of_pages):
        page = reader.pages[i]
        text = page.extract_text()
        document.append(text)
    
    #split the document into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512,
                                                   chunk_overlap=128,
                                                   length_function=len,
                                                   is_separator_regex=False)
    sentences = text_splitter.create_documents(document)
    #clean each sentence in the document
    for document in sentences:
        document.page_content = preprocess(document.page_content)
        page_contents.append(document.page_content)
    return page_contents

#convert data to vector embeddings
def generate_embeddings(text):
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    embeddings = embedding_model.embed_query(text)
    return embeddings


#generate embeddings for document title and contents in file 
def generate_embeddings_for_documents(data):
    subject = {}

    for filename, document in data.items():
        title_embeddings = generate_embeddings(filename)
        subject[filename] = {'title_embeddings': title_embeddings}
        subject[filename].update({f'page_content_{filename}_{i+1}': {'content': page, 'content_embeddings': generate_embeddings(page)} 
                                  for i, page in enumerate(document)})
        subject['@search.action'] = 'upload'

    return subject


#load data from directories
def context(option): 
    print("inside ingest.py", option)
    if option == 'Calculus 1':
        pdf_dir_path = 'app/Knowledge Base/Calculus 1'
    elif option == 'Physics':
        pdf_dir_path = 'app/Knowledge Base/Physics'
    elif option == 'Computer Science':
        pdf_dir_path = 'app/Knowledge Base/demo/Computer Science_full'
    elif option == 'Finance':
        pdf_dir_path = 'app/Knowledge Base/Finance'

    #load each file in directory and read the document 
    #save each document in dictionary with file name and file contents 
    data = {}
    for filename in os.listdir(pdf_dir_path):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(pdf_dir_path, filename)
            document = load_pdf(pdf_file_path)
            data[filename] = document

    course_jsonfile = generate_embeddings_for_documents(data)
    #write in a json file
    with open(f"{option}.json", "w") as f:
        json.dump(course_jsonfile, f)
    
    return data
     

