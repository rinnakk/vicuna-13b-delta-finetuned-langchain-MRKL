# vicuna-13b-delta-finetuned-langchain-MRKL

vicuna-13b-delta-finetuned-langchain-MRKL is a Vicuna-13B v1.1 model fine-tuned using lm-sys/FastChat.

## Model Weights

python3 apply_delta.py --base /path/to/model_weights/llama-13b --target rinna-vicuna-13b-finetuned-langchain-MRKL --delta /path/to/model_weights/vicuna-13b-delta-finetuned-langchain-MRKL


## Model usage


## Training data

python3 format.py 

**NOTE**:
we really only use 15 examples for finetune, but we mix data (sharegpt + 32*my.json + moss-003-sft-data).
And only train one epoch with mixed data.

