from llmtuner import run_exp


run_exp(dict(
  stage="sft",
  do_train=True,
  model_name_or_path="",
  dataset="",
  template="llama3",
  finetuning_type="full",
  output_dir="",
  per_device_train_batch_size=2,
  gradient_accumulation_steps=4,
  lr_scheduler_type="cosine",
  logging_steps=10,
  warmup_ratio=0.1,
  save_steps=1000,
  learning_rate=5e-5,
  num_train_epochs=3.0,
  max_samples=500,
  max_grad_norm=1.0,
  quantization_bit=4,
  use_unsloth=True,
  fp16=True,
))