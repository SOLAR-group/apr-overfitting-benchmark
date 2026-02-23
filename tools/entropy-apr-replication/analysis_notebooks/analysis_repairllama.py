import sys
import os
import json
import pandas as pd

# Directory containing patch files
PATCHES_DIRECTORY = "patches/patches_entropy_repairllama_filtered"

# Initialize an empty list to store patch data
patches_list = []

# Walk through the patch directory to process each file
for subdir, _, files in os.walk(PATCHES_DIRECTORY):
    for file in files:
        # Extract bug and project information from the directory structure
        bug = subdir.split("/")[-1]
        project = subdir.split("/")[-2]
        file_path = os.path.join(subdir, file)
        
        # Determine if the patch is correct or incorrect based on the file path
        correct = True
        if "incorrect" in file_path:
            correct = False
        
        # Open and parse the JSON file
        with open(file_path, "r") as f:
            try:
                patches_dict = json.load(f)
            except:
                # Print the file path if JSON parsing fails and skip to the next file
                print(file_path)
                continue
        
        # Calculate entropy metrics for the patch
        patched_entropy = patches_dict["patched_entropy"]
        original_entropy = patches_dict["original_entropy"]
        average_patch_entropy = sum(patched_entropy.values()) / len(patched_entropy)
        average_original_entropy = sum(original_entropy.values()) / len(original_entropy)
        
        # Add calculated metrics to the patch dictionary
        patches_dict["avg_patch_entropy"] = average_patch_entropy
        patches_dict["avg_original_entropy"] = average_original_entropy
        patches_dict["entropy_delta"] = average_original_entropy - average_patch_entropy
        
        # Append the patch dictionary to the list
        patches_list.append(patches_dict)

# Create a DataFrame from the list of patches
df = pd.DataFrame(patches_list)

# Convert the 'correct' column to boolean type
df["correct"] = df["correct"].astype(bool)

# Filter the DataFrame to include only correct patches
df_count = df[df['correct'] == True]

# Count the number of unique bug IDs in each project for correct patches
print("rq1 dataset (table 1)")
print(df_count.groupby(['project']).size().reset_index(name='counts'))

# Function to calculate the number of top-N ranked patches for a given project
def top_n(df, n, project):
    if not project == "Total":
        df = df[df["project"] == project]
    top_n = len(df[df["correct"] & (df["patch_rank"] <= n)])
    print(f"{project}: top {n} ranking: {top_n}")

# Rank patches within each project and bug ID by entropy delta in descending order
df["patch_rank"] = df.groupby(["project", "bug_id"])["entropy_delta"].rank(
    ascending=False
)

# Calculate and print top-1 and top-2 rankings for each project and overall
top_n(df, 1, "Chart")
top_n(df, 2, "Chart")

top_n(df, 1, "Closure")
top_n(df, 2, "Closure")

top_n(df, 1, "Lang")
top_n(df, 2, "Lang")

top_n(df, 1, "Math")
top_n(df, 2, "Math")

top_n(df, 1, "Mockito")
top_n(df, 2, "Mockito")

top_n(df, 1, "Time")
top_n(df, 2, "Time")

top_n(df, 1, "Total")
top_n(df, 2, "Total")

# Import visualization libraries
import seaborn as sns
from matplotlib import pyplot as plt

# Set the theme for the plots
sns.set_theme(style="whitegrid")

# Prepare data for visualization
df_melt = df[["project", "correct", "entropy_delta"]]
df_melt.columns = ["project", "correct_patch", "entropy_delta"]

# Create a side-by-side boxplot to compare entropy deltas for correct and incorrect patches
sns.boxplot(data=df_melt, x="project", y="entropy_delta", hue="correct_patch", palette="colorblind")
plt.xlabel('', fontsize="15")
plt.ylabel('Entropy delta', fontsize="15")

# Adjust font sizes for better readability
plt.xticks(fontsize="15")
plt.yticks(fontsize="15")

# Save the plot to a file
plt.savefig("analysis_notebooks/plots_repairllama/repairllama_tested_ranking_edelta.pdf")

# Function to classify patches based on entropy delta and calculate metrics
def classification(df, prior_tool, cutoff):
    # Rank patches within each project and bug ID by entropy delta
    df["patch_rank"] = df.groupby(["project", "bug_id"])["entropy_delta"].rank(
        ascending=False
    )
    
    # Calculate the mean entropy delta for each bug ID and correctness
    df_mean_delta = (
        df.groupby(["project", "bug_id", "correct"])["entropy_delta"]
        .mean()
        .reset_index(name="avg_entropy_delta")
    )
    
    # Determine if the average entropy delta exceeds the cutoff
    df_binary_delta = (
        df_mean_delta.groupby(["project", "bug_id", "correct"])["avg_entropy_delta"]
        .apply(lambda x: (x > cutoff).sum())
        .reset_index(name="positive_delta")
    )

    # Classify patches into true positives, false positives, true negatives, and false negatives
    true_positive_df = df_binary_delta[
        (df_binary_delta["correct"]) & df_binary_delta["positive_delta"] == 1
    ]
    false_positive_df = df_binary_delta[
        ~(df_binary_delta["correct"]) & (df_binary_delta["positive_delta"] == 1)
    ]
    true_negative_df = df_binary_delta[
        ~(df_binary_delta["correct"]) & (df_binary_delta["positive_delta"] == 0)
    ]
    false_negative_df = df_binary_delta[
        (df_binary_delta["correct"]) & (df_binary_delta["positive_delta"] == 0)
    ]

    # Create a CSV output with patch analysis
    df_patches = df.copy()
    df_patches['prediction'] = (df_patches['entropy_delta'] > cutoff).astype(int)
    df_patches['patch_name'] = df_patches['file_path'].apply(lambda x: x.split('/')[-1])
    df_patches['correctness'] = df_patches['correct'].apply(lambda x: 'correct' if x else 'overfitting')
    df_patches['prediction'] = df_patches['prediction'].apply(lambda x: 'correct' if x == 1 else 'overfitting')
    
    # Select and write to CSV
    result_df = df_patches[['patch_name', 'correctness', 'prediction']]
    csv_path = f"entropy_analysis_repairllama_cutoff_{cutoff}.csv"
    result_df.to_csv(csv_path, index=False)
    print(f"Patch analysis written to {csv_path}")
    
    # Calculate and print classification metrics
    true_positive = len(true_positive_df)
    false_positive = len(false_positive_df)
    true_negative = len(true_negative_df)
    false_negative = len(false_negative_df)

    print(f"True positive count: {true_positive}")
    print(f"True negative count: {true_negative}")

    print(f"False positive count: {false_positive}")
    print(f"False negative count: {false_negative}")

    accuracy = round(
        (true_positive + true_negative)
        / (true_positive + true_negative + false_positive + false_negative),
        3,
    )
    precision = round(true_positive / (true_positive + false_positive), 3)
    pos_recall = round(true_positive / (true_positive + false_negative), 3)
    neg_recall = round(true_negative / (true_negative + false_positive), 3)
    f1 = round(
        true_positive / (true_positive + 0.5 * (false_positive + false_negative)), 3
    )

    print(f"accuracy: {accuracy}")
    print(f"precision: {precision}")
    print(f"+recall: {pos_recall}")
    print(f"-recall: {neg_recall}")
    print(f"f1: {f1}")

# Run the classification function with a specified cutoff value
classification(df, "i", -0.55)