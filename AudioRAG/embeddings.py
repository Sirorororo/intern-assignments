from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np

def load_model(model_name):
    return SentenceTransformer(model_name)
    
def create_df(chunks,model):
    embedded_chunks = model.encode(chunks)
    df = pd.DataFrame({
        "Text" : chunks,
        "Embeddings" : [row.tolist() for row in embedded_chunks]
    })
    return df

def cosine_similarity(a,b):
    a = np.array(a)
    b = np.array(b)

    dot_product = np.dot(a,b)

    mag_a = np.linalg.norm(a)
    mag_b = np.linalg.norm(b)

    similarity = dot_product / (mag_a * mag_b)
    return similarity

def calculate_cosine_similarity(df,embedded_query):
    df["similarity"] = df["Embeddings"].apply(lambda x: cosine_similarity(x,embedded_query))
    results = df.sort_values("similarity",ascending = False)
    top_k = results["Text"].head(5).tolist()
    return top_k