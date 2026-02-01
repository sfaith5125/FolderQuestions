# Ollama Setup Guide - Local LLM for DocumentQA

## Overview

This guide explains how to set up and use **Ollama** with DocumentQA for complete data privacy. Ollama runs large language models locally on your computer with **zero data sent to cloud services**.

## Why Ollama?

✅ **Privacy**: 100% of your data stays on your machine
✅ **Cost**: No API charges
✅ **Control**: You choose which model to use
✅ **Speed**: No internet latency
✅ **Offline**: Works without internet connection
❌ **Tradeoff**: Slower responses than cloud APIs (but still usable)

## Installation

### Windows

1. **Download Ollama**
   - Go to https://ollama.ai
   - Click "Download for Windows"
   - Run the installer
   - Accept defaults and complete installation

2. **Verify Installation**
   ```powershell
   ollama --version
   ```

3. **Start Ollama Service**
   - Ollama should start automatically after installation
   - You should see Ollama icon in system tray
   - Or manually start with: `ollama serve`

### Mac

```bash
# Download from https://ollama.ai
# Or use Homebrew:
brew install ollama

# Start Ollama:
ollama serve
```

### Linux

```bash
curl https://ollama.ai/install.sh | sh

# Start Ollama:
ollama serve
```

## Pulling Models

Once Ollama is running, pull a model. Open a new terminal/PowerShell:

```powershell
ollama pull mistral
```

### Available Models (Recommended for DocumentQA)

| Model | Size | Speed | Quality | Memory | Use Case |
|-------|------|-------|---------|--------|----------|
| **mistral** (recommended) | 7B | ⚡⚡ Fast | Good | 5GB | General Q&A, best all-around |
| **neural-chat** | 7B | ⚡⚡ Fast | Good | 5GB | Conversational, friendly |
| **llama2** | 7B | ⚡⚡ Fast | Good | 5GB | General purpose |
| **dolphin-mixtral** | 46B | 🐢 Slow | Excellent | 28GB | Complex questions, very detailed |
| **openchat** | 7B | ⚡⚡⚡ Very Fast | Good | 4GB | Budget/low-resource option |
| **orca-mini** | 3B | ⚡⚡⚡ Very Fast | Fair | 2GB | Minimal resources |

**Recommendation**: Start with **mistral** - good balance of speed and quality.

### Pull a Model

```powershell
# Most popular choice:
ollama pull mistral

# Or try alternatives:
ollama pull neural-chat
ollama pull llama2
ollama pull dolphin-mixtral
```

### List Installed Models

```powershell
ollama list
```

### Remove a Model

```powershell
ollama rm mistral
```

## Verify Ollama is Running

```powershell
# Should return model list
curl http://localhost:11434/api/tags

# Test with a prompt:
curl -X POST http://localhost:11434/api/generate `
  -H "Content-Type: application/json" `
  -d '{"model":"mistral","prompt":"Hello, how are you?"}'
```

## Install DocumentQA Dependencies

```powershell
cd C:\Users\sfaith\Dev\FolderQuestions
pip install -r requirements.txt
```

## Run DocumentQA with Ollama

### GUI Version

```powershell
python DocumentQA_GUI.py
```

The application will:
1. ✅ Automatically detect Ollama running
2. ✅ Load available models
3. ✅ Show which model is in use
4. Load your documents
5. Answer questions locally (no cloud calls)

### CLI Version

```powershell
python DocumentQA.py [folder_path]
```

For example:
```powershell
python DocumentQA.py ./documents
```

## Performance Tips

### For Faster Responses

1. **Use a smaller model**
   ```powershell
   ollama pull neural-chat
   # Or
   ollama pull openchat
   ```

2. **Use GPU acceleration** (if you have NVIDIA/AMD GPU)
   - Ollama automatically uses GPU if available
   - Check if it's working: `ollama --version`
   - For manual GPU config, see Ollama docs

3. **Close other applications**
   - Free up RAM for Ollama
   - 8GB+ recommended

4. **Use shorter documents**
   - Load smaller document sets
   - Ask more specific questions

### For Better Answers

1. **Use a larger model**
   ```powershell
   ollama pull dolphin-mixtral
   # Or
   ollama pull neural-chat
   ```

2. **Provide more context**
   - Load all relevant documents
   - Ask specific multi-part questions

3. **Adjust temperature in code**
   - Lower (0.3): More focused, deterministic answers
   - Higher (0.9): More creative, varied answers
   - Default (0.7): Good balance

## Troubleshooting

### Issue: "Connection refused" error

**Solution:**
```powershell
# Make sure Ollama is running:
ollama serve

# Or check if it's running:
netstat -an | findstr 11434

# If Ollama crashed, restart it
```

### Issue: "No models found"

**Solution:**
```powershell
# Pull a model:
ollama pull mistral

# List models:
ollama list
```

### Issue: Slow responses (taking 30+ seconds)

**Causes & Solutions:**

1. **Using large model on weak computer**
   ```powershell
   ollama pull neural-chat  # Smaller, faster
   ```

2. **No GPU acceleration**
   - Check if Ollama is using GPU (see console output)
   - Some systems don't support GPU acceleration
   - CPU-only is fine, just slower

3. **Not enough RAM**
   - 8GB minimum recommended
   - Close other applications
   - Use smaller model (mistral instead of dolphin-mixtral)

### Issue: Out of Memory error

**Solution:**
```powershell
# Use a smaller model:
ollama pull openchat      # 4GB
# Instead of:
ollama rm dolphin-mixtral # 28GB
```

### Issue: "Ollama took too long to respond (timeout)"

**Solution:**
1. Model is too large for your hardware
   ```powershell
   ollama pull neural-chat  # Switch to smaller model
   ```

2. Increase timeout in code:
   - In `DocumentQA_GUI.py`, find: `timeout=120`
   - Change to: `timeout=300` (5 minutes)

3. Close other applications to free RAM

## Model Comparison for Your Use Case

### Fast Responses (< 5 seconds)
```powershell
ollama pull neural-chat    # Balanced, conversational
ollama pull openchat       # Very fast
```

### Better Quality Answers (< 30 seconds)
```powershell
ollama pull mistral        # Good balance (recommended)
ollama pull llama2         # General purpose
```

### Excellent Quality (1-2 minutes per response)
```powershell
ollama pull dolphin-mixtral  # Best quality
```

## System Requirements by Model

| Model | RAM | VRAM | Storage |
|-------|-----|------|---------|
| openchat (3B) | 4GB | - | 2GB |
| neural-chat (7B) | 5GB | - | 5GB |
| mistral (7B) | 6GB | - | 5GB |
| llama2 (7B) | 6GB | - | 4GB |
| dolphin-mixtral (46B) | 32GB | 8GB | 28GB |

**Recommendation for most users**: mistral with 8GB+ RAM

## Advanced Configuration

### Custom Ollama Port

By default, Ollama runs on `http://localhost:11434`

If you need to change it, edit DocumentQA files and find:
```python
self.ollama_url = "http://localhost:11434"
```

Change to your desired port.

### Memory/Context Settings

To improve answer quality for long documents:

In `DocumentQA_GUI.py`, find the Ollama API call and modify:
```python
response = requests.post(
    f"{self.ollama_url}/api/generate",
    json={
        "model": self.ollama_model,
        "prompt": full_prompt,
        "stream": False,
        "temperature": 0.7,
        "top_p": 0.9,              # Add this
        "num_ctx": 4096,           # Context window size
        "num_predict": 512,        # Max response length
    },
    timeout=120
)
```

### Use Streaming for Real-Time Responses

For a more interactive feel, enable streaming (shows response as it's generated):

Change `"stream": False,` to `"stream": True,` in the API call.

This requires different response parsing. See Ollama API docs.

## Running Both Ollama and DocumentQA

### Setup:

**Terminal 1** - Start Ollama (keep this running):
```powershell
ollama serve
```

**Terminal 2** - Run DocumentQA:
```powershell
cd C:\Users\sfaith\Dev\FolderQuestions
python DocumentQA_GUI.py
```

Or for CLI:
```powershell
python DocumentQA.py ./documents
```

## Performance Expectations

### Response Times

| Model | Hardware | Time Per Question |
|-------|----------|-------------------|
| mistral | CPU only | 20-60 seconds |
| mistral | GPU (NVIDIA RTX 3090) | 5-15 seconds |
| neural-chat | CPU only | 15-30 seconds |
| neural-chat | GPU | 3-8 seconds |
| dolphin-mixtral | GPU (A100) | 30-90 seconds |

Your actual times depend on:
- Document size and complexity
- Question complexity
- Hardware specs
- Model size

## Switching Models Dynamically

Edit the code to let users select models:

In `DocumentQA_GUI.py`, modify `_check_api_key()`:
```python
# Show dropdown of available models instead of auto-selecting first
# This allows users to switch models without restarting
```

## Comparison: Google Gemini vs Ollama

| Aspect | Google Gemini | Ollama (Local) |
|--------|---------------|----------------|
| **Privacy** | Cloud (risky) | Local (safe) |
| **Cost** | Free (for now) | Free (one-time) |
| **Speed** | 2-5 seconds | 15-60 seconds |
| **Quality** | Excellent | Good-Excellent |
| **Data Capture** | Yes | No |
| **Internet Needed** | Yes | No |
| **Setup** | API key only | Install + model |
| **Compliance** | Standard | HIPAA-safe |

## Next Steps

1. **Install Ollama**: https://ollama.ai
2. **Pull a model**: `ollama pull mistral`
3. **Run DocumentQA**: `python DocumentQA_GUI.py`
4. **Load documents** and ask questions
5. **Enjoy complete privacy!**

## Resources

- **Ollama Official**: https://ollama.ai
- **Ollama GitHub**: https://github.com/ollama/ollama
- **Model Library**: https://ollama.ai/library
- **API Documentation**: https://github.com/ollama/ollama/blob/main/docs/api.md

## FAQ

**Q: Is Ollama secure?**
A: Yes, it runs locally on your machine. No data leaves unless you explicitly send it.

**Q: Can I use Ollama without internet?**
A: Yes, once models are downloaded, Ollama works completely offline.

**Q: Will Ollama slow down my computer?**
A: It uses significant RAM while running. Close it when not in use.

**Q: Can I run multiple models simultaneously?**
A: Only one model can run at a time to preserve RAM.

**Q: How do I uninstall Ollama?**
A: Windows: Add/Remove Programs → Ollama
   Mac: `rm -rf ~/.ollama` and uninstall app
   Linux: Follow distribution's package manager

**Q: Can I improve answer quality?**
A: Yes, use `dolphin-mixtral` model for better answers (requires more resources).

---

**You now have complete data privacy with Ollama! 🎉**
