##### Getting Started(vLLM)

Visit our [documentation](https://vllm.readthedocs.io/en/latest/) to get started.
- [Installation](https://vllm.readthedocs.io/en/latest/getting_started/installation.html)
- [Quickstart](https://vllm.readthedocs.io/en/latest/getting_started/quickstart.html)
- [Supported Models](https://vllm.readthedocs.io/en/latest/models/supported_models.html)

##### You can install vLLM using pip:
```
# (Recommended) Create a new conda environment.
conda create -n myenv python=3.9 -y
conda activate myenv
# Install vLLM with CUDA 12.1.
pip install vllm
```
##### Generate Model Responses:
Fill in your model path, data save path and other parameters in `run_gen_response.sh` and run this script.
```
bash run_gen_response.sh
```

##### Generate Safe Classifer evaluations:
Fill in your model path, data save path and other parameters in `run_gen_evaluation.sh` and run this script.
```
bash run_gen_evaluation.sh
```