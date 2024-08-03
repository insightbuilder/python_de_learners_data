from modal import Image, SharedVolume, Stub
import random
from typing import Optional
from pathlib import Path

from typing import Optional

from modal import gpu, method
from modal.cls import ClsMixin

VOL_MOUNT_PATH = Path("/vol")

WANDB_PROJECT = ""

MODEL_PATH = "/model"


def download_models():
    from transformers import LlamaForCausalLM, LlamaTokenizer

    model_name = "openlm-research/open_llama_7b_400bt_preview"

    model = LlamaForCausalLM.from_pretrained(model_name)
    model.save_pretrained(MODEL_PATH)

    tokenizer = LlamaTokenizer.from_pretrained(model_name)
    tokenizer.save_pretrained(MODEL_PATH)

openllama_image = (
    Image.micromamba()
    .micromamba_install(
        "cudatoolkit=11.7",
        "cudnn=8.1.0",
        "cuda-nvcc",
        channels=["conda-forge", "nvidia"],
    )
    .apt_install("git")
    .pip_install(
        "accelerate==0.18.0",
        "bitsandbytes==0.37.0",
        "bitsandbytes-cuda117==0.26.0.post2",
        "datasets==2.10.1",
        "fire==0.5.0",
        "gradio==3.23.0",
        "peft @ git+https://github.com/huggingface/peft.git@e536616888d51b453ed354a6f1e243fecb02ea08",
        "transformers @ git+https://github.com/huggingface/transformers.git@a92e0ad2e20ef4ce28410b5e05c5d63a5a304e65",
        "torch==2.0.0",
        "torchvision==0.15.1",
        "sentencepiece==0.1.97",
    )
    .run_function(download_models)
    .pip_install("wandb==0.15.0")
)

stub = Stub(name="ollama-bot", image=openllama_image)

output_vol = SharedVolume(cloud="gcp").persist("slack-finetune-vol")


def generate_prompt(user, input, output=""):
    return f"""You are {user}, employee at a fast-growing startup. Below is an input conversation that takes place in the company's internal Slack. Write a response that appropriately continues the conversation.

### Input:
{input}

### Response:
{output}"""

def user_data_path(user: str, team_id: Optional[str] = None) -> Path:
    return VOL_MOUNT_PATH / (team_id or "data") / user / "data.json"

def user_model_path(user: str, team_id: Optional[str] = None, checkpoint: Optional[str] = None) -> Path:
    path = VOL_MOUNT_PATH / (team_id or "data") / user
    if checkpoint:
        path = path / checkpoint
    return path

if stub.is_inside():
    import sys
    import torch
    from peft import PeftModel
    from transformers import LlamaForCausalLM, LlamaTokenizer
    from transformers import GenerationConfig

@stub.cls(
    gpu=gpu.T4,
    shared_volumes={VOL_MOUNT_PATH: output_vol},
)
class OpenLlamaModel(ClsMixin):
    def __init__(self):
        load_8bit = False
        device = "cuda"

        self.tokenizer = LlamaTokenizer.from_pretrained(MODEL_PATH)

        model = LlamaForCausalLM.from_pretrained(
            MODEL_PATH,
            load_in_8bit=load_8bit,
            torch_dtype=torch.float16,
            device_map="auto",
        )
        # unwind broken decapoda-research config
        model.config.pad_token_id = self.tokenizer.pad_token_id = 0  # unk
        model.config.bos_token_id = 1
        model.config.eos_token_id = 2

        if not load_8bit:
            model.half()  # seems to fix bugs for some users.

        model.eval()
        if torch.__version__ >= "2" and sys.platform != "win32":
            model = torch.compile(model)
        self.model = model
        self.device = device

    @method()
    def generate(
        self,
        input: str,
        max_new_tokens=128,
        **kwargs,
    ):
        prompt = generate_prompt(input)
        inputs = self.tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self.device)
        # tokens = self.tokenizer.convert_ids_to_tokens(input_ids[0])
        # print(tokens)
        generation_config = GenerationConfig(
            **kwargs,
        )
        with torch.no_grad():
            generation_output = self.model.generate(
                input_ids=input_ids,
                generation_config=generation_config,
                return_dict_in_generate=True,
                output_scores=True,
                max_new_tokens=max_new_tokens,
            )

        s = generation_output.sequences[0]
        output = self.tokenizer.decode(s)
        return output.split("### Response:")[1].strip()

@stub.local_entrypoint()
def main(user: str):
    inputs = [
        "Tell me about alpacas.",
        "Tell me about the president of Mexico in 2019.",
        "What should we do next? Who should work on this?",
        "What are your political views?",
        "What did you work on yesterday?",
        "@here is anyone in the office?",
        "What did you think about the last season of Silicon Valley?",
        "Who are you?",
    ]
    model = OpenLlamaModel.remote(user, "T02B9UTL2E4")
    # model = OpenLlamaModel.remote(user, "T031JJZ7Q6T")
    for input in inputs:
        input = "U02ASG53F9S: " + input
        print(input)
        print(
            model.generate(
                input,
                do_sample=True,
                temperature=0.3,
                top_p=0.85,
                top_k=40,
                num_beams=1,
                max_new_tokens=600,
                repetition_penalty=1.2,
                )
            )
