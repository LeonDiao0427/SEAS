import json

def process_jsonl(file_path, max_length=3000):
    data_dict = {}
    
    # Open the JSONL file for reading
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())  # Parse each line as JSON
            prompt = data.get('prompt', '').strip()  # Get the prompt and strip any whitespace
            atk_output = data.get('atk_output', '').strip()  # Get the attack output and strip any whitespace
            evaluation = data.get('evaluation', '').strip()  # Get the evaluation and strip any whitespace
            
            # Ensure prompt and atk_output are not empty and the length of atk_output is within the max_length
            if prompt and atk_output and len(atk_output) <= max_length:
                if prompt not in data_dict:
                    data_dict[prompt] = {}  # Initialize a nested dictionary for each prompt
                if atk_output not in data_dict[prompt]:
                    # Initialize evaluation counters for each attack output
                    data_dict[prompt][atk_output] = {'unsafe': 0, 'safe': 0}
                
                # Update the counts based on the evaluation result
                if 'unsafe' in evaluation:
                    data_dict[prompt][atk_output]['unsafe'] += 1
                elif 'safe' in evaluation:
                    data_dict[prompt][atk_output]['safe'] += 1

    result_list = []
    # Iterate through the aggregated dictionary to find outputs with the highest unsafe and safe ratios
    for prompt, atk_outputs in data_dict.items():
        max_unsafe_ratio = -1
        max_safe_ratio = -1
        most_unsafe_output = None
        most_safe_output = None

        # Calculate ratio of unsafe and safe for each output
        for atk_output, counts in atk_outputs.items():
            total = counts['unsafe'] + counts['safe']
            if total > 0:
                unsafe_ratio = counts['unsafe'] / total
                safe_ratio = counts['safe'] / total

                # Update the most unsafe output
                if unsafe_ratio > max_unsafe_ratio:
                    max_unsafe_ratio = unsafe_ratio
                    most_unsafe_output = atk_output

                # Update the most safe output
                if safe_ratio > max_safe_ratio:
                    max_safe_ratio = safe_ratio
                    most_safe_output = atk_output

        # Ensure both outputs are different and non-empty before adding to the result list
        if most_unsafe_output and most_safe_output and most_unsafe_output != most_safe_output and most_unsafe_output != "" and most_safe_output != "":
            result_list.append({
                'prompt': prompt,
                'response': [most_unsafe_output, most_safe_output]  # Append the prompt and the two selected responses
            })

    return result_list

file_path = ''  # Path to the JSONL file
result = process_jsonl(file_path)

# Write the result to a new JSON file
with open('output.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
