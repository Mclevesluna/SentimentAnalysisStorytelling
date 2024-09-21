import os
import pandas as pd
import plotly.graph_objects as go

# Path to the CSV files
csv_file_data = '../SEANCE/Output/Each_reactiondata/results.csv'
csv_file_stories = '../SEANCE/Output/Each_reactionstory/results.csv'

# Path to the output Excel file
excel_output_file = '../SEANCE/Output/Each_reactiondata/analysis_results.xlsx'

# Check if the files exist
if not os.path.exists(csv_file_data):
    raise FileNotFoundError(f"File not found: {csv_file_data}")

if not os.path.exists(csv_file_stories):
    raise FileNotFoundError(f"File not found: {csv_file_stories}")

# Load the CSV files into DataFrames
df_data = pd.read_csv(csv_file_data)
df_stories = pd.read_csv(csv_file_stories)

# Define columns to analyze (exclude the first two columns)
columns_to_analyze = df_data.columns[2:]

# Compute correlation matrices
correlation_matrix_data = df_data[columns_to_analyze].corr()
correlation_matrix_stories = df_stories[columns_to_analyze].corr()

# Function to get strong correlations
def get_strong_correlations(correlation_matrix):
    strong_corrs = correlation_matrix[(correlation_matrix > 0.59) | (correlation_matrix < -0.59)]
    # Extract unique variables involved in strong correlations
    strong_vars = list(set(strong_corrs.columns[strong_corrs.notna().any()].tolist() +
                           strong_corrs.index[strong_corrs.notna().any()].tolist()))
    return strong_corrs, strong_vars

# Get strong correlations and variables
strong_corr_data, strong_vars_data = get_strong_correlations(correlation_matrix_data)
strong_corr_stories, strong_vars_stories = get_strong_correlations(correlation_matrix_stories)

# Filter correlation matrices to only include strong correlations
def filter_correlation_matrix(correlation_matrix, strong_vars):
    return correlation_matrix.loc[strong_vars, strong_vars]

# Filtered correlation matrices
filtered_corr_data = filter_correlation_matrix(correlation_matrix_data, strong_vars_data)
filtered_corr_stories = filter_correlation_matrix(correlation_matrix_stories, strong_vars_stories)

# Function to plot heatmap of filtered correlations
def plot_heatmap(correlation_matrix, title):
    fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        colorscale='Viridis',
        colorbar=dict(title='Correlation'),
        zmin=-1, zmax=1
    ))
    fig.update_layout(title=title, xaxis_title='Features', yaxis_title='Features')
    return fig

# Plot heatmaps
fig_heatmap_data = plot_heatmap(filtered_corr_data, 'Strong Correlations Heatmap - Data')
fig_heatmap_stories = plot_heatmap(filtered_corr_stories, 'Strong Correlations Heatmap - Stories')

# Save heatmaps to HTML files
fig_heatmap_data.write_html('../SEANCE/Output/Each_reactiondata/heatmap_data.html')
fig_heatmap_stories.write_html('../SEANCE/Output/Each_reactiondata/heatmap_stories.html')

print(f"Heatmaps have been saved to '../SEANCE/Output/Each_reactiondata/heatmap_data.html' and '../SEANCE/Output/Each_reactiondata/heatmap_stories.html'")

# Compute descriptive statistics
desc_stats_data = df_data[columns_to_analyze].describe()
desc_stats_stories = df_stories[columns_to_analyze].describe()

# Write to Excel
with pd.ExcelWriter(excel_output_file, engine='openpyxl') as writer:
    desc_stats_data.to_excel(writer, sheet_name='Descriptive Statistics Data')
    desc_stats_stories.to_excel(writer, sheet_name='Descriptive Statistics Stories')
    correlation_matrix_data.to_excel(writer, sheet_name='Correlation Matrix Data')
    correlation_matrix_stories.to_excel(writer, sheet_name='Correlation Matrix Stories')

print(f"Analysis results have been saved to {excel_output_file}")
