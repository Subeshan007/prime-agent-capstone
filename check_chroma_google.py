try:
    from chromadb.utils import embedding_functions
    if hasattr(embedding_functions, 'GoogleGenerativeAIEmbeddingFunction'):
        print("GoogleGenerativeAIEmbeddingFunction exists")
    else:
        print("GoogleGenerativeAIEmbeddingFunction NOT found")
except Exception as e:
    print(f"Error: {e}")
