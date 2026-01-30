"""DocumentQA GUI with RAG

Interactive GUI-based Q&A system that loads documents from a folder and answers questions
using Claude with RAG (Retrieval-Augmented Generation) for smarter searching.

Features:
- GUI folder browser for document selection
- Recursive document loading (PDF, DOCX, TXT)
- Semantic search using embeddings
- RAG-based answers using Claude Haiku
- Conversation history

Usage: python DocumentQA_GUI.py

Requires: anthropic, PyPDF2, python-docx, scikit-learn
Install: pip install anthropic PyPDF2 python-docx scikit-learn
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import threading

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, scrolledtext, messagebox
    import anthropic
    from PyPDF2 import PdfReader
    from docx import Document as DocxDocument
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    import numpy as np
except ImportError as e:
    print(f"Import error: {e}")
    print("Please install required packages:")
    print("  pip install anthropic PyPDF2 python-docx scikit-learn")
    sys.exit(1)


class DocumentQAGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DocumentQA - Interactive Document Q&A")
        self.root.geometry("1000x700")
        
        self.documents = {}  # {file_path: text}
        self.document_chunks = {}  # {doc_id: [(chunk_text, start_idx, end_idx), ...]}
        self.vectorizer = None
        self.tfidf_matrix = None
        self.all_chunks = []  # flat list of chunks for searching
        self.chunk_to_doc = {}  # {chunk_idx: doc_name}
        
        self.client = None
        
        self._setup_ui()
        self._check_api_key()
    
    def _check_api_key(self):
        """Check if ANTHROPIC_API_KEY is set."""
        if not os.getenv('ANTHROPIC_API_KEY'):
            messagebox.showwarning(
                "API Key Missing",
                "ANTHROPIC_API_KEY not set.\n\n"
                "Please set the environment variable:\n"
                "  $env:ANTHROPIC_API_KEY = 'sk-ant-...'"
            )
        else:
            try:
                self.client = anthropic.Anthropic()
            except Exception as e:
                messagebox.showerror("API Error", f"Failed to initialize Anthropic client: {e}")
    
    def _setup_ui(self):
        """Setup the GUI layout."""
        # Top frame: Folder selection
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(top_frame, text="Document Folder:").pack(side=tk.LEFT)
        self.folder_var = tk.StringVar(value="./documents")
        ttk.Entry(top_frame, textvariable=self.folder_var, width=50).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Browse", command=self._browse_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="Load Documents", command=self._load_documents_async).pack(side=tk.LEFT, padx=2)
        
        # Status label
        self.status_var = tk.StringVar(value="No documents loaded")
        ttk.Label(top_frame, textvariable=self.status_var, foreground="blue").pack(side=tk.LEFT, padx=10)
        
        # Middle frame: Q&A input
        middle_frame = ttk.LabelFrame(self.root, text="Ask a Question", padding=10)
        middle_frame.pack(fill=tk.BOTH, padx=10, pady=5)
        
        ttk.Label(middle_frame, text="Question:").pack(anchor=tk.W)
        
        button_frame = ttk.Frame(middle_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.question_entry = ttk.Entry(button_frame, width=70)
        self.question_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.question_entry.bind("<Return>", lambda e: self._ask_question_async())
        
        ttk.Button(button_frame, text="Ask", command=self._ask_question_async).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Clear", command=self._clear_output).pack(side=tk.LEFT, padx=2)
        
        # Lower frame: Answer display
        lower_frame = ttk.LabelFrame(self.root, text="Answer & Retrieved Context", padding=10)
        lower_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(
            lower_frame, wrap=tk.WORD, height=20, width=120
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Bottom frame: Info
        bottom_frame = ttk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.info_var = tk.StringVar(value="Ready")
        ttk.Label(bottom_frame, textvariable=self.info_var, foreground="green").pack(side=tk.LEFT)
    
    def _browse_folder(self):
        """Open folder browser dialog."""
        folder = filedialog.askdirectory(title="Select Documents Folder")
        if folder:
            self.folder_var.set(folder)
    
    def _load_documents_async(self):
        """Load documents in a separate thread to avoid freezing UI."""
        thread = threading.Thread(target=self._load_documents, daemon=True)
        thread.start()
    
    def _load_documents(self):
        """Load all documents from the folder and build RAG index."""
        folder_path = self.folder_var.get()
        self.status_var.set("Loading documents...")
        self.root.update()
        
        self.documents = {}
        self.all_chunks = []
        self.chunk_to_doc = {}
        
        supported_extensions = {'.pdf', '.txt', '.docx'}
        folder_path = Path(folder_path)
        
        if not folder_path.exists():
            self.status_var.set(f"Folder not found: {folder_path}")
            messagebox.showerror("Error", f"Folder not found: {folder_path}")
            return
        
        # Extract text from all documents
        for file_path in folder_path.rglob('*'):
            if file_path.is_file():
                ext = file_path.suffix.lower()
                if ext not in supported_extensions:
                    continue
                
                text = None
                if ext == '.pdf':
                    text = self._extract_text_from_pdf(file_path)
                elif ext == '.docx':
                    text = self._extract_text_from_docx(file_path)
                elif ext == '.txt':
                    text = self._extract_text_from_txt(file_path)
                
                if text:
                    self.documents[str(file_path)] = text
        
        # Build RAG index from chunks
        self._build_rag_index()
        
        doc_count = len(self.documents)
        chunk_count = len(self.all_chunks)
        self.status_var.set(f"✓ Loaded {doc_count} document(s), {chunk_count} chunk(s)")
        self.info_var.set(f"Ready. {doc_count} documents indexed with RAG.")
        self.output_text.insert(tk.END, f"Loaded {doc_count} documents with {chunk_count} searchable chunks.\n\n")
    
    def _extract_text_from_pdf(self, file_path):
        """Extract text from PDF."""
        try:
            text = []
            with open(file_path, 'rb') as f:
                reader = PdfReader(f)
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text.append(page_text)
            return "\n\n".join(text)
        except Exception as e:
            print(f"Error extracting PDF {file_path}: {e}")
            return ""
    
    def _extract_text_from_docx(self, file_path):
        """Extract text from DOCX."""
        try:
            doc = DocxDocument(file_path)
            paragraphs = [para.text for para in doc.paragraphs if para.text.strip()]
            return "\n".join(paragraphs)
        except Exception as e:
            print(f"Error extracting DOCX {file_path}: {e}")
            return ""
    
    def _extract_text_from_txt(self, file_path):
        """Extract text from TXT."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading TXT {file_path}: {e}")
            return ""
    
    def _build_rag_index(self):
        """
        Build a searchable index by chunking documents and computing embeddings.
        Uses TF-IDF vectorization for semantic search.
        """
        self.all_chunks = []
        self.chunk_to_doc = {}
        
        chunk_size = 500  # characters per chunk
        overlap = 50  # character overlap between chunks
        
        for doc_name, doc_text in self.documents.items():
            doc_short_name = Path(doc_name).name
            
            # Split into chunks
            chunks = []
            for i in range(0, len(doc_text), chunk_size - overlap):
                chunk = doc_text[i:i + chunk_size]
                if chunk.strip():
                    chunks.append(chunk)
            
            # Add to global list
            for chunk in chunks:
                chunk_idx = len(self.all_chunks)
                self.all_chunks.append(chunk)
                self.chunk_to_doc[chunk_idx] = doc_short_name
        
        # Build TF-IDF vectorizer
        if self.all_chunks:
            try:
                self.vectorizer = TfidfVectorizer(max_features=500, stop_words='english')
                self.tfidf_matrix = self.vectorizer.fit_transform(self.all_chunks)
            except Exception as e:
                print(f"Error building TF-IDF index: {e}")
    
    def _retrieve_relevant_chunks(self, query: str, top_k: int = 5) -> List[Tuple[str, str]]:
        """
        Retrieve the most relevant chunks for a query using TF-IDF similarity.
        Returns: [(chunk_text, source_doc_name), ...]
        """
        if not self.vectorizer or not self.all_chunks:
            return []
        
        try:
            query_vec = self.vectorizer.transform([query])
            similarities = cosine_similarity(query_vec, self.tfidf_matrix)[0]
            
            # Get top-k indices
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.0:
                    chunk = self.all_chunks[idx]
                    doc_name = self.chunk_to_doc.get(idx, "Unknown")
                    results.append((chunk, doc_name))
            
            return results
        except Exception as e:
            print(f"Error retrieving chunks: {e}")
            return []
    
    def _ask_question_async(self):
        """Ask question in a separate thread."""
        thread = threading.Thread(target=self._ask_question, daemon=True)
        thread.start()
    
    def _ask_question(self):
        """Ask a question using RAG."""
        if not self.documents:
            messagebox.showwarning("No Documents", "Please load documents first.")
            return
        
        if not self.client:
            messagebox.showerror("API Error", "Anthropic client not initialized. Check your API key.")
            return
        
        question = self.question_entry.get().strip()
        if not question:
            messagebox.showwarning("No Question", "Please enter a question.")
            return
        
        self.info_var.set("Searching and thinking...")
        self.root.update()
        
        # Retrieve relevant chunks using RAG
        relevant_chunks = self._retrieve_relevant_chunks(question, top_k=5)
        
        if not relevant_chunks:
            self.output_text.insert(tk.END, f"Q: {question}\n\n")
            self.output_text.insert(tk.END, "A: No relevant information found in documents.\n\n")
            self.info_var.set("Ready")
            return
        
        # Build context from retrieved chunks
        context = "\n\n---\n\n".join([
            f"[From: {doc}]\n{chunk}" for chunk, doc in relevant_chunks
        ])
        
        # Build system prompt with retrieved context
        system_prompt = f"""You are a helpful assistant that answers questions based on the following document excerpts:

{context}

Please answer the user's question based on the provided context. If the information is not in the provided excerpts, 
say so explicitly. Be concise and accurate. Cite which document(s) you're referencing."""
        
        try:
            # Call Claude Haiku with RAG context
            message = self.client.messages.create(
                model="claude-3-5-haiku-20241022",
                max_tokens=1024,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": question}
                ]
            )
            
            answer = message.content[0].text
            
            # Display in UI
            self.output_text.insert(tk.END, f"Q: {question}\n\n")
            self.output_text.insert(tk.END, "Retrieved Context:\n")
            for i, (chunk, doc) in enumerate(relevant_chunks, 1):
                preview = chunk[:200].replace('\n', ' ')
                self.output_text.insert(tk.END, f"  {i}. [{doc}] {preview}...\n")
            self.output_text.insert(tk.END, "\nA: " + answer + "\n\n")
            self.output_text.insert(tk.END, "=" * 80 + "\n\n")
            self.output_text.see(tk.END)
            
            self.question_entry.delete(0, tk.END)
            self.info_var.set("Ready")
        
        except anthropic.APIError as e:
            self.output_text.insert(tk.END, f"API Error: {e}\n\n")
            self.info_var.set("API Error")
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {e}\n\n")
            self.info_var.set("Error")
    
    def _clear_output(self):
        """Clear the output text area."""
        self.output_text.delete(1.0, tk.END)


def main():
    root = tk.Tk()
    app = DocumentQAGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
