import re
from io import BytesIO
import pdfplumber

def extract_text_from_pdf(pdf_data):
    """
    Extract text content from a PDF file and perform basic text preprocessing.

    Args:
        pdf_data (bytes): Binary data representing the contents of the PDF file.

    Returns:
        list: A list of dictionaries, where each dictionary contains the text content of a page.
    """
    pages_content = []
    with BytesIO(pdf_data) as f:
        with pdfplumber.open(f) as pdf:
            for page in pdf.pages:
                # Extract text content from each page
                text_content = page.extract_text()
                # Basic text preprocessing
                text_content = preprocess(text_content)
                # Append preprocessed text content to the list
                pages_content.append({"page_content": text_content})
    
    return pages_content

def preprocess(text):
    """
    Preprocess text content by removing unwanted characters and normalizing whitespace.

    Args:
        text (str): Text content to preprocess.

    Returns:
        str: Preprocessed text content.
    """
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