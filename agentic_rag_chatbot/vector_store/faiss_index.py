from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")
        self.embeddings = []
        self.documents = []
        self.index = None

    def add_documents(self, chunks, metadata=None):
        vectors = self.model.encode(chunks, show_progress_bar=False)
        self.embeddings.extend(vectors)
        self.documents.extend(chunks)
        self._rebuild_index()

    def _rebuild_index(self):
        if self.embeddings:
            arr = np.array(self.embeddings).astype('float32')
            self.index = faiss.IndexFlatL2(arr.shape[1])
            self.index.add(arr)

    def search(self, query, top_k=5):
        if self.index is None:
            return []

        q_vec = self.model.encode([query])
        D, I = self.index.search(np.array(q_vec).astype('float32'), top_k)
        results = [{"chunk": self.documents[i]} for i in I[0] if i < len(self.documents)]
        return results
