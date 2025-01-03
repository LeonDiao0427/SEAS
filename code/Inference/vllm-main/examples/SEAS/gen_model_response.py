import json
import argparse
# import ray

from vllm import LLM, SamplingParams, sampling_params

def get_prompts(path: str):
    dat = []
    with open(path, "r") as f:
        datas = f.readlines()
        dat = [json.loads(line) for line in datas]
    return dat

def get_sampling_params(temperature=0.0, top_p=1.0, top_k=-1, presence_penalty=0.0, frequency_penalty=0.0):
    return SamplingParams(temperature=temperature,
                          top_p=top_p,
                          top_k=top_k,
                          presence_penalty=presence_penalty,
                          frequency_penalty=frequency_penalty,
                          max_tokens=2048)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-path", type=str, required=True)
    parser.add_argument("--model-path", type=str, required=True)
    parser.add_argument("--save-path", type=str, required=True)
    parser.add_argument("--prompt-prefix", type=str, default="")
    parser.add_argument("--prompt-suffix", type=str, default="")
    parser.add_argument("--tp", type=int, default=1)
    parser.add_argument("--dtype", type=str, default='float16', choices=['float32', 'float16', 'bfloat16'])
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float, default=1.0)
    parser.add_argument("--top-k", type=int, default=-1)
    parser.add_argument("--presence-penalty", type=float, default=0.0)
    parser.add_argument("--frequency-penalty", type=float, default=0.0)
    args = parser.parse_args()
    return args

def create_prompt(x, args):
        return args.prompt_prefix + str(x["prompt"]) + args.prompt_suffix

if __name__ == "__main__":
    args = get_args()
    ray.init()
    dat = get_prompts(args.data_path)
    sampling_params = get_sampling_params(args.temperature, args.top_p, args.top_k, args.presence_penalty, args.frequency_penalty)
    llm = LLM(model=args.model_path,
              tokenizer=args.model_path,
              tensor_parallel_size=args.tp,
              dtype=args.dtype)

    prompts = [create_prompt(x, args) for x in dat]

    print(f"begin general {len(prompts)} samples...")
    outputs = llm.generate(prompts, sampling_params)
    with open(args.save_path + '.json', "w", encoding='utf-8') as f:
        # Print the outputs.
        for item, output in zip(dat, outputs):
            prompt = output.prompt
            generated_text = output.outputs[0].text
            item['response'] = generated_text
            # item['input'] = prompts
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
            f.flush()
