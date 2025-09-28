import faiss
import numpy as np

def build_faiss_index(embeddings, metadata_list):
    arr = np.array(embeddings).astype("float32")
    faiss.normalize_L2(arr)
    index = faiss.IndexFlatIP(arr.shape[1])
    index.add(arr)
    return index, metadata_list

def similarity_search(index, query_embedding, metadata_list, top_k=5):
    q = np.array([query_embedding]).astype("float32")
    faiss.normalize_L2(q)
    D, I = index.search(q, top_k)
    results = []
    for idx, score in zip(I[0], D[0]):
        results.append({
            "score": float(score),
            "metadata": metadata_list[idx]
        })
    return results
