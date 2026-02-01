"""DocumentQA - Local Ollama Version

Interactive Q&A system that loads documents from a folder and answers questions
about them using local LLM models via Ollama.

Usage: python DocumentQA.py [folder_path]
  If folder_path is not provided, defaults to "./documents"

Requires: requests, PyPDF2, python-docx, scikit-learn
Install: pip install requests PyPDF2 python-docx scikit-learn

"""

import os
import sys
from pathlib import Path
import json
import requests

try:
    from PyPDF2 import PdfReader
    from docx import Document as DocxDocument
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required packages:")
    print("  pip install requests PyPDF2 python-docx scikit-learn")
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
    This provides context to Gemini for answering questions.
    """
    if not documents:
        return "You are a helpful assistant."
    
    doc_content = "\n\n---\n\n".join([
        f"Document: {path}\n\n{text[:5000]}"  # Increased from 3000 to provide more context
        for path, text in documents.items()
    ])
    
    system_prompt = f"""You are an expert analyst providing detailed, well-researched answers based ONLY on the provided documents.

DOCUMENTS:
{doc_content}

CRITICAL INSTRUCTIONS:
1. Answer must be comprehensive and detailed - provide full explanations, not brief summaries
2. Quote or paraphrase specific evidence directly from the documents
3. For each major point, identify which source document(s) support it
4. Structure complex answers with clear headers, bullet points, or numbered lists
5. Include specific facts: numbers, dates, names, metrics, percentages from the documents
6. Explain the relationship between different concepts mentioned in the documents
7. Address ALL parts of the question thoroughly - do not skip any aspect
8. If the question asks for analysis, synthesis, or comparison, provide that explicitly
9. If information needed to answer is NOT in the documents, clearly state "This information is not in the provided documents"
10. NEVER invent, assume, or infer information beyond what is explicitly in the documents
11. When information is ambiguous, acknowledge the ambiguity and provide your best interpretation based on context
12. End with a brief summary if the answer is lengthy

ANSWER QUALITY REQUIREMENT: Provide 3-5 substantial paragraphs for most questions, more if needed."""
    
    return system_prompt


def interactive_qa_loop(documents, ollama_url="http://localhost:11434"):
    """
    Interactive loop where user asks questions and Ollama answers.
    """
    if not documents:
        print("No documents loaded. Exiting.")
        return
    
    # Check if Ollama is running
    try:
        response = requests.get(f'{ollama_url}/api/tags', timeout=2)
        if response.status_code != 200:
            print("Error: Could not connect to Ollama.")
            print("Please ensure Ollama is running: ollama serve")
            return
        
        models = response.json().get('models', [])
        if not models:
            print("Error: No models found in Ollama.")
            print("Please pull a model first: ollama pull openchat")
            return
        
        # Prefer openchat, then mistral, then use first available
        model_names = [m['name'] for m in models]
        if 'openchat' in model_names:
            ollama_model = 'openchat'
        elif 'mistral' in model_names:
            ollama_model = 'mistral'
        else:
            ollama_model = model_names[0]
        print(f"Using model: {ollama_model}")
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama at " + ollama_url)
        print("Please start Ollama with: ollama serve")
        return
    
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
            
            # Call the Ollama API
            response = requests.post(
                f"{ollama_url}/api/generate",
                json={
                    "model": ollama_model,
                    "prompt": full_prompt,
                    "stream": False,
                    "temperature": 0.7,
                },
                timeout=120  # Give Ollama up to 2 minutes to respond
            )
            
            if response.status_code == 200:
                answer = response.json().get('response', 'No response received')
            else:
                answer = f"Error: Ollama returned status {response.status_code}"
            
            print("\n")
            print(f"Answer:\n{answer}\n")
        
        except requests.exceptions.Timeout:
            print("\nError: Ollama took too long to respond (timeout after 2 minutes)")
            print("Try with a smaller model like 'neural-chat' instead of 'mistral'\n")
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
