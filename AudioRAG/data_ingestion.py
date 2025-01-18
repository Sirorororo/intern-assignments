from pdfminer.high_level import extract_text
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def extract_text_from_pdf(pdf_file):
    return extract_text(pdf_file)

def text_cleaning(text):
    text_modified = re.sub(r'-\n', '', text) # Concatinating same words on multiple lines
    text_modified = re.sub(r'(?<!\n)\n(?!\n)', ' ', text_modified) # Add space between words on multiple lines
    return text_modified

def chunk_text(text):
    print("inside chunk_text")
    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n\n", "\n\n",".","\n"],  # Prioritize splitting by paragraphs, then sentences, then spaces
        chunk_size = 500,  # Maximum size of each chunk
        chunk_overlap = 100  # Overlap to maintain context between chunks
    )
    print("Instantiation done")
    chunks = text_splitter.split_text(text)
    print("splitting done")
    return chunks

def clean_chunk(chunk):
    cleaned_chunk = chunk.strip() # remove leading/trailing whitespaces
    cleaned_chunk = re.sub(r'^\.+', '', cleaned_chunk) # remove leading fullstops
    cleaned_chunk = re.sub(r'\n+', ' ', cleaned_chunk) # remove \n\n
    cleaned_chunk = cleaned_chunk.strip()
    return cleaned_chunk

def clean_all_chunks(chunks):
    return [clean_chunk(chunk) for chunk in chunks]

def create_chunks(pdf_file):
    text = extract_text_from_pdf(pdf_file)
    print("Extracted text")
    cleaned_text = text_cleaning(text)
    print("Cleaned Text")
    chunked_text = chunk_text(cleaned_text)
    print("Created chunks")
    cleaned_chunks = clean_all_chunks(chunked_text)
    print("Cleaned chunks")
    return cleaned_chunks

    