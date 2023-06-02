import urllib.request
import modal

stub = modal.Stub("text-classifier")

volume = modal.SharedVolume().persist("classify_model_vol")
CACHE_PATH = "/root/model_cache"

@stub.function(
    image=modal.Image.debian_slim().pip_install("transformers","torch"),
    shared_volumes={CACHE_PATH: volume},
    retries=3,
)
def classify_text(prompt: str):
    from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english",
                                                    cache_dir=CACHE_PATH)
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased",
                                                                cache_dir=CACHE_PATH)

    inputs = tokenizer(prompt,
                       return_tensors="pt")
    with torch.no_grad():
        logits = model(**inputs).logits

    predicted_class_id = logits.argmax().item()

    predict = model.config.id2label[predicted_class_id]

    return predict

@stub.local_entrypoint()
def main(prompt):
    class_out = classify_text(prompt) 
    print(class_out)

