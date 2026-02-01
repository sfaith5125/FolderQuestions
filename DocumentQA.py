"""DocumentQA

Interactive Q&A system that loads documents from a folder and answers questions
about them using Google Gemini 2.5 Flash.

Usage: python DocumentQA.py [folder_path]
  If folder_path is not provided, defaults to "./documents"

Requires: google-generativeai, PyPDF2, python-docx
Install: pip install google-generativeai PyPDF2 python-docx

"""

import os
import sys
from pathlib import Path
import json

try:
    import google.generativeai as genai
    from PyPDF2 import PdfReader
    from docx import Document as DocxDocument
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required packages:")
    print("  pip install anthropic PyPDF2 python-docx")
    sys.exit(1)


def extract_text_from_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        text = []
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text.append(f"--- Page {page_num + 1} ---\n{page_text}")
        return "\n".join(text)
    except Exception as e:
        print(f"Error extracting PDF {file_path}: {e}")
        return ""


def extract_text_from_docx(file_path):
    """Extract text from a DOCX file."""
    try:
        doc = DocxDocument(file_path)
        paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
        return "\n".join(paragraphs)
    except Exception as e:
        print(f"Error extracting DOCX {file_path}: {e}")
        return ""


def extract_text_from_txt(file_path):
    """Extract text from a TXT file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading TXT {file_path}: {e}")
        return ""


def load_documents_from_folder(folder_path):
    """
    Recursively scan folder for documents and extract text.
    Returns a dict: {file_path: extracted_text}
    """
    documents = {}
    supported_extensions = {'.pdf', '.txt', '.docx'}
    
    folder_path = Path(folder_path)
    if not folder_path.exists():
        print(f"Folder not found: {folder_path}")
        return documents
    
    print(f"Scanning folder: {folder_path}")
    
    for file_path in folder_path.rglob('*'):
        if file_path.is_file():
            ext = file_path.suffix.lower()
            if ext not in supported_extensions:
                continue
            
            print(f"  Loading {file_path.name}...", end=" ", flush=True)
            text = None
            
            if ext == '.pdf':
                text = extract_text_from_pdf(file_path)
            elif ext == '.docx':
                text = extract_text_from_docx(file_path)
            elif ext == '.txt':
                text = extract_text_from_txt(file_path)
            
            if text:
                documents[str(file_path)] = text
                print(f"✓ ({len(text)} chars)")
            else:
                print("(empty or failed)")
    
    print(f"\nLoaded {len(documents)} document(s).\n")
    return documents


def build_system_prompt(documents):
    """
    Build a system prompt that includes all document text.
    This provides context to Claude for answering questions.
    """
    if not documents:
        return "You are a helpful assistant."
    
    doc_content = "\n\n---\n\n".join([
        f"Document: {path}\n\n{text[:3000]}"  # limit text per doc to avoid token overload
        for path, text in documents.items()
    ])
    
    system_prompt = f"""You are a helpful assistant that answers questions about the following documents:

{doc_content}

Please answer questions based on the provided document content. If information is not in the documents, 
say so explicitly. Be concise and accurate."""
    
    return system_prompt


def interactive_qa_loop(documents):
    """
    Interactive loop where user asks questions and Claude answers.
    """
    if not documents:
        print("No documents loaded. Exiting.")
        return
    
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
    client = genai.GenerativeModel('gemini-2.5-flash')
    system_prompt = build_system_prompt(documents)
    
    print("=" * 60)
    print("Document Q&A System Ready")
    print("=" * 60)
    print(f"Documents loaded: {len(documents)}")
    print("Type 'exit' or 'quit' to exit.\n")
    
    while True:
        user_question = input("Ask a question about the documents: ").strip()
        
        if user_question.lower() in ('exit', 'quit'):
            print("Goodbye!")
            break
        
        if not user_question:
            print("Please enter a question.\n")
            continue
        
        print("\nThinking...", end=" ", flush=True)
        
        try:
            full_prompt = f"{system_prompt}\n\nUser Question: {user_question}"
            response = client.generate_content(full_prompt)
            answer = response.text
            
            print("\n")
            print(f"Answer:\n{answer}\n")
        
        except Exception as e:
            print(f"\nAPI Error: {e}\n")


def main():
    # Get folder path from command line or use default
    if len(sys.argv) > 1:
        folder_path = sys.argv[1]
    else:
        folder_path = "./documents"
    
    # Load all documents from folder
    documents = load_documents_from_folder(folder_path)
    
    if not documents:
        print("No documents found. Please add PDF, DOCX, or TXT files to the folder.")
        sys.exit(1)
    
    # Start interactive Q&A loop
    interactive_qa_loop(documents)


if __name__ == '__main__':
    main()
