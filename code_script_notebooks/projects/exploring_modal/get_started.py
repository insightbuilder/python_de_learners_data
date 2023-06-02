import modal

#Create a stub to connect with modal exec point
stub = modal.Stub("gpt2-example")

#make the function part of the modal
@stub.function()
def add_num(x,y):
    print("This code is running on a remote worker!")
    return x + y 

#make the function part of the modal
@stub.function()
def square(x):
    print("This code is running on a remote worker!")
    return x**2

#calling this from local ???
@stub.local_entrypoint()
def main(num1, num2):
    print("the square is", square.call(42))
    print(f"The sum of {num1} and {num2} is {add_num.call(int(num1),int(num2))}")
