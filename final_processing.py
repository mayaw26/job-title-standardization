import pandas as pd
from transformers import T5Tokenizer, T5ForConditionalGeneration
from datetime import datetime

# Load the data
input_path = ""
data = pd.read_excel(input_path)

# Load the trained model and tokenizer
model = T5ForConditionalGeneration.from_pretrained("")
tokenizer = T5Tokenizer.from_pretrained("")

# Define batch size
batch_size = 250  # Adjust as needed based on system capacity
num_batches = (len(data) + batch_size - 1) // batch_size  # Calculate number of batches

# Initialize a list to store predictions
predictions = []

# Process data in batches
for batch_num in range(num_batches):
    try:
        # Get the batch start and end indices
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(data))
        
        # Get the current batch of job titles
        batch = data["AFTER_PREPROCESSING"].iloc[start_idx:end_idx]
        
        # Pre-process the batch: Replace non-strings or NaN with empty strings
        batch = batch.fillna("").astype(str)
        
        # Tokenize the batch
        inputs = tokenizer(batch.tolist(), return_tensors="pt", padding=True, truncation=True)
        
        # Generate predictions for the batch
        output_ids = model.generate(inputs.input_ids, max_new_tokens=50)
        
        # Decode the outputs and extend the predictions list
        batch_predictions = [tokenizer.decode(output, skip_special_tokens=True) for output in output_ids]
        predictions.extend(batch_predictions)
        
        # Print progress
        print(f"Processed batch {batch_num + 1} of {num_batches}")
    
    except Exception as e:
        print(f"Error in batch {batch_num + 1}: {e}")
        break  # Stop processing if an error occurs

# Add predictions to a new column in the DataFrame
data['MODEL_OUTPUT'] = predictions + [None] * (len(data) - len(predictions))  # Fill unmatched rows with None

# Save the updated DataFrame to a new file with a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_path = f"MODEL_OUTPUT_{timestamp}.xlsx"
data.to_excel(output_path, index=False)

print(f"Model output saved to: {output_path}")