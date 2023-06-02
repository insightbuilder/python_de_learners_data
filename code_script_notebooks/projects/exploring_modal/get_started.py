import modal

#Create a stub to connect with modal exec point
stub = modal.Stub("gpt2-example")

#make the function part of the modal
@stub.function()
def square(x):
    print("This code is running on a remote worker!")
    return x**2

#calling this from local ???
@stub.local_entrypoint()
def main():
    print("the square is", square.call(42))
