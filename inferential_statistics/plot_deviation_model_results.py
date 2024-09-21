import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load the data from CSV files
group1_df = pd.read_csv('../SEANCE/Output/Each_reactiondata/results.csv')
group2_df = pd.read_csv('../SEANCE/Output/Each_reactionstory/results.csv')

# Load the detailed comparison results
detailed_comparisons_df = pd.read_csv('significant_features_comparison.csv')

# Set up the style of seaborn
sns.set(style="whitegrid")

# Create a directory for saving plots if needed
import os
if not os.path.exists("plots"):
    os.makedirs("plots")

# Plotting the distributions for each significant feature
for index, row in detailed_comparisons_df.iterrows():
    feature = row['Feature']

    # Load original data for the feature
    group1_data = group1_df[feature].dropna().values
    group2_data = group2_df[feature].dropna().values

    # Initialize a new figure
    plt.figure(figsize=(10, 6))

    # Boxplot for both groups
    sns.boxplot(data=[group1_data, group2_data], palette="Set2")
    plt.xticks([0, 1], ['Group 1', 'Group 2'])
    plt.title(f'Box Plot for {feature}')
    plt.ylabel('Values')
    plt.xlabel('Groups')

    # Save the plot
    plt.savefig(f"plots/boxplot_{feature}.png")
    plt.close()

    # Violin Plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(data=[group1_data, group2_data], palette="Set2")
    plt.xticks([0, 1], ['Group 1', 'Group 2'])
    plt.title(f'Violin Plot for {feature}')
    plt.ylabel('Values')
    plt.xlabel('Groups')

    # Save the plot
    plt.savefig(f"plots/violinplot_{feature}.png")
    plt.close()

    # Bar Plot with Error Bars
    plt.figure(figsize=(10, 6))
    means = [row['Mean Group 1'], row['Mean Group 2']]
    stds = [row['Std Group 1'], row['Std Group 2']]
    sns.barplot(x=['Group 1', 'Group 2'], y=means, yerr=stds, palette="Set2")
    plt.title(f'Bar Plot with Error Bars for {feature}')
    plt.ylabel('Mean Value')
    plt.xlabel('Groups')

    # Save the plot
    plt.savefig(f"plots/barplot_{feature}.png")
    plt.close()

print("Plots have been saved in the 'plots' directory.")