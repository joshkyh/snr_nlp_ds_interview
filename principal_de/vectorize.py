import numpy as np
from sentence_transformers import SentenceTransformer

def vectorize(input_str:str) -> np.array:
    #input_str = "hello"
    model = SentenceTransformer('BAAI/bge-small-en')
    embeddings_1 = model.encode(input_str, normalize_embeddings=True)
    return embeddings_1

if __name__ == "__main__":
    print(vectorize("hello"))
