# Answer Quality Tuning Guide

This guide explains how to fine-tune your DocumentQA system for better answer quality.

## Current Optimizations Applied

The following improvements have been automatically applied to your system:

### 1. **Enhanced Chunk Size & Overlap**
- **Chunk Size**: 1000 characters (was 500)
  - Larger chunks preserve more context and relationships between ideas
  - Prevents important information from being split across chunks

- **Chunk Overlap**: 200 characters (was 50)
  - Greater overlap ensures seamless context between chunks
  - Reduces information loss at chunk boundaries

### 2. **Improved TF-IDF Vectorization**
- **Max Features**: 1000 (was 500)
  - Captures more vocabulary for better relevance matching
  
- **N-gram Range**: (1, 2)
  - Matches both single words AND phrases
  - Example: matches both "machine" and "machine learning"

- **Sublinear TF**: Enabled
  - Scales term frequency logarithmically
  - Prevents common terms from dominating

### 3. **Better Chunk Retrieval**
- **Retrieved Chunks**: 10 (was 5)
  - More context for the AI to synthesize from
  
- **Similarity Threshold**: 0.01 minimum
  - Filters out irrelevant chunks while keeping marginal ones

### 4. **Advanced System Prompt**
- Specific instructions for comprehensive, detailed answers
- Explicit requirements for source citations
- Emphasis on quoting/paraphrasing from documents
- Minimum answer length expectations (3-5 paragraphs)
- Clear prohibition on inference or invention

## Further Fine-Tuning Options

### **Option A: For Very Long Documents**
If your documents are very lengthy (100+ pages), try increasing chunk settings:

In `DocumentQA_GUI.py`, find the `_build_rag_index` method:
```python
chunk_size = 1500  # Increase to 1500 for longer documents
overlap = 300      # Increase to 300
```

### **Option B: For Highly Technical Documents**
If your documents are technical (code, specifications, technical papers):

Find the TF-IDF settings and modify:
```python
self.vectorizer = TfidfVectorizer(
    max_features=2000,  # Increase to capture more technical terms
    stop_words='english',
    ngram_range=(1, 3),  # Include trigrams for technical phrases
    min_df=1,
    sublinear_tf=True
)
```

### **Option C: For Conversational/Narrative Documents**
If your documents are narratives or stories:

```python
chunk_size = 800   # Slightly smaller to keep scenes intact
overlap = 150      # Less overlap needed
```

Then increase retrieved chunks:
```python
relevant_chunks = self._retrieve_relevant_chunks(question, top_k=15)
```

### **Option D: Stricter Answer Quality**
For even more detailed, formal answers, modify the system prompt:

Find the system_prompt in `_ask_question` method and change:
```python
ANSWER QUALITY REQUIREMENT: Provide 5-8 substantial paragraphs for most questions, more if needed.
```

Add additional instruction:
```python
13. For any claims, provide supporting evidence with specific quotes
14. Maintain an academic or professional tone
15. Be exhaustively thorough - err on the side of providing too much detail
```

## Testing & Validation

### How to Test Improvements:
1. Run the application with the same test questions you used before
2. Compare answer length and detail
3. Check for proper source citations
4. Verify all aspects of complex questions are addressed

### Questions That Test Answer Quality:
- **Complex Multi-Part Questions**: "What is X and how does it relate to Y? What are the implications?"
- **Comparative Questions**: "Compare X and Y. What are the advantages of each?"
- **Analytical Questions**: "Analyze the evidence for X. What are the strengths and weaknesses?"
- **Synthesis Questions**: "Based on the documents, what can we conclude about X?"

## Performance Considerations

The optimizations increase:
- **Memory Usage**: ~2-3x due to larger context window
- **Retrieval Time**: Slightly slower TF-IDF computation, but still <1 second
- **API Token Usage**: More tokens per request (larger context = higher cost)

If API costs become an issue:
```python
relevant_chunks = self._retrieve_relevant_chunks(question, top_k=7)  # Reduce from 10
```

## Troubleshooting

### Problem: "Answers are still too brief"
**Solution 1**: Increase retrieved chunks further
```python
relevant_chunks = self._retrieve_relevant_chunks(question, top_k=15)
```

**Solution 2**: Make the quality requirement explicit in the system prompt
- Add: "MINIMUM: Every answer must be at least 4 paragraphs"

**Solution 3**: Ask follow-up questions
- After an answer, ask: "Can you provide more details about [specific point]?"

### Problem: "Answers include too much irrelevant information"
**Solution**: Increase the similarity threshold
```python
min_similarity = 0.05  # was 0.01, filter more aggressively
```

### Problem: "Answers are sometimes contradictory"
**Solution**: Ensure documents are coherent, or reduce chunk overlap
```python
overlap = 100  # Reduce from 200 to prevent redundancy
```

### Problem: "Specific details are missing"
**Solution**: Increase context provided to the AI
```python
chunk_size = 1500  # Increase from 1000
relevant_chunks = self._retrieve_relevant_chunks(question, top_k=15)  # Increase from 10
```

## Recommended Configurations by Document Type

### Scientific Papers / Research Documents
```python
chunk_size = 1200
overlap = 300
top_k = 12
max_features = 2000
ngram_range = (1, 3)
```

### Technical Documentation / Manuals
```python
chunk_size = 1000
overlap = 250
top_k = 10
max_features = 1500
ngram_range = (1, 2)
```

### General Business / News Articles
```python
chunk_size = 800
overlap = 150
top_k = 8
max_features = 1000
ngram_range = (1, 2)
```

### Long-Form Narratives / Books
```python
chunk_size = 1200
overlap = 200
top_k = 15
max_features = 1000
ngram_range = (1, 2)
```

## Advanced Techniques

### 1. **Hybrid Search** (Future Enhancement)
Combine TF-IDF with semantic embeddings using a model like SentenceTransformers:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(chunks)
```

### 2. **Query Expansion** (Future Enhancement)
Automatically expand queries with synonyms:
```python
from textblob import TextBlob
expanded_query = query + " " + " ".join(get_synonyms(query))
```

### 3. **Iterative Retrieval** (Future Enhancement)
Refine results based on initial retrieval:
```python
# Get initial results
results_1 = retrieve(question, top_k=10)
# Extract keywords from results
keywords = extract_keywords(results_1)
# Retrieve again with expanded query
results_2 = retrieve(question + keywords, top_k=5)
```

## Summary

You now have:
✅ Larger, overlapping chunks for better context
✅ Better vocabulary coverage with bigrams
✅ More retrieved chunks for richer context
✅ Explicit, detailed instructions for the AI
✅ Citation requirements built into the prompt
✅ Minimum answer length expectations

**Start using the application now** and test with your documents. The answers should be significantly more detailed and better sourced.
