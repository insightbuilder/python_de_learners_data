from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse

from modal import Image, Stub, asgi_app

#this is fastapi app
web_app = FastAPI()
#this is modal app
stub = Stub('super-app')

image = Image.debian_slim().pip_install("boto3")

@web_app.post("/foo")
async def foo(request: Request):
    body = await request.json()
    return body


@web_app.get("/bar")
async def bar(arg="world"):
    return HTMLResponse(f"<h1>Hello Fast {arg}!</h1>")

#the stub is used with the image and the asgi_app
@stub.function(image=image)
@asgi_app()
def fastapi_app():
    return web_app
