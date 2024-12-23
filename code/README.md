## Description:
In the SEAS pipeline, we utilized some open-source code. We will acknowledge and cite them in the camera-ready version.
Throughout the entire pipeline, we utilize SFT to initialize both the Red Team model and the Target model. Inference is used for the Ted Team model to generate adversarial prompts, for the Target model to produce responses, and for the safe classifier to carry out evaluations. We employ DPO for the iterative updates of both the Red Team model and the Target model.

## Framework
- `Inference`: Generation model response and safe classifier evaluation.
- `SFT&DPO`: Initialize the model, iteratively update the model.
- `Judge`: Generation model ASR score, SEAS harmless test score.
- `Data_iteration`: Data filtering, constructing paired data.


## Getting Started

### Step 1 Initialization Stage.

You need to navigate to the SFT&DPO/examples/full_multi_gpu directory and run the single_node_sft_llama3.sh script. For detailed instructions, please refer to the README in the SFT&DPO directory. Once you have configured the necessary settings, you can run the initialization using the following command:
```
cd SFT&DPO/examples/full_multi_gpu
bash single_node_sft_llama3.sh
```

### Step 2 Attack Stage.
You can conduct model adversarial attacks in the Inference folder. Specifically, you will generate model responses and perform model security evaluation. Detailed configuration information can be found in the README within the Inference folder. After setting up the necessary configurations (details in Inference/README.md), you can run the adversarial attack using the following command:
```
cd Inference
bash run_gen_response.sh
bash run_gen_evaluation.sh
```

### Step 3 Adversarial Optimization Stage.
First, you need to construct the DPO pair data. In the Data_iteration folder, you can generate the relevant data using the following command:
```
cd Data_iteration
python make_atk_dpo.py
python make_tgt_dpo.py
```
Next, provide the data address and relevant configuration information as detailed in SFT&DPO/README.md. Afterward, you can run the model iteration using the following command:
```
cd SFT&DPO/examples/full_multi_gpu
bash single_node_dpo_llama3_atk.sh
bash single_node_dpo_llama3_tgt.sh
```


### Step 4 Evaluation.
You can find the calculation of ASR and the evaluation on the SEAS harmless test set in the Evaluation section. For detailed information, please refer to Evaluation/README. Alternatively, you can directly calculate the ASR using the following command:
```
cd Evaluation
python ASR.py
```