MODEL_PATH="your model path"
SAVE_PATH="save path"
MODEL_ID="your model name"
export CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7

cd vllm-main/examples/SEAS
bash ./gen_model_response.sh \
        --model-path $MODEL_PATH \
        --save-path $SAVE_PATH \
        --model-id $MODEL_ID \
        --prompt_prefix "" \
        --prompt_suffix "" \
        --tp 8
# # &&

