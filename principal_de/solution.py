import hashlib
import pandas as pd

from principal_de.vectorize import vectorize


def get_set1_df() -> pd.DataFrame:
    """
    Returns:
        pd.DataFrame: A DataFrame containing file names and their corresponding MD5 checksums.
    """
    file_names = ["principal_de/set1/lincoln.txt", "principal_de/set1/obama.txt", "principal_de/set1/trump.txt"]
    df = pd.DataFrame(file_names, columns=["file_names"])
    df["checksums"] = df["file_names"].apply(lambda x: hashlib.md5(open(x, 'rb').read()).hexdigest())
    return df

def get_set2_df() -> pd.DataFrame:
    """
    Returns:
        pd.DataFrame: A DataFrame containing file names and their corresponding MD5 checksums.
    """
    file_names = ["principal_de/set2/bush-added.txt", "principal_de/set2/obama-modified.txt", "principal_de/set2/trump-nochange.txt"]
    df = pd.DataFrame(file_names, columns=["file_names"])
    df["checksums"] = df["file_names"].apply(lambda x: hashlib.md5(open(x, 'rb').read()).hexdigest())
    return df

def get_merged_df() -> pd.DataFrame:
    """
    Returns:
        pd.DataFrame: A DataFrame containing the merged results of set1 and set2 with scenarios marked.
    """
    set1_df = get_set1_df()
    set2_df = get_set2_df()

    # Full outer join
    merged_df = pd.merge(set1_df, set2_df, on="checksums", how="outer", suffixes=("_set1", "_set2"))

    # 3 scenarios
    # 1. checksums in set1 and set2 are the same: do nothing
    # 2. checksums in set1 are not in set2: mark as delete
    # 3. checksums in set2 are not in set1: mark as add
    merged_df["scenario"] = merged_df.apply(lambda x: "do nothing" if not pd.isna(x["file_names_set1"]) and not pd.isna(x["file_names_set2"]) else "delete" if pd.isna(x["file_names_set2"]) else "add", axis=1)
    
    return merged_df


if __name__ == "__main__":

    # Vectorize set 1
    tbl_vectors = get_set1_df()
    tbl_vectors["vectors"] = None
    
    for index, row in tbl_vectors.iterrows():
        # Read file
        file_path = row["file_names"]
        with open(file_path, "r") as file:
            content = file.read()
        vector = vectorize(content)
        tbl_vectors.at[index, "vectors"] = vector

    tbl_vectors['marked_as_delete'] = False
    print(tbl_vectors)

    # Compare set1 and set2
    merged_df = get_merged_df()
    print(merged_df)

    # Update tbl_vectors accordingly.



    # Discuss pros and cons of this approach. Suggest alternative approaches.