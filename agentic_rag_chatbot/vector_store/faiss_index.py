import faiss
import openai
import numpy as np

class VectorStore:
    def __init__(self, embedding_dim=1536):  # OpenAI's dim for text-embedding-3-small
        self.embedding_dim = embedding_dim
        self.index = faiss.IndexFlatL2(embedding_dim)
        self.documents = []  # List of dicts: {"chunk": ..., "metadata": {...}}

    def embed_text(self, texts):
        """
        Accepts a list of strings, returns numpy matrix of embeddings
        """
        response = openai.Embedding.create(
            input=texts,
            model="text-embedding-3-small"
        )
        embeddings = [e["embedding"] for e in response["data"]]
        return np.array(embeddings).astype("float32")

    def add_documents(self, chunks, metadata_list=None):
        """
        Adds chunk embeddings to index.
        :param chunks: List[str]
        :param metadata_list: Optional[List[dict]] — same length as chunks
        """
        embeddings = self.embed_text(chunks)
        self.index.add(embeddings)

        for i, chunk in enumerate(chunks):
            self.documents.append({
                "chunk": chunk,
                "metadata": metadata_list[i] if metadata_list else {}
            })

    def search(self, query, top_k=5):
        """
        Semantic search for top_k similar chunks
        :returns: List of {"chunk": ..., "metadata": ...}
        """
        query_embedding = self.embed_text([query])
        D, I = self.index.search(query_embedding, top_k)

        results = []
        for i in I[0]:
            if i < len(self.documents):
                results.append(self.documents[i])
        return results
