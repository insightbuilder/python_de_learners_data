from modal import Image, gpu, Stub, method, web_endpoint

IMAGE_MODEL_DIR = "/model"

def download_model():
    from huggingface_hub import snapshot_download

    model_name = "TheBloke/falcon-40b-instruct-GPTQ"
    snapshot_download(model_name, local_dir=IMAGE_MODEL_DIR)

image = (
    Image.debian_slim(python_version="3.10")
    .apt_install("git")
    .pip_install(
        "huggingface_hub==0.14.1",
        "transformers @ git+https://github.com/huggingface/transformers.git@f49a3453caa6fe606bb31c571423f72264152fce",
        "auto-gptq @ git+https://github.com/PanQiWei/AutoGPTQ.git@b5db750c00e5f3f195382068433a3408ec3e8f3c",
        "einops==0.6.1",
    )
    .run_function(download_model)
)

stub = Stub(name="example-falcon-gptq", image=image)

@stub.cls(gpu=gpu.A10G(), 
          timeout=60 * 10, 
          container_idle_timeout=60 * 8)
class Falcon40BGPTQ:
    def __enter__(self):
        from transformers import AutoTokenizer
        from auto_gptq import AutoGPTQForCausalLM

        self.tokenizer = AutoTokenizer.from_pretrained(
            IMAGE_MODEL_DIR, use_fast=True
        )
        print("Loaded tokenizer.")

        self.model = AutoGPTQForCausalLM.from_quantized(
            IMAGE_MODEL_DIR,
            trust_remote_code=True,
            use_safetensors=True,
            device_map="auto",
            use_triton=False,
            strict=False,
        )
        print("Loaded model.")

    @method()
    def generate(self, prompt: str):
        from threading import Thread
        from transformers import TextIteratorStreamer

        inputs = self.tokenizer(prompt, return_tensors="pt")
        streamer = TextIteratorStreamer(
            self.tokenizer, skip_special_tokens=True
        )
        generation_kwargs = dict(
            inputs=inputs.input_ids.cuda(),
            attention_mask=inputs.attention_mask,
            temperature=0.1,
            max_new_tokens=512,
            streamer=streamer,
        )

        # Run generation on separate thread to enable response streaming.
        thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
        thread.start()
        for new_text in streamer:
            yield new_text

        thread.join()

prompt_template = (
    "A chat between a curious human user and an artificial intelligence assistant. The assistant give a helpful, detailed, and accurate answer to the user's question."
    "\n\nUser:\n{}\n\nAssistant:\n"
)

@stub.local_entrypoint()
def cli(prompt:str):
    question = prompt
    model = Falcon40BGPTQ()
    for text in model.generate.call(prompt_template.format(question)):
        print(text, end="", flush=True)

@stub.function(timeout=600)
@web_endpoint()
def get(question: str):
    from fastapi.responses import StreamingResponse
    from itertools import chain

    model = Falcon40BGPTQ()
    return StreamingResponse(
        chain(
            ("Loading model. This usually takes around 20s ...\n\n"),
            model.generate.call(prompt_template.format(question)),
        ),
        media_type="text/event-stream",
    )

