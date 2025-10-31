# embed_model.py
from sentence_transformers import SentenceTransformer
from settings import EMBEDDING_MODEL

class Embedder:
    def __init__(self, model_name=EMBEDDING_MODEL):
        print("Loading embedding model:", model_name)
        self.model = SentenceTransformer(model_name)

    def encode(self, texts):
        # returns list of vectors
        if isinstance(texts, str):
            texts = [texts]
        vectors = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        return vectors
