from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



import numpy as np
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

def fetch_and_vectorize_20newsgroups():
    # Fetch the data for all 20 categories
    categories = [
        'alt.atheism', 'comp.graphics', 'comp.os.ms-windows.misc', 'comp.sys.ibm.pc.hardware',
        'comp.sys.mac.hardware', 'comp.windows.x', 'misc.forsale', 'rec.autos', 'rec.motorcycles',
        'rec.sport.baseball', 'rec.sport.hockey', 'sci.crypt', 'sci.electronics', 'sci.med',
        'sci.space', 'soc.religion.christian', 'talk.politics.guns', 'talk.politics.mideast',
        'talk.politics.misc', 'talk.religion.misc'
    ]

    # Fetch the training data
    newsgroups_train = fetch_20newsgroups(subset='train', categories=categories)

    # Create a DataFrame
    df = pd.DataFrame({'text_content': newsgroups_train.data, 'topic': newsgroups_train.target})

    # To get 10 rows per topic, we need to filter the DataFrame
    sampled_df = df.groupby('topic').head(10).reset_index(drop=True)

    
    return sampled_df

# Fetch and vectorize the 20 newsgroups data, returning the sampled DataFrame
sampled_df = fetch_and_vectorize_20newsgroups()

def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

# Apply the get_embedding function to each row in the 'text_content' column and create a new 'embedding' column
sampled_df['embedding'] = sampled_df['text_content'].apply(lambda x: get_embedding(x))


# Save sampled_df as parquet
sampled_df.to_pickle('sampled_df.pkl')
