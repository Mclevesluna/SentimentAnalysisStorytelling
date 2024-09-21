import pandas as pd
from tabulate import tabulate

# Path to the single CSV file
csv_file = '../SEANCE/Output/Combined_reactiontxts/results.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(csv_file)

# Split the DataFrame into two parts: one for the first row and one for the second row
df_data = df.iloc[0:1, :]   # First row
df_stories = df.iloc[1:2, :] # Second row

# Select columns starting from 'Anger_EmoLex'
columns_to_analyze = df.columns[df.columns.get_loc('Anger_EmoLex'):]

# Extract relevant columns for each row
df_data_selected = df_data[columns_to_analyze]
df_stories_selected = df_stories[columns_to_analyze]

# Calculate the mean for the first and second rows
mean_data = df_data_selected.mean()
mean_stories = df_stories_selected.mean()

# Combine the means into one DataFrame for easy comparison
combined_means = pd.concat([mean_data, mean_stories], axis=1)
combined_means.columns = ['First Row Mean', 'Second Row Mean']

# Display the results as a nice table using tabulate
print(tabulate(combined_means, headers='keys', tablefmt='fancy_grid'))

# Export the combined means to a CSV file
combined_means.to_csv('combined_means.csv', index=True)
print("Combined means have been exported to 'combined_means.csv'.")
