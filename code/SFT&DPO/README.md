## Requirement

| Mandatory    | Minimum | Recommend |
| ------------ | ------- | --------- |
| python       | 3.8     | 3.10      |
| torch        | 1.13.1  | 2.2.0     |
| transformers | 4.37.2  | 4.39.3    |
| datasets     | 2.14.3  | 2.18.0    |
| accelerate   | 0.27.2  | 0.28.0    |
| peft         | 0.9.0   | 0.10.0    |
| trl          | 0.8.1   | 0.8.1     |

| Optional     | Minimum | Recommend |
| ------------ | ------- | --------- |
| CUDA         | 11.6    | 12.2      |
| deepspeed    | 0.10.0  | 0.14.0    |
| bitsandbytes | 0.39.0  | 0.43.0    |
| flash-attn   | 2.3.0   | 2.5.6     |

### Hardware Requirement

\* *estimated*

| Method            | Bits |   7B  |  13B  |  30B  |   70B  |  8x7B |  8x22B |
| ----------------- | ---- | ----- | ----- | ----- | ------ | ----- | ------ |
| Full              | AMP  | 120GB | 240GB | 600GB | 1200GB | 900GB | 2400GB |
| Full              |  16  |  60GB | 120GB | 300GB |  600GB | 400GB | 1200GB |
| Freeze            |  16  |  20GB |  40GB |  80GB |  200GB | 160GB |  400GB |
| LoRA/GaLore/BAdam |  16  |  16GB |  32GB |  64GB |  160GB | 120GB |  320GB |
| QLoRA             |   8  |  10GB |  20GB |  40GB |   80GB |  60GB |  160GB |
| QLoRA             |   4  |   6GB |  12GB |  24GB |   48GB |  30GB |   96GB |
| QLoRA             |   2  |   4GB |   8GB |  16GB |   24GB |  18GB |   48GB |

## Getting Started
Model init
```
cd /examples/full_multi_gpu
bash single_node_sft_llama3.sh
```

Model update
```
cd /examples/full_multi_gpu
bash single_node_dpo_llama3_tgt.sh
bash single_node_dpo_llama3_atk.sh
```

### Data Preparation

Please refer to [data/README.md](data/README.md) for checking the details about the format of dataset files. You can either use datasets on HuggingFace / ModelScope hub or load the dataset in local disk.

> [!NOTE]
> Please update `data/dataset_info.json` to use your custom dataset.

