import json

def process_jsonl(file_path, max_length=3000):
    data_dict = {}
    prompts_set = set()  # Used to detect duplicate collections
    
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())  # Clear possible whitespace characters at the beginning and end of a line
            atk_output = data.get('atk_output', '').strip()  # Clear whitespace characters at both ends of field values
            tgt_output = data.get('tgt_output', '').strip()
            evaluation = data.get('evaluation', '').strip()
            
            # Ensure that neither atk_output nor tgt_output is empty and that tgt_output does not exceed the maximum length
            if atk_output and tgt_output and len(tgt_output) <= max_length:
                if atk_output not in data_dict:
                    data_dict[atk_output] = [None, None]
                
                if 'safe' in evaluation and data_dict[atk_output][0] is None:
                    data_dict[atk_output][0] = tgt_output
                elif 'unsafe' in evaluation and data_dict[atk_output][1] is None:
                    data_dict[atk_output][1] = tgt_output

    result_list = []
    for prompt, responses in data_dict.items():
        if prompt not in prompts_set and None not in responses:  # Check for repetition and no empty elements in the responses
            result_list.append({
                'prompt': prompt,
                'response': responses
            })
            prompts_set.add(prompt)  # Added to the collection to avoid duplication

    return result_list

# 调用函数处理文件
file_path = ''
result = process_jsonl(file_path)

# 输出结果到一个新的JSON文件
with open('', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
