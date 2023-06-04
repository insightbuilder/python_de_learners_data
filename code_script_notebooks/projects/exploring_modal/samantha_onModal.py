import os
import re
from dataclasses import dataclass
from typing import List

import modal

stub = modal.Stub(name="samantha_on_modal")
MODEL_NAME = "ehartford/samantha-7b"
CACHE_DIR = "/cache"

stub["deep_learning_image"] = modal.Image.debian_slim().pip_install(
    "transformers==4.28.1", "torch", "sentencepiece"
)

volume = modal.SharedVolume().persist("samantha-modal-cpu")

if stub.is_inside(stub["deep_learning_image"]):
    from transformers import AutoTokenizer, LlamaForCausalLM

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME,
                                              cache_dir=CACHE_DIR)
    model = LlamaForCausalLM.from_pretrained(MODEL_NAME,
                                                 cache_dir=CACHE_DIR)

@stub.function(
    image=stub["deep_learning_image"],
    gpu=False,
    shared_volumes={CACHE_DIR: volume},
    memory=16384,
)
def generate_article(text: str) -> str:
    print(f"Generating article with with prompt: {text}.")

    # summarize text
    batch = tokenizer(text, return_tensors="pt").to("cpu")
    translated = model.generate(batch.input_ids, max_length=200)
    gen_text = tokenizer.batch_decode(translated, 
                                      skip_special_tokens=True,
                                      clean_up_tokenization_spaces=False)[0]

    return gen_text

@stub.local_entrypoint()
def main(prompt: str):
    print("Generation Starting: \n")
    output = generate_article.call(prompt)
    print(output)
