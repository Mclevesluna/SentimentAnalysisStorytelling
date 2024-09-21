import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA

import os

# Print the current working directory to debug path issues
print("Current Working Directory:", os.getcwd())

# Load the data from CSV files, excluding the first two non-numeric columns
group1_df = pd.read_csv('../SEANCE/Output/Each_reactiondata/results.csv').iloc[:, 2:]
group2_df = pd.read_csv('../SEANCE/Output/Each_reactionstory/results.csv').iloc[:, 2:]

# Define substrings to exclude
exclude_substrings = ['_neg_3', '_nwords']

# Create a mask to filter out columns with the specified substrings in their names
mask_group1 = ~group1_df.columns.str.contains('|'.join(exclude_substrings))
mask_group2 = ~group2_df.columns.str.contains('|'.join(exclude_substrings))

# Apply the mask to filter columns
group1_df_filtered = group1_df.loc[:, mask_group1]
group2_df_filtered = group2_df.loc[:, mask_group2]

# Calculate mean and standard deviation for each feature across both groups
mean_group1 = group1_df_filtered.mean()
mean_group2 = group2_df_filtered.mean()
std_group1 = group1_df_filtered.std()
std_group2 = group2_df_filtered.std()

# Create a DataFrame for clustering with means and standard deviations
feature_data = pd.DataFrame({
    'Mean_Group1': mean_group1,
    'Mean_Group2': mean_group2,
    'Std_Group1': std_group1,
    'Std_Group2': std_group2
})

# Standardize the data
scaler = StandardScaler()
scaled_features = scaler.fit_transform(feature_data)

# Perform K-means clustering with K=2 and K=4
kmeans_2 = KMeans(n_clusters=2, random_state=42)
kmeans_2.fit(scaled_features)

kmeans_4 = KMeans(n_clusters=4, random_state=42)
kmeans_4.fit(scaled_features)

# Calculate and print SSE for K=2 and K=4
sse_k2 = kmeans_2.inertia_
sse_k4 = kmeans_4.inertia_
print(f"When K=2 SSE = {sse_k2}")
print(f"When K=4 SSE = {sse_k4}")

# Perform K-means clustering with K=5 (as per your original code)
kmeans = KMeans(n_clusters=5, random_state=42)  # Adjust the number of clusters as needed
kmeans.fit(scaled_features)

# Assign cluster labels to each feature
feature_data['Cluster_KMeans'] = kmeans.labels_

# Display the names of features grouped by clusters for K-means
clusters_kmeans = feature_data.groupby('Cluster_KMeans')
print("K-means Clustering Results:")
for cluster, features in clusters_kmeans:
    print(f"Cluster {cluster}:")
    print(features.index.tolist())  # Printing the names of features in this cluster
    print("\n")

# Save the clustered features to a CSV file for K-means results
feature_data.to_csv('clustered_features_kmeans.csv')
print("K-means clustered features have been saved to 'clustered_features_kmeans.csv'.")

# Plot K-means clusters in terms of the first two principal components
pca = PCA(n_components=2)
principal_components = pca.fit_transform(scaled_features)

plt.figure(figsize=(12, 8))
plt.scatter(principal_components[:, 0], principal_components[:, 1], c=kmeans.labels_, cmap='viridis', marker='o')
plt.title('K-means Clustering (K=5) - PCA of Features')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.colorbar(label='Cluster Label')
plt.show()

# Correlation Analysis and Filtering for Significant Correlations

# Calculate correlations for both groups
correlation_data = group1_df_filtered.corr(method='pearson')
correlation_story = group2_df_filtered.corr(method='pearson')

# Select only significant correlations (>=0.6 or <=-0.6) for data group
significant_corr_data = correlation_data[(correlation_data >= 0.0) | (correlation_data <= -0.0)].dropna(how='all', axis=0).dropna(how='all', axis=1)

# Select only significant correlations (>=0.6 or <=-0.6) for stories group
significant_corr_story = correlation_story[(correlation_story >= 0.0) | (correlation_story <= -0.0)].dropna(how='all', axis=0).dropna(how='all', axis=1)

# Plot heatmap for significant correlations in data group
plt.figure(figsize=(12, 10))
sns.heatmap(significant_corr_data, annot=False, cmap='coolwarm', center=0)
plt.title('Significant Correlation Heatmap (Data Stories)')
plt.show()

# Plot heatmap for significant correlations in stories group
plt.figure(figsize=(12, 10))
sns.heatmap(significant_corr_story, annot=False, cmap='coolwarm', center=0)
plt.title('Significant Correlation Heatmap (Creative Stories)')
plt.show()

# Load significant features from the CSV file
try:
    significant_features_df = pd.read_csv('../inferential_statistics/significant_features_comparison.csv')
    print("Significant features CSV loaded successfully.")
except FileNotFoundError:
    print("Error: The file 'significant_features_comparison.csv' was not found in 'inferential_statistics'.")
    exit()

# Extract the list of features from the first column
significant_features = significant_features_df.iloc[:, 0].tolist()

# Print to debug the loaded features and column names
print("Significant features from CSV:", significant_features)
print("Group 1 columns:", group1_df_filtered.columns.tolist())
print("Group 2 columns:", group2_df_filtered.columns.tolist())

# Check if the significant features are present in the group dataframes
significant_features_group1 = [feature for feature in significant_features if feature in group1_df_filtered.columns]
significant_features_group2 = [feature for feature in significant_features if feature in group2_df_filtered.columns]
print("Filtered significant features for Group 1:", significant_features_group1)
print("Filtered significant features for Group 2:", significant_features_group2)

# Filter both dataframes to only include the significant features
group1_filtered_for_heatmap = group1_df_filtered[significant_features_group1]
group2_filtered_for_heatmap = group2_df_filtered[significant_features_group2]

# Calculate correlations for the filtered data
filtered_corr_data = group1_filtered_for_heatmap.corr(method='pearson')
filtered_corr_story = group2_filtered_for_heatmap.corr(method='pearson')

# Plot heatmap for filtered significant correlations in data group
plt.figure(figsize=(12, 10))
sns.heatmap(filtered_corr_data, annot=False, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap for Significant Features (Data Stories)')
plt.show()

# Plot heatmap for filtered significant correlations in stories group
plt.figure(figsize=(12, 10))
sns.heatmap(filtered_corr_story, annot=False, cmap='coolwarm', center=0)
plt.title('Correlation Heatmap for Significant Features (Creative Stories)')
plt.show()

# Function to print top 20 correlations
def print_top_correlations(correlation_matrix, title):
    # Unstack the correlation matrix to a DataFrame and drop duplicate pairs
    corr_pairs = correlation_matrix.unstack().reset_index()
    corr_pairs.columns = ['Feature1', 'Feature2', 'Correlation']
    corr_pairs = corr_pairs[corr_pairs['Feature1'] != corr_pairs['Feature2']]
    corr_pairs = corr_pairs.drop_duplicates(subset=['Feature1', 'Feature2'])
    
    # Print top 20 positive and negative correlations
    top_positives = corr_pairs[corr_pairs['Correlation'] > 0].sort_values(by='Correlation', ascending=False).head(20)
    top_negatives = corr_pairs[corr_pairs['Correlation'] < 0].sort_values(by='Correlation').head(20)
    
    print(f"Top 20 Positive Correlations for {title}:")
    print(top_positives)
    print("\nTop 20 Negative Correlations for {title}:")
    print(top_negatives)

# Print top 20 correlations for each group
print_top_correlations(filtered_corr_data, "Data Stories")
print_top_correlations(filtered_corr_story, "Creative Stories")
