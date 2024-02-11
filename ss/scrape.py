import requests
from langchain_community.document_loaders import WebBaseLoader
import re

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

    # change \' to '
    text = re.sub(r'\\', '', text)

    return text

def scrape_web(url):
    
    loader = WebBaseLoader(url)
    scrape_data = loader.load()

    for document in scrape_data:
        document.page_content = preprocess(document.page_content)
    
    return scrape_data
