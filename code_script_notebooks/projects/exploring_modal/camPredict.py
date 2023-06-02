import base64
import io
from pathlib import Path

from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles

from modal import Image, Mount, Secret, SharedVolume, Stub, method, asgi_app

stub = Stub("example-webcam-object-detection")

image = (
    Image.debian_slim()
    .pip_install(
        "Pillow",
        "timm",
        "transformers",
    )
    .apt_install("fonts-freefont-ttf")
)

@stub.cls(
    cpu=4,
    shared_volumes={"/cache": SharedVolume()},
    image=image,
    secret=Secret.from_dict(
        {"TORCH_HOME": "/cache", "TRANSFORMERS_CACHE": "/cache"}
    ),
)

class ObjectDetection:
    def __enter__(self):
        from transformers import DetrFeatureExtractor, DetrForObjectDetection

        self.feature_extractor = DetrFeatureExtractor.from_pretrained(
            "facebook/detr-resnet-50"
        )
        self.model = DetrForObjectDetection.from_pretrained(
            "facebook/detr-resnet-50"
        )

    @method()
    def detect(self, img_data_in):
        # Based on https://huggingface.co/spaces/nateraw/detr-object-detection/blob/main/app.py
        from PIL import Image, ImageColor, ImageDraw, ImageFont

        # Read png from input
        image = Image.open(io.BytesIO(img_data_in)).convert("RGB")

        # Make prediction
        import torch

        inputs = self.feature_extractor(image, return_tensors="pt")
        outputs = self.model(**inputs)
        img_size = torch.tensor([tuple(reversed(image.size))])
        processed_outputs = self.feature_extractor.post_process(
            outputs, img_size
        )
        output_dict = processed_outputs[0]

        # Grab boxes
        keep = output_dict["scores"] > 0.7
        boxes = output_dict["boxes"][keep].tolist()
        scores = output_dict["scores"][keep].tolist()
        labels = output_dict["labels"][keep].tolist()

        # Plot bounding boxes
        colors = list(ImageColor.colormap.values())
        font = ImageFont.truetype(
            "/usr/share/fonts/truetype/freefont/FreeMono.ttf", 18
        )
        output_image = Image.new("RGBA", (image.width, image.height))
        output_image_draw = ImageDraw.Draw(output_image)
        for score, box, label in zip(scores, boxes, labels):
            color = colors[label % len(colors)]
            text = self.model.config.id2label[label]
            box = tuple(map(int, box))
            output_image_draw.rectangle(box, outline=color)
            output_image_draw.text(
                box[:2], text, font=font, fill=color, width=3
            )

        # Return PNG as bytes
        with io.BytesIO() as output_buf:
            output_image.save(output_buf, format="PNG")
            return output_buf.getvalue()

web_app = FastAPI()
static_path = Path(__file__).with_name("webcam").resolve()

@web_app.post("/predict")
async def predict(request: Request):
    # Takes a webcam image as a datauri, returns a bounding box image as a datauri
    body = await request.body()
    img_data_in = base64.b64decode(body.split(b",")[1])  # read data-uri
    img_data_out = ObjectDetection().detect.call(img_data_in)
    output_data = b"data:image/png;base64," + base64.b64encode(img_data_out)
    return Response(content=output_data)

@stub.function(
    mounts=[Mount.from_local_dir(static_path, remote_path="/assets")],
)

@asgi_app()
def fastapi_app():
    web_app.mount("/", StaticFiles(directory="/assets", html=True))
    return web_app
