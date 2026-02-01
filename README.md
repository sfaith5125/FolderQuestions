# FolderQuestions - Interactive Document Q&A with Local LLMs

An interactive Python app that lets you drop documents into a folder and ask questions about them using **local Ollama models** with RAG (Retrieval-Augmented Generation). Complete data privacy - all processing stays on your computer.

## 🌳 Branch Structure

This project has **two branches** for different deployment approaches:

### 📍 **main** - Local Ollama (Private, Recommended Default)
- Uses **Local Ollama** with models like Mistral, Llama2, Neural-Chat
- ✅ **100% data privacy** (stays on your computer)
- ✅ No API costs
- ✅ Works offline
- ✅ No compliance concerns
- ⚠️ Slower responses (15-60 seconds)
- 📦 Requires Ollama installation + 6GB+ RAM

**Use this if:**
- Your documents are sensitive/proprietary
- You need complete data privacy
- You want zero cloud processing
- Cost is a concern
- You have compliance requirements (HIPAA, GDPR, etc.)
- **This is the recommended default branch**

### 🌐 **feature/google-gemini-api** - Cloud-Based Alternative
- Uses **Google Gemini 2.5 Flash** API
- ✅ Fast responses (2-5 seconds)
- ✅ Excellent answer quality
- ✅ No local resources needed
- ⚠️ Data sent to Google's servers
- 💰 Free tier (15 requests/min) or paid plan

**Use this if:**
- Your documents are non-sensitive
- You want fast, high-quality answers
- You don't mind cloud processing
- Easy setup is priority

## Features (Both Versions)

- **Multi-format support**: PDF, DOCX, and TXT files
- **Recursive folder scanning**: Automatically loads all documents from a folder and subfolders
- **RAG (Retrieval-Augmented Generation)**: Semantic search using TF-IDF to find relevant document chunks
- **Smart Context Retrieval**: Shows which documents were used to answer your question
- **Interactive Q&A**: Ask natural language questions and get answers based on document content
- **Document Listing**: See all loaded documents with their sources
- **GUI Interface**: Browse folders, ask questions, view retrieved context
- **CLI Interface**: Command-line version for scripting/batch processing
- **Threading**: Non-blocking UI - operations run in background threads
- **Advanced RAG Tuning**: Configurable chunk size, overlap, and retrieval parameters

## Two Versions Available

- **DocumentQA_GUI.py** (Recommended) - GUI version with folder browser, interactive Q&A, and RAG-based semantic search
- **DocumentQA.py** - CLI version for command-line use

## Installation Instructions

### For Local Ollama (main branch - RECOMMENDED)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Ollama:
   - Download from https://ollama.ai
   - Run installer and complete setup

3. Pull a model:
```bash
ollama pull mistral
# Or try: neural-chat, llama2, dolphin-mixtral
```

4. Start Ollama (in one terminal):
```bash
ollama serve
```

5. Run DocumentQA (in another terminal):
```bash
python DocumentQA_GUI.py
```

**See `OLLAMA_SETUP.md` for detailed Ollama setup and troubleshooting**

### For Google Gemini (feature/google-gemini-api branch)

1. Checkout the branch:
```bash
git checkout feature/google-gemini-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Get a Google Gemini API key:
   - Visit https://aistudio.google.com/app/apikey
   - Click "Create API Key"
   - Copy your key

4. Set environment variable:
```powershell
# PowerShell (Windows)
$env:GOOGLE_API_KEY = 'your-api-key-here'

# Or permanently in Windows:
# Settings → System → Environment Variables → New User Variable
# Name: GOOGLE_API_KEY
# Value: your-api-key-here
```

5. Run the application:
```bash
python DocumentQA_GUI.py
```

**See `GEMINI_SETUP.md` for detailed Google Gemini setup**

## Quick Start

### Default (Ollama Local - Recommended)
```bash
# Already on main branch with Ollama
pip install -r requirements.txt
ollama pull mistral
# (in new terminal) ollama serve
# (back to original terminal)
python DocumentQA_GUI.py
```

### Alternative: Google Gemini
```bash
git checkout feature/google-gemini-api
pip install -r requirements.txt
# Set GOOGLE_API_KEY environment variable
python DocumentQA_GUI.py
```

## Documentation

- **`OLLAMA_SETUP.md`** - Complete setup guide for local Ollama models (main branch)
- **`GEMINI_SETUP.md`** - Complete setup guide for Google Gemini API (feature/google-gemini-api)
- **`ANSWER_QUALITY_TUNING.md`** - How to improve answer quality and performance
- **`DATA_PRIVACY_GUIDE.md`** - Data privacy analysis and considerations
- **`BRANCH_STRUCTURE.md`** - How to manage and switch between branches

## API & Technology

### Main Branch (Ollama Local)
- Uses: Local Ollama HTTP API at `localhost:11434`
- Models: Mistral, Llama2, Neural-Chat, Dolphin-Mixtral, etc.
- Cost: None (local processing)
- Data: Stays on your computer

### feature/google-gemini-api Branch
- Uses: Google's cloud API
- Models: Google Gemini 2.5 Flash
- Cost: Free tier (15 req/min) or paid plan
- Data: Sent to Google servers

## Comparison Table

| Feature | Gemini | Ollama |
|---------|--------|--------|
| **Speed** | ⚡⚡⚡ 2-5s | ⚡ 15-60s |
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Privacy** | Cloud | Local |
| **Cost** | Free/Paid | Free |
| **Setup** | API key | Install Ollama |
| **Offline** | ❌ | ✅ |
| **RAM Needed** | Minimal | 6GB+ |
| **Compliance** | Standard | HIPAA-safe |

## Hardware Requirements

### Google Gemini Version
- **Minimum**: 2GB RAM, internet connection
- **Recommended**: 4GB RAM, good internet
- Works on: Windows, Mac, Linux

### Ollama Version
- **Minimum**: 6GB RAM, local storage
- **Recommended**: 16GB RAM, GPU (NVIDIA/AMD)
- **Models**:
  - Mistral (7B): 5GB RAM
  - Neural-Chat (7B): 5GB RAM
  - Dolphin-Mixtral (46B): 28GB RAM
- Works on: Windows, Mac, Linux

## Troubleshooting

### Gemini Version
- See `GEMINI_SETUP.md` troubleshooting section
- API key not set error: Check environment variable
- 404 model error: Model not available on your account tier

### Ollama Version
- See `OLLAMA_SETUP.md` troubleshooting section
- Connection refused: Make sure `ollama serve` is running
- Out of memory: Use smaller model (neural-chat instead of dolphin-mixtral)
- Slow responses: Increase timeout or use GPU acceleration

## Main Branch (main)

The `main` branch contains the latest Google Gemini version with all improvements. Both feature branches are kept up-to-date with any enhancements to core RAG functionality.

## Switching Between Versions

```bash
# See both branches
git branch -a

# Switch to Google Gemini
git checkout feature/google-gemini-api

# Switch to Ollama
git checkout feature/ollama-local-llm

# Switch back to main
git checkout main
```

## Performance Tips

### For Google Gemini
1. Increase retrieved chunks in code (currently 10)
2. Use larger context in system prompt
3. Ask specific questions for better answers

### For Ollama
1. Use smaller models for faster responses (neural-chat, openchat)
2. Use larger models for better quality (dolphin-mixtral)
3. Ensure GPU acceleration is enabled
4. Close other applications to free RAM
5. Reduce document size/complexity

## License

MIT

## Contributing

Feel free to fork and submit pull requests for improvements!

---

**Choose your version and enjoy private, powerful document Q&A! 🚀**
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
