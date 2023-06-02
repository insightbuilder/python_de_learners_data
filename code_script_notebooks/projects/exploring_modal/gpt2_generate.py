import modal

stub = modal.Stub("example-gpt2")


volume = "/run/media/solverbot/repoA/opensource_models"

def download_model():
    from transformers import pipeline

    generator = pipeline("text-generation",model='gpt2')

    generator.save_pretrained(volume)

@stub.function(
        image=modal.Image.debian_slim()
        .pip_install("torch","transformers")
        .run_function(download_model)
        )
def generate_text(prompt: str):
    from transformers import pipeline

    generator = pipeline("text-generation",model=volume)
    return generator(prompt, do_sample=True, 
                     min_length=50, max_length=250)[0]['generated_text']

@stub.local_entrypoint()
def main(prompt: str = ''):
    generation = generate_text.call(prompt=prompt or "What is meaning of life")
    print(generation)
