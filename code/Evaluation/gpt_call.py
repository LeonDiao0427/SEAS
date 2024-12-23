# encoding=utf8
import json
import requests
from typing import List
import pandas as pd
from tqdm import tqdm
import random
import sys
import concurrent.futures
import os
import tenacity
random.seed(2024)

AppId = "" 
MODEL_NAME = ["", ""] 
GEN_CONFIG = {"max_tokens": 2048,}


def call_gpt4(prompt):
    messages = generate_messages(prompt)
    r = tenacity.Retrying(stop=tenacity.stop_after_attempt(10),
                          wait=tenacity.wait_random_exponential(min=5, max=30),
                          reraise=True)
    eval_result = r(create_chat_completion, messages, model=MODEL_NAME[0], **GEN_CONFIG)
    return messages, eval_result[0]

def create_chat_completion(messages, functions=None, function_call=None, model="", **kwargs):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AppId}"
    }
    json_data = {"model": model, "messages": messages}
    json_data.update(kwargs)
    try:
        response = requests.post(MODEL_NAME[1], headers=headers, json=json_data)
        response.raise_for_status()  
        res = response.json()  
        print(f"API response: {json.dumps(res, indent=2)}")
        if 'choices' in res and isinstance(res['choices'], list):
            return [choice['message']['content'] for choice in res['choices']]
        else:
            raise ValueError("Response format is not as expected. 'choices' key not found")
    except requests.exceptions.RequestException as req_err:
        print(f"Request failed: {req_err}")
        raise req_err
    except ValueError as val_err:
        print(f"Response format error: {val_err}")
        raise val_err
    except Exception as e:
        print(f"Parsing the GPT return value failed，input={messages}, response={response.text}, return={response}")
        raise e  # Error

def generate_messages(prompt):
    return [{'role': 'user', 'content': prompt}]

if __name__ == "__main__":
    test_prompt = "1+1=?"
    try:
        messages, response = call_gpt4(test_prompt)
        print(f"Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
