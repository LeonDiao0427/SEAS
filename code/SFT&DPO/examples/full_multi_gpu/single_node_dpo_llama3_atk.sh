#!/bin/bash
cd ./examples/full_multi_gpu
python3 network.py

deepspeed --num_gpus 8 ../../src/train_bash.py \
    --deepspeed ../deepspeed/ds_z3_config.json \
    --stage dpo \
    --do_train \
    --model_name_or_path "model_name_or_path" \
    --dataset SEAS_dpo_atk \
    --dataset_dir ../../data \
    --template llama3 \
    --finetuning_type full \
    --output_dir "output_path" \
    --overwrite_cache \
    --overwrite_output_dir \
    --cutoff_len 2048 \
    --preprocessing_num_workers 1 \
    --per_device_train_batch_size 2 \
    --gradient_accumulation_steps 16 \
    --lr_scheduler_type cosine \
    --logging_steps 10 \
    --warmup_steps 20 \
    --save_steps 100 \
    --learning_rate 5e-6 \
    --num_train_epochs 1.0 \
    --max_samples 200000 \
    --ddp_timeout 180000000 \
    --seed 42 \
    --plot_loss \
    --report_to tensorboard \
    --plot_loss \
    --fp16