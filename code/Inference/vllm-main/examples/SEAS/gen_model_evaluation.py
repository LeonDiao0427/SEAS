import ray
import json
import argparse

from enum import Enum
from vllm import LLM, SamplingParams, sampling_params
from prompt_format_utils import build_custom_prompt, create_conversation, LLAMA_GUARD_2_CATEGORY, LLAMA_GUARD_2_CATEGORY_SHORT_NAME_PREFIX, PROMPT_TEMPLATE_2,ConversationTurn


class LlamaGuardVersion(Enum):
    LLAMA_GUARD_1 = "Llama Guard 1"
    LLAMA_GUARD_2 = "Llama Guard 2"

class AgentType(Enum):
    AGENT = "Agent"
    USER = "User"

def get_prompts(path: str):
    dat = []
    with open(path, "r") as f:
        datas = f.readlines()
        dat = [json.loads(line) for line in datas]
        # prompts = ["[Round 0] USER:"+json.loads(line)['prompt']+" ASSISTANT:" for line in datas]
    return dat


def get_sampling_params(tokenizer, temperature=0.0, top_p=1.0, top_k=-1, presence_penalty=0.0, frequency_penalty=0.0):
    return SamplingParams(temperature=temperature,
                          top_p=top_p,
                          top_k=top_k,
                          presence_penalty=presence_penalty,
                          frequency_penalty=frequency_penalty,
                          stop_token_ids=[tokenizer.eos_token_id,tokenizer.convert_tokens_to_ids("<|eot_id|>")], 
                          max_tokens=2048)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--model-path", type=str, required=True)
    parser.add_argument("--save-path", type=str, required=True)
    parser.add_argument("--tp", type=int, default=1)  # 8
    parser.add_argument("--dtype", type=str, default='float16', choices=['float32', 'float16', 'bfloat16'])
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--top-k", type=int, default=-1)
    parser.add_argument("--presence-penalty", type=float, default=0.0)
    parser.add_argument("--frequency-penalty", type=float, default=0.0)
    parser.add_argument("--total-split", type=int, default=1)
    parser.add_argument("--cur-split", type=int, default=1)
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    ray.init()
    dat = get_prompts(args.data_path)
    # sampling_params = get_sampling_params(args.temperature, args.top_p, args.top_k, args.presence_penalty, args.frequency_penalty)
    llm = LLM(model=args.model_path,
              tokenizer=args.model_path,
              tensor_parallel_size=args.tp,
              dtype=args.dtype)
    tokenizer = llm.get_tokenizer()
    sampling_params = get_sampling_params(tokenizer,args.temperature, args.top_p, args.top_k, args.presence_penalty, args.frequency_penalty)

    if args.total_split >= 1:
        num_samples = (len(dat) + args.total_split - 1) // args.total_split
        start_id = (args.cur_split - 1) * num_samples
        end_id = min(len(dat), args.cur_split * num_samples)
        dat = dat[start_id: end_id]

   
    user = [x['atk_output'] for x in dat]
    agent = [x['response'] for x in dat]
    # conversations = [create_conversation([prompt]) for prompt in prompts]

    conversations = [[ConversationTurn(u, AgentType.USER), ConversationTurn(a, AgentType.AGENT)] for u, a in zip(user, agent)]

    # prompts = [build_default_prompt(AgentType.USER, conversation, LlamaGuardVersion.LLAMA_GUARD_2) for conversation in conversations]
    prompts = [
            build_custom_prompt(
                AgentType.AGENT, 
                conversation, 
                LLAMA_GUARD_2_CATEGORY,  
                LLAMA_GUARD_2_CATEGORY_SHORT_NAME_PREFIX, 
                PROMPT_TEMPLATE_2,  # 确保这是一个 Template 对象
                with_policy=True
            ) for conversation in conversations
        ]
    

    print(f"begin general {len(prompts)} samples...")
    outputs = llm.generate(prompts, sampling_params)
    with open(args.save_path + str(args.cur_split) + '_' + str(args.total_split) + '.json', "w") as f:
        # Print the outputs.
        for item, output in zip(dat, outputs):
            prompt = output.prompt
            generated_text = output.outputs[0].text
            item['evaluation'] = generated_text
            # item['to_model'] = prompt
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            f.flush()
