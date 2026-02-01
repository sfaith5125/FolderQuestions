# Model Selection & Preference

## How the App Chooses Which Model to Use

Both `DocumentQA_GUI.py` and `DocumentQA.py` now use intelligent model selection:

### **Priority Order**
1. **openchat** (3.5B) - If available, always use this ⚡ FASTEST
2. **mistral** (7B) - If openchat not available, use this
3. **Any other model** - If neither openchat nor mistral available

### **Code Implementation**

```python
# Get list of available models
model_names = [m['name'] for m in models]

# Prefer openchat, then mistral, then first available
if 'openchat' in model_names:
    ollama_model = 'openchat'
elif 'mistral' in model_names:
    ollama_model = 'mistral'
else:
    ollama_model = model_names[0]

print(f"Using model: {ollama_model}")
```

## **To Ensure openchat is Used**

### **Method 1: Keep Only openchat (Recommended)**

```powershell
# Remove other models
ollama rm mistral
ollama rm neural-chat
ollama rm llama2
ollama list  # Should only show openchat
```

Then restart DocumentQA - it will use openchat automatically.

### **Method 2: Install openchat (If Not Already Done)**

```powershell
# Pull openchat
ollama pull openchat

# Verify it's installed
ollama list

# Restart DocumentQA
# App will automatically prefer openchat over other models
```

### **Method 3: Remove All Models and Keep Only What You Want**

```powershell
# See what you have
ollama list

# Remove everything except openchat
ollama rm mistral
ollama rm neural-chat
ollama rm llama2

# Verify
ollama list
```

## **What Happens at Startup**

When you run `DocumentQA_GUI.py` or `DocumentQA.py`:

1. ✅ Connects to Ollama
2. ✅ Gets list of installed models
3. ✅ Checks if **openchat** is available
4. ✅ If yes → uses **openchat**
5. ✅ If no → checks for **mistral**
6. ✅ If no → uses **first available model**
7. ✅ Shows selected model in status bar

**Status bar example:**
```
✓ Ollama connected - Using model: openchat
```

## **Verifying Your Setup**

### **Check Installed Models**
```powershell
ollama list
```

**Expected output (if you want only openchat):**
```
NAME            ID              SIZE    MODIFIED
openchat        a14b74836b8e    3.5GB   2 minutes ago
```

### **Verify the App Detects openchat**

1. Open `DocumentQA_GUI.py`
2. Look at the status bar at the top
3. Should show: `✓ Ollama connected - Using model: openchat`

## **Model Details**

### **openchat (Recommended)**
- **Size:** 3.5B parameters, 2GB RAM
- **Speed:** ⚡⚡⚡ Very fast (8-15 seconds per query)
- **Quality:** Good
- **Best for:** Speed, low resource usage
- **Trade-off:** Slightly shorter answers

### **mistral (Fallback)**
- **Size:** 7B parameters, 5GB RAM
- **Speed:** ⚡⚡ Fast (15-30 seconds per query)
- **Quality:** Good
- **Best for:** Balanced speed/quality
- **Trade-off:** Slightly slower than openchat

## **Quick Setup**

```powershell
# 1. Stop any running DocumentQA
# (Close the GUI window)

# 2. Pull openchat if not already installed
ollama pull openchat

# 3. Verify installation
ollama list

# 4. Restart DocumentQA
python DocumentQA_GUI.py

# 5. Check status bar shows "Using model: openchat"
```

## **Troubleshooting**

### **Status bar shows wrong model**

The app remembers which model list it retrieved. Try:

```powershell
# Restart Ollama
# 1. Kill ollama serve process
# 2. Run: ollama serve
# 3. Restart DocumentQA
```

### **openchat not detected even though it's installed**

```powershell
# Verify it's actually installed
ollama list

# Verify it has a model ID (not corrupted)
ollama show openchat

# If issues, remove and reinstall
ollama rm openchat
ollama pull openchat
```

## **Advanced: Manual Model Selection**

If you want to force a specific model, you can edit the code:

**In `DocumentQA_GUI.py` around line 78:**
```python
# Force use of specific model
self.ollama_model = 'openchat'  # Change this line
```

**In `DocumentQA.py` around line 170:**
```python
# Force use of specific model
ollama_model = 'openchat'  # Change this line
```

Then restart the app. It will use that model regardless of what's available.

## **Summary**

✅ **Default behavior:** Prefers openchat, falls back to mistral
✅ **To ensure openchat:** Install it with `ollama pull openchat`
✅ **To verify:** Check status bar on app startup
✅ **To force openchat only:** Remove other models with `ollama rm <model>`

**Recommended setup:**
```powershell
ollama pull openchat
ollama list  # Verify openchat is there
python DocumentQA_GUI.py  # Status bar should show "Using model: openchat"
```
