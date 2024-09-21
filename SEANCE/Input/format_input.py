import pandas as pd
import os

# Paths for CSV files and output directories
engaging_data_csv = '/Users/mclevesluna/Documents/Thesis/Artefact/data/reactions/engaging_data.csv'
engaging_stories_csv = '/Users/mclevesluna/Documents/Thesis/Artefact/data/reactions/engaging_stories.csv'

# Output directories
combined_output_dir = 'Combined_reactiontxts'
separate_output_dir = 'Separated_reactiontxts'
each_reactionstory_dir = 'Each_reactionstory'
each_reactiondata_dir = 'Each_reactiondata'

# Create directories if they don't exist
if not os.path.exists(combined_output_dir):
    os.makedirs(combined_output_dir)

if not os.path.exists(separate_output_dir):
    os.makedirs(separate_output_dir)

if not os.path.exists(each_reactionstory_dir):
    os.makedirs(each_reactionstory_dir)

if not os.path.exists(each_reactiondata_dir):
    os.makedirs(each_reactiondata_dir)

# Process engaging_data.csv
df_data = pd.read_csv(engaging_data_csv)

# Combined Output for engaging_data.csv
combined_text = ''
for column in df_data.columns[-3:]:
    combined_text += '\n'.join(df_data[column].dropna().astype(str)) + '\n'

combined_file_path = os.path.join(combined_output_dir, 'combined_responses_engaging_data.txt')
with open(combined_file_path, 'w', encoding='utf-8') as file:
    file.write(combined_text)

print("Combined responses from engaging_data.csv have been successfully written to 'combined_responses_engaging_data.txt'.")

# Separate Outputs for engaging_data.csv
for i, column in enumerate(df_data.columns[-3:]):
    question_text = '\n'.join(df_data[column].dropna().astype(str))
    question_file_path = os.path.join(separate_output_dir, f'question_{i + 1}_responses_engaging_data.txt')
    with open(question_file_path, 'w', encoding='utf-8') as file:
        file.write(question_text)

print("Individual question responses from engaging_data.csv have been successfully written to separate text files.")

# Each Row Output for engaging_data.csv
for index, row in df_data.iterrows():
    row_text = '\n'.join(row.dropna().astype(str))
    row_file_path = os.path.join(each_reactiondata_dir, f'engaging_data_row_{index + 1}.txt')
    with open(row_file_path, 'w', encoding='utf-8') as file:
        file.write(row_text)

print("Each row from engaging_data.csv has been successfully written to separate text files.")


# Process engaging_stories.csv
df_stories = pd.read_csv(engaging_stories_csv)

# Identify question columns in engaging_stories.csv
question_columns = [col for col in df_stories.columns if 'What do you understand or interpret from this piece?' in col or
                    'How would you describe how this piece made you feel?' in col or
                    'Did you relate to this text in any way?' in col]

# Combined Output for engaging_stories.csv
combined_text_stories = ''
for column in question_columns:
    combined_text_stories += '\n'.join(df_stories[column].dropna().astype(str)) + '\n'

combined_file_path_stories = os.path.join(combined_output_dir, 'combined_responses_engaging_stories.txt')
with open(combined_file_path_stories, 'w', encoding='utf-8') as file:
    file.write(combined_text_stories)

print("Combined responses from engaging_stories.csv have been successfully written to 'combined_responses_engaging_stories.txt'.")

# Separate Outputs for engaging_stories.csv
# Create a dictionary to group columns by question type
question_responses = {
    "interpretation": [],
    "feeling": [],
    "relation": []
}

# Group responses by the three question types
for column in question_columns:
    if 'What do you understand or interpret from this piece?' in column:
        question_responses['interpretation'].extend(df_stories[column].dropna().astype(str).tolist())
    elif 'How would you describe how this piece made you feel?' in column:
        question_responses['feeling'].extend(df_stories[column].dropna().astype(str).tolist())
    elif 'Did you relate to this text in any way?' in column:
        question_responses['relation'].extend(df_stories[column].dropna().astype(str).tolist())

# Write each type of question response to a separate file
for question_type, responses in question_responses.items():
    question_file_path = os.path.join(separate_output_dir, f'{question_type}_responses_engaging_stories.txt')
    with open(question_file_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(responses))

print("Individual question responses from engaging_stories.csv have been successfully written to separate text files.")

# Each Row Output for engaging_stories.csv
for index, row in df_stories.iterrows():
    row_text = '\n'.join(row.dropna().astype(str))
    row_file_path = os.path.join(each_reactionstory_dir, f'engaging_stories_row_{index + 1}.txt')
    with open(row_file_path, 'w', encoding='utf-8') as file:
        file.write(row_text)

print("Each row from engaging_stories.csv has been successfully written to separate text files.")
