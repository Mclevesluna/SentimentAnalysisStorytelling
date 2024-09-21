# Sentiment and Cognition Analysis Tool

This program analyzes emotional and cognitive responses to different types of stimuli (e.g., data dashboards and storytelling) by formatting the input data, running SEANCE, and identifying features with significant differences between two groups. The workflow is broken down into three main steps:


---

**🟢 TO DEMO THIS TOOL:**
> Please ensure you have installed the SEANCE model within the SEANCE folder (Available on: https://www.linguisticanalysistools.org/seance.html)
> Please follow steps 3, 4, and 5 in the following set of instructions. You will only have to run 3 files:  
> - `2standard_deviation_model.py`
> - `plot_deviation_model_results.py`
> - `cluster_correlation_analysis.py`

---


## 1. Format Input Data for SEANCE

This script processes your input CSV files to generate the necessary format for running SEANCE, which performs sentiment and cognition analysis.

### File: `format_input.py`

### Libraries:
- `pandas`
- `os`

### How It Works:
- Reads two CSV files containing reactions to data dashboards and storytelling.
- Outputs the following text files:
  - **Combined responses** from all participants into a single file.
  - **Separated question responses** for each question from the CSVs.
  - **Individual row responses** where each row from the CSV becomes a separate file.

### Instructions:
1. Modify the paths in the script to point to your input CSV files and desired output directories.
2. Run `format_input.py` to generate the formatted text files for SEANCE.

---

## 2. Run SEANCE

This step requires the **SEANCE** software to perform sentiment and cognition analysis.

### How It Works:
- SEANCE generates output files analyzing sentiment and cognition based on the provided text files.
- You must manually start SEANCE, select the appropriate lexicons, and point it to the input folder with your formatted text files.

### Instructions:
1. Open SEANCE by running:
    ```bash
    python SEANCE_1_2_0.py
    ```
2. Once SEANCE opens, select the input folder (either `Each_reactionstory` or `Each_reactiondata`).
3. Choose your lexicons and click on "Start" to run the analysis.
4. Output files will be saved in the SEANCE `Output` directory.

---

## 3. Analyze Significant Feature Differences

This script identifies significant features with differences in their means between the two groups (data dashboards vs. storytelling) using a 2-standard-deviation rule.

### File: `2standard_deviation_model.py`

### Libraries:
- `pandas`
- `numpy`

### How It Works:
- Reads SEANCE output files for both groups.
- Filters features using a 2-standard-deviation model to find those with the most significant differences between groups.

### Instructions:
1. Modify the paths in the script to point to the SEANCE output files for each group.
2. Run `2standard_deviation_model.py` to calculate the significant feature differences.

---

### Folder Structure
After running the scripts, the folder structure will look like this:

## 4. Plot Violin and Box Plots to Visualize Differences in Features with Significant Differences

This script generates violin and box plots to visualize the distribution of features identified as having significant differences between two groups.

### File: `plot_deviation_model_results.py`

### Libraries:
- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `os`

### How It Works:
- Loads the SEANCE output files for both groups.
- Loads the detailed comparison results file, which contains information about significant features.
- For each significant feature, the script generates:
  - A **box plot** to compare the distribution of values for each group.
  - A **violin plot** to visualize the data's density and distribution.
  - A **bar plot with error bars** to show the mean and standard deviation of each feature across the two groups.
- The plots are saved as PNG files in a `plots` directory.

### Instructions:
1. Modify the paths in the script to point to the SEANCE output files and the comparison results CSV.
2. Run the `plot_deviation_model_results.py` to generate and save the plots.

---

## 5. Perform Cluster and Correlation Analysis to Identify Patterns

This script performs clustering analysis using K-means, evaluates cluster effectiveness with SSE, and conducts correlation analysis to find patterns among significant features.

### File: `cluster_correlation_analysis.py`

### Libraries:
- `pandas`
- `seaborn`
- `matplotlib`
- `sklearn.preprocessing.StandardScaler`
- `sklearn.cluster.KMeans, AgglomerativeClustering`
- `sklearn.decomposition.PCA`
- `os`

### How It Works:
- Loads the SEANCE output files, excluding non-numeric columns.
- Filters columns to remove those containing specific substrings (e.g., `_neg_3`, `_nwords`).
- Standardizes the data and performs K-means clustering with different values of K (2, 4, 5).
- The results of clustering (e.g., feature grouping by clusters) are saved to a CSV file and printed in the console.
- **PCA** is used to visualize clusters in a 2D space.
- **Correlation analysis** identifies significant correlations (>= 0.6 or <= -0.6) between features for both groups.
- Heatmaps are generated for both groups, showing significant correlations.
- Top 20 positive and negative correlations are printed for each group.

### Instructions:
1. Modify the paths in the script to point to the SEANCE output files.
2. Run the `cluster_correlation_analysis.py` to:
   - Perform clustering and save the results to `clustered_features_kmeans.csv`.
   - Visualize the clusters with PCA.
   - Perform correlation analysis and display the top correlations.
   - Generate and display heatmaps of significant correlations.

---

## Output

After running these steps:
- **Box, Violin, and Bar Plots** for significant features will be stored in the `plots/` directory.
- **K-means clustering results** will be stored in `clustered_features_kmeans.csv`.
- **Correlation heatmaps** will be generated and displayed.
- **Top correlations** (positive and negative) will be printed in the console.


Source for SEANCE tool contained in the folder SEANCE_1_2_0_Py3: 



Crossley, S. A., Kyle, K., & McNamara, D. S. (2017). Sentiment analysis and social cognition engine (SEANCE): An automatic tool for sentiment, social cognition, and social order analysis. Behavior Research Methods 49(3), pp. 803-821. doi:10.3758/s13428-016-0743-z. 
Available on: https://www.linguisticanalysistools.org/seance.html
