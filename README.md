# FolderQuestions - Interactive Document Q&A with Claude Haiku

An interactive Python app that lets you drop documents into a folder and ask questions about them using Claude Haiku with RAG (Retrieval-Augmented Generation).

## Two Versions Available

- **DocumentQA_GUI.py** (Recommended) - GUI version with folder browser, interactive Q&A, and RAG-based semantic search
- **DocumentQA.py** - CLI version for command-line use

## Features

- **Multi-format support**: PDF, DOCX, and TXT files
- **Recursive folder scanning**: Automatically loads all documents from a folder and subfolders
- **RAG (Retrieval-Augmented Generation)**: Semantic search using TF-IDF to find relevant document chunks
- **Smart Context Retrieval**: Shows which documents were used to answer your question
- **Interactive Q&A**: Ask natural language questions and get answers based on document content
- **Claude Haiku 4.5**: Uses Anthropic's fast and efficient Claude Haiku model
- **GUI Interface**: Browse folders, ask questions, view retrieved context
- **Threading**: Non-blocking UI - document loading and queries run in background threads

## Requirements

- Python 3.8+
- Anthropic API key (get one at https://console.anthropic.com)

## Installation

1. Install dependencies:
```bash
pip install anthropic PyPDF2 python-docx scikit-learn numpy
```

Or use the provided requirements file:
```bash
pip install -r requirements.txt
```

2. Set your Anthropic API key as an environment variable:

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "sk-ant-..."
```

**On Windows (Command Prompt):**
```cmd
set ANTHROPIC_API_KEY=sk-ant-...
```

**On macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

## Quick Start - GUI Version (Recommended)

Run the GUI version:
```bash
python DocumentQA_GUI.py
```

Then:
1. Click **Browse** to select your documents folder
2. Click **Load Documents** to scan and index all PDFs, DOCX, and TXT files
3. Type your question in the text field
4. Click **Ask** or press Enter
5. View the answer and the retrieved context chunks

### GUI Features

- **Folder Browser**: Click "Browse" to select any folder on your PC
- **Auto-reload**: Change the folder path and click "Load Documents" to reload
- **Context Display**: See which documents and passages were used to answer your question
- **RAG Search**: Semantic search finds the most relevant passages automatically
- **Conversation History**: View your questions and answers in the output window
- **Status Indicators**: Real-time feedback on loading and processing status

## Quick Start - CLI Version

1. Create a documents folder:
```bash
mkdir documents
```

2. Drop your PDF, DOCX, or TXT files into the folder

3. Run the app:
```bash
python DocumentQA.py
```

Or specify a custom folder:
```bash
python DocumentQA.py /path/to/your/documents
```

4. Type your questions and get answers based on the document content. Type `exit` or `quit` to exit.

## How RAG Works

**RAG (Retrieval-Augmented Generation)** improves answer quality by:

1. **Document Chunking**: Your documents are automatically split into 500-character chunks with 50-character overlap
2. **Semantic Indexing**: Each chunk is indexed using TF-IDF (Term Frequency-Inverse Document Frequency) vectorization
3. **Similarity Search**: When you ask a question, the app finds the 5 most relevant chunks using cosine similarity
4. **Context-Aware Answers**: Only the relevant chunks are sent to Claude, reducing hallucinations and improving accuracy
5. **Source Tracking**: The app shows you which documents were used to answer your question

This approach means:
- ✓ Faster responses (only relevant context sent to Claude)
- ✓ More accurate answers (Claude sees the actual source material)
- ✓ Transparency (you can see which documents were referenced)
- ✓ Cost-effective (smaller context = fewer tokens)

## Examples

**GUI Version:**
```
Folder: C:\Users\YourName\Documents\Research
Documents loaded: 3 documents, 15 chunks
Q: What were the quarterly profits?
```
Retrieved Context shows:
- [financial_report.pdf] Q3 showed profits of...
- [quarterly_summary.docx] Year-over-year growth...

A: According to the financial report, Q3 quarterly profits were $2.5M, representing a 12% increase year-over-year...

**CLI Version:**
```
$ python DocumentQA.py ./my_docs
Loaded 3 document(s).
Ask a question about the documents: What are the main risks?
Thinking...
Answer: The main risks identified in the documents include...
```

## Document Format Support

- **PDF**: Text extraction from all pages
- **DOCX**: Extracts paragraphs and text content
- **TXT**: Plain text files

## Notes

- **Token limits**: To avoid hitting API token limits, the app includes the first 3000 characters of each document per question. For very large documents, consider splitting them or using a higher-tier Claude model.
- **API costs**: Each question uses Claude Haiku, which is inexpensive but does incur API costs.
- **Privacy**: Your documents are sent to Anthropic's API. If you have sensitive data, review Anthropic's privacy policy.
- **RAG Search**: TF-IDF is used for semantic search. For more advanced semantic search, consider using embedding-based approaches in the future.

## Troubleshooting

**"No documents found"**: Make sure the folder exists and contains PDF, DOCX, or TXT files.

**"API Error: 401 Unauthorized"**: Check that your `ANTHROPIC_API_KEY` is set correctly.

**"ModuleNotFoundError"**: Install the required packages using the command above.

**GUI doesn't open**: Make sure tkinter is installed (usually included with Python). On Linux, you may need to install it separately: `sudo apt-get install python3-tk`

## Future Enhancements

- Add support for more file types (PPTX, Excel, etc.)
- Implement advanced vector embeddings (OpenAI embeddings, local models)
- Cache document embeddings for faster queries
- Add conversation history/memory
- Support for larger documents with smart chunking
- Export conversation history to file
- Add settings panel for chunk size, top-k results, API model selection
- Implement SQLite storage for persistent conversation history

## License

MIT

## Support

For issues or questions, please check the troubleshooting section or contact support.
