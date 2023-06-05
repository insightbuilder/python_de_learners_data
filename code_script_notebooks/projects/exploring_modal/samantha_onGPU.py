import os
import re
from dataclasses import dataclass
from typing import List

import modal

stub = modal.Stub(name="samantha_on_gpu")
MODEL_NAME = "ehartford/samantha-7b"
CACHE_DIR = "/cache"

stub["deep_learning_image"] = modal.Image.debian_slim().pip_install(
    "transformers==4.28.1", "torch~=2.0.0", "sentencepiece","accelerate~=0.18.0",
)

volume = modal.SharedVolume().persist("samantha-modal-temp")

if stub.is_inside(stub["deep_learning_image"]):
    from transformers import AutoTokenizer, LlamaForCausalLM
    import torch

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME,
                                              cache_dir=CACHE_DIR)
    model = LlamaForCausalLM.from_pretrained(MODEL_NAME,
                                             cache_dir=CACHE_DIR,
                                             torch_dtype=torch.float16,
                                             device_map='auto')

@stub.function(
    image=stub["deep_learning_image"],
    gpu="T4",
    shared_volumes={CACHE_DIR: volume},
    memory=16384,
)
def generate_article(text: str) -> str:
    print(f"Generating article with with prompt: {text}.")

    # summarize text
    data = tokenizer(text, return_tensors="pt")
    batch = data['input_ids'].to("cuda")
    translated = model.generate(batch, 
                                max_length=200)
    gen_text = tokenizer.batch_decode(translated, 
                                      skip_special_tokens=True,
                                      clean_up_tokenization_spaces=False)[0]

    return gen_text

@stub.local_entrypoint()
def main(prompt: str):
    print("Generation Starting: \n")
    output = generate_article.call(prompt)
    print(output)
