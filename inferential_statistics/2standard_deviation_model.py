import pandas as pd
import numpy as np

# Load the data from CSV files
group1_df = pd.read_csv('../SEANCE/Output/Each_reactiondata/results.csv')
group2_df = pd.read_csv('../SEANCE/Output/Each_reactionstory/results.csv')

## Load the data from CSV files, excluding the first two non-numeric columns
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


# Ensure both dataframes have the same columns and shape
assert group1_df_filtered.shape[1] == group2_df_filtered.shape[1], "The two groups must have the same number of features."

# Convert all columns to numeric, coercing errors to NaN
group1_df_numeric = group1_df_filtered.apply(pd.to_numeric, errors='coerce')
group2_df_numeric = group2_df_filtered.apply(pd.to_numeric, errors='coerce')

# Initialize a list to store the results
results = []

# Iterate over each feature (column)
for feature in group1_df_numeric.columns:
    # Extract data for the current feature, dropping NaN values
    group1 = group1_df_numeric[feature].dropna().values  # Drop missing values, if any
    group2 = group2_df_numeric[feature].dropna().values
    
    # Check if both groups have sufficient data
    if len(group1) == 0 or len(group2) == 0:
        print(f"Skipping feature '{feature}' due to insufficient data.")
        continue
    
    # Step 1: Calculate the mean and standard deviation for each group
    mean1 = np.mean(group1)
    mean2 = np.mean(group2)
    
    # Calculating standard deviation for each group
    std1 = np.std(group1)  # Population standard deviation
    std2 = np.std(group2)  # Population standard deviation

    # Step 2: Compute the difference in means
    mean_diff = mean1 - mean2

    # Step 3: Calculate the combined standard deviation for the difference in means
    n1 = len(group1)
    n2 = len(group2)
    combined_std = np.sqrt((std1**2 / n1) + (std2**2 / n2))

    # Step 4: Determine if the difference is significant using the 2 standard deviation rule
    significance_threshold = 2 * combined_std

    # Step 5: Check significance and store the result
    is_significant = abs(mean_diff) > significance_threshold
    results.append({
        'Feature': feature, 
        'Mean Difference': mean_diff, 
        'Std Group 1': std1,
        'Std Group 2': std2,
        'Significant': is_significant
    })

# Convert results to a DataFrame for easy viewing
results_df = pd.DataFrame(results)

# Save results to CSV file
results_df.to_csv('results_comparison.csv', index=False)
results_df.to_excel('results_comparison.xlsx', index=False)

print("Results have been saved to 'results_comparison.csv' and 'results_comparison.xlsx'.")

# Step 6: Extract significant features
significant_features = results_df[results_df['Significant'] == True]['Feature'].tolist()

# Initialize a list to store detailed comparisons for significant features
detailed_comparisons = []

# Step 7: Compare statistics for significant features
for feature in significant_features:
    # Get data for the significant feature from the original DataFrames
    group1_data = group1_df[feature].dropna().values  # Drop missing values, if any
    group2_data = group2_df[feature].dropna().values
    
    # Calculate statistics for Group 1
    mean1 = np.mean(group1_data)
    std1 = np.std(group1_data)
    min1 = np.min(group1_data)
    max1 = np.max(group1_data)
    
    # Calculate statistics for Group 2
    mean2 = np.mean(group2_data)
    std2 = np.std(group2_data)
    min2 = np.min(group2_data)
    max2 = np.max(group2_data)
    
    # Store the comparison
    detailed_comparisons.append({
        'Feature': feature,
        'Mean Group 1': mean1,
        'Std Group 1': std1,
        'Min Group 1': min1,
        'Max Group 1': max1,
        'Mean Group 2': mean2,
        'Std Group 2': std2,
        'Min Group 2': min2,
        'Max Group 2': max2
    })

# Convert detailed comparisons to a DataFrame
detailed_comparisons_df = pd.DataFrame(detailed_comparisons)

# Save detailed comparisons to a CSV file
detailed_comparisons_df.to_csv('significant_features_comparison.csv', index=False)

# Save detailed comparisons to an Excel file
detailed_comparisons_df.to_excel('significant_features_comparison.xlsx', index=False)

print("Detailed comparisons for significant features have been saved to 'significant_features_comparison.csv' and 'significant_features_comparison.xlsx'.")


