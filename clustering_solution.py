import matplotlib.pyplot as plt
import umap
import pandas as pd
from sklearn.cluster import KMeans


def load_data() -> pd.DataFrame:
    """
    Load the dataset from a pickle file and filter for specific topics.

    Returns:
        pd.DataFrame: The filtered DataFrame containing only topics 1, 6, 11, and 16.
    """
    # Load the DataFrame from the pickle file
    dfr = pd.read_pickle('sampled_df.pkl')

    # Keep only topics 1, 6, 11, and 16
    dfr = dfr[dfr['topic'].isin([1, 6, 11, 16])]
    print(dfr.shape)
    return dfr


def perform_k_means(dfr: pd.DataFrame) -> pd.DataFrame:
    """
    Perform KMeans clustering on the embeddings in the DataFrame.

    Args:
        dfr (pd.DataFrame): The DataFrame containing the embeddings.

    Returns:
        pd.DataFrame: The DataFrame with an additional 'cluster' column indicating the cluster assignment.
    """
    # Extract embeddings from the DataFrame
    embeddings = list(dfr['embedding'])

    # Run KMeans clustering with k=4
    kmeans = KMeans(n_clusters=4, random_state=42)
    dfr['cluster'] = kmeans.fit_predict(embeddings)
    return dfr

def check_agreement(dfr: pd.DataFrame) -> None:
    """
    Check the agreement between topics and clusters by calculating the proportion of each topic in each cluster.

    Args:
        dfr (pd.DataFrame): The DataFrame containing the topic and cluster information.
    """
    # Group by topic and cluster, and count the occurrences
    grouped = dfr.groupby(['topic', 'cluster']).size().reset_index(name='count')
    
    # Calculate the total count for each topic
    topic_counts = grouped.groupby('topic')['count'].transform('sum')

    # Add a new column 'proportion' which is count / count_of_topic
    grouped['proportion'] = grouped['count'] / topic_counts

    # For each topic, filter for the row that has the highest proportion
    max_proportion_per_topic = grouped.loc[grouped.groupby('topic')['proportion'].idxmax()]

    print(max_proportion_per_topic)


def downproject_2D(dfr: pd.DataFrame) -> pd.DataFrame:
    """
    Downproject the embeddings to 2D using UMAP.

    Args:
        dfr (pd.DataFrame): The DataFrame containing the embeddings.

    Returns:
        pd.DataFrame: The DataFrame with an additional 'embedding_2d' column containing the 2D embeddings.
    """
    # Initialize UMAP with 2 components
    umap_model = umap.UMAP(n_components=2)
    embeddings = list(dfr['embedding'])

    # Fit and transform the embeddings to 2D
    dfr['embedding_2d'] = list(umap_model.fit_transform(embeddings))
    return dfr


def plot_2D(dfr: pd.DataFrame) -> None:
    """
    Plot the 2D embeddings with cluster labels as colors and topic labels as markers.

    Args:
        dfr (pd.DataFrame): The DataFrame containing the 2D embeddings, cluster, and topic information.
    """
    # Plot the 2D embeddings with cluster labels as colors
    plt.figure(figsize=(10, 8))
    markers = ['o', 's', 'D', '^']  # Define different markers for each topic
    colors = ['r', 'g', 'b', 'y']  # Define different colors for each cluster
    for i, topic in enumerate(dfr['topic'].unique()):
        for j, cluster in enumerate(dfr['cluster'].unique()):
            topic_cluster_data = dfr[(dfr['topic'] == topic) & (dfr['cluster'] == cluster)]
            plt.scatter(topic_cluster_data['embedding_2d'].apply(lambda x: x[0]), 
                        topic_cluster_data['embedding_2d'].apply(lambda x: x[1]), 
                        color=colors[cluster % len(colors)], s=50, 
                        marker=markers[i % len(markers)], label=f'Topic {topic} Cluster {cluster}')

    # Set plot title and labels
    plt.title('Color = Cluster, Marker = Topic')
    plt.xlabel('UMAP 1')
    plt.ylabel('UMAP 2')

    # Show plot
    #plt.show()
    
    # Export the plot to a png file
    plt.savefig('clusters.png')


if __name__=='__main__':
    dfr = load_data()
    dfr = perform_k_means(dfr)
    check_agreement(dfr)
    dfr = downproject_2D(dfr)
    plot_2D(dfr)