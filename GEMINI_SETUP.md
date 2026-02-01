# Google Gemini API Setup Guide

## Overview

This application now uses Google's **Gemini 2.5 Flash** model via the new `google-genai` package (the old `google-generativeai` package has been deprecated).

## Step 1: Get Your Free Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"** button
3. Select or create a Google Cloud project
4. Your API key will be generated (looks like: `AIza...`)
5. Copy the API key

## Step 2: Set the Environment Variable

### Option A: Set it temporarily in PowerShell (current session only)

Run this command in PowerShell:

```powershell
$env:GOOGLE_API_KEY = 'your-api-key-here'
```

Replace `'your-api-key-here'` with your actual API key from Step 1.

Then run the application:
```powershell
python DocumentQA_GUI.py
```

### Option B: Set it permanently in Windows (persistent across sessions)

1. Press **Win + X** and select **System**
2. Click **Advanced system settings** on the left
3. Click **Environment Variables** button at the bottom
4. Under "User variables", click **New**
5. Fill in:
   - Variable name: `GOOGLE_API_KEY`
   - Variable value: `your-api-key-here` (paste your actual key)
6. Click **OK** three times to save

**Note:** After setting a permanent environment variable, you need to restart PowerShell or any open applications for the change to take effect.

## Step 3: Verify Your Setup

Before running the application, verify the API key is set:

```powershell
$env:GOOGLE_API_KEY
```

If it's set correctly, you'll see your API key displayed. If it's empty, you haven't set it yet.

## Step 4: Install Dependencies

Make sure you have the required Python packages installed:

```powershell
pip install -r requirements.txt
```

This installs:
- `google-genai` - Google's new Generative AI library (replaces deprecated google-generativeai)
- `PyPDF2` - For PDF parsing
- `python-docx` - For Word document parsing
- `scikit-learn` - For semantic search
- `numpy` - For numerical operations

If you have the old `google-generativeai` package installed, you can uninstall it:
```powershell
pip uninstall google-generativeai
```

## Step 5: Run the Application

### GUI Version:
```powershell
python DocumentQA_GUI.py
```

### CLI Version:
```powershell
python DocumentQA.py [folder_path]
```

## Model Information

- **Model**: `gemini-2.5-flash`
- **Library**: `google-genai` (new, active development)
- **Performance**: Fast inference, good for Q&A tasks
- **Cost**: Free tier with 15 requests per minute limit

## Free Tier Limits

Google's free Gemini API tier includes:
- **15 requests per minute**
- No credit card required
- Unlimited requests (within the rate limit)
- Access to all available Gemini models including Gemini 2.5

## Troubleshooting

### Error: "GOOGLE_API_KEY not set"
- Make sure you've set the environment variable correctly
- Restart PowerShell after setting it
- Check that your API key is pasted correctly (no extra spaces)

### Error: "API quota exceeded"
- You've hit the 15 requests per minute limit
- Wait a minute and try again

### Error: "Invalid API key"
- Your API key is incorrect or expired
- Go back to [Google AI Studio](https://aistudio.google.com/app/apikey) and regenerate it

### "No module named 'google.genai'"
- Make sure you've installed the new package: `pip install google-genai`
- Remove the old deprecated package: `pip uninstall google-generativeai`

## What Changed?

The application has been updated to use Google's newer Gemini API:
- **Old library**: `google-generativeai` (deprecated, no longer maintained)
- **New library**: `google-genai` (current, actively maintained)
- **Model**: `gemini-2.5-flash` (latest, faster, more capable)
- **Environment variable**: `GOOGLE_API_KEY` (same as before)

All functionality remains the same - document loading, RAG search, and Q&A work exactly as before, just with the newer, better Gemini model!
