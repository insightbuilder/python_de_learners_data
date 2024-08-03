from modal import Stub, web_endpoint

stub = Stub()

@stub.function()
@web_endpoint()
def f():
    return "This is from inside!"

@stub.function()
@web_endpoint()
def square(x: int):
    return {"square": x**2}


