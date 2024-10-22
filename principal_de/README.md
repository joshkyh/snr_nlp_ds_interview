# Interview Briefing Document

## Overview
Data engineering for unstructured data often requires comparing sets of documents. In this project, you will be given two sets of documents in set1 and set2. Your task is to perform steps 3 and 4:
## Steps

1. **Vectorize Documents in Set 1**:
    - Use the `get_set1_df` function to create a DataFrame containing file names and their corresponding MD5 checksums for documents in set1.
    - For each document in set1, read the content and use the `vectorize` function to generate vector embeddings.
    - Store these vector embeddings in the DataFrame.

2. **Compare Set 1 and Set 2**:
    - Use the `get_set2_df` function to create a DataFrame containing file names and their corresponding MD5 checksums for documents in set2.
    - Use the `get_merged_df` function to merge the DataFrames from set1 and set2 based on their checksums.
    - Identify the following scenarios in the merged DataFrame:
        - Documents with the same checksums in both sets: "do nothing".
        - Documents with checksums in set1 but not in set2: "delete".
        - Documents with checksums in set2 but not in set1: "add".
    - To help supervision, `lincoln.txt` is deleted. `trump.txt` is left as-is (do nothing). `obama.txt` is modified. `bush.txt` is added.

3. **Update Vectorized DataFrame**:
    - Based on the scenarios identified in the merged DataFrame, update the vectorized DataFrame from set1.
    - Mark documents that need to be deleted.

4. **Discussion**:
    - Discuss the pros and cons of the current approach.
    - Suggest alternative approaches for vectorizing and comparing documents.
