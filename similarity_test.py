import pandas as pd
import spacy
import numpy as np

file_path = ""
output_path = ""

# Load spaCy
nlp = spacy.load("en_core_web_lg")

# Define function to calculate cosine similarity
def cosine_similarity(input_text, output_text):
    doc_input = nlp(input_text)
    doc_output = nlp(output_text)
    
    # Skip calculation if either vector is empty
    if not doc_input.vector_norm or not doc_output.vector_norm:
        return 0  # Return 0 similarity for invalid cases
    
    return doc_input.similarity(doc_output)

# Load the dataset
filtered_df = pd.read_excel(file_path)
print(f"Filtered dataset loaded successfully. Total rows: {len(filtered_df)}")
print("Columns in the dataset:", filtered_df.columns)

# Ensure required columns exist
if 'AFTER_PREPROCESSING' not in filtered_df.columns or 'MODEL_OUTPUT' not in filtered_df.columns:
    raise ValueError("Required columns 'AFTER_PREPROCESSING' or 'MODEL_OUTPUT' are missing.")
else:
    print("Required columns found! Ready for processing")

# Filter out rows with missing values in 'AFTER_PREPROCESSING' or 'MODEL_OUTPUT'
filtered_df = filtered_df.dropna(subset=['AFTER_PREPROCESSING', 'MODEL_OUTPUT'])
print(f"Rows after filtering: {len(filtered_df)}")

# Ensure 'COSINE_SIMILARITY' column exists
if 'COSINE_SIMILARITY' not in filtered_df.columns:
    filtered_df['COSINE_SIMILARITY'] = float('nan')

# Process the entire dataset
print(f"Processing the entire dataset with {len(filtered_df)} rows...")

for index, row in filtered_df.iterrows():
    try:
        input_text = row['AFTER_PREPROCESSING']
        output_text = row['MODEL_OUTPUT']
        similarity = cosine_similarity(input_text, output_text)
        filtered_df.at[index, 'COSINE_SIMILARITY'] = similarity
    except Exception as e:
        print(f"Error at row {index}: {e}")
        filtered_df.at[index, 'COSINE_SIMILARITY'] = 0  # Default to 0 for errors

# Filter data into final sheets based on similarity scores
final_data = filtered_df[filtered_df['COSINE_SIMILARITY'] >= 0.95]
tentative_data = filtered_df[(filtered_df['COSINE_SIMILARITY'] >= 0.93) & (filtered_df['COSINE_SIMILARITY'] < 0.95)]
excluded_data = filtered_df[filtered_df['COSINE_SIMILARITY'] < 0.93]

# Additional condition: Move entries from final_data to tentative_data
condition_to_move = (final_data['COSINE_SIMILARITY'] < 1) & (~final_data['MODEL_OUTPUT'].str.contains(","))
entries_to_move = final_data[condition_to_move]

# Update final_data and tentative_data accordingly
final_data = final_data[~condition_to_move]
tentative_data = pd.concat([tentative_data, entries_to_move])

# Save results to separate sheets
try:
    with pd.ExcelWriter(output_path, engine='openpyxl', mode='w') as writer:
        # Save each DataFrame if it has rows
        if not final_data.empty:
            final_data.to_excel(writer, sheet_name="Final Data (0.95+)", index=False)
        if not tentative_data.empty:
            tentative_data.to_excel(writer, sheet_name="Tentative (0.93 - 0.94)", index=False)
        if not excluded_data.empty:
            excluded_data.to_excel(writer, sheet_name="Excluded Data (<0.93)", index=False)
    print(f"Consolidated results saved successfully at {output_path}")
except Exception as e:
    print(f"Error saving results: {e}")
