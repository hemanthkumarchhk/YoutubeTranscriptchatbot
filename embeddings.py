import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

def get_openai_embeddings(openai, texts, model=EMBEDDING_MODEL):
    response = openai.Embedding.create(model=model, input=texts)
    return [r["embedding"] for r in response["data"]]

def get_local_embeddings(texts, model_name="all-MiniLM-L6-v2"):
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    return model.encode(texts, show_progress_bar=False).tolist()
