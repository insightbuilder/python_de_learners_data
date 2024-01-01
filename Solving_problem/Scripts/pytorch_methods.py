import torch
import torch.nn as nn
import numpy as np
import time
from torch.utils.data import Dataset, DataLoader
device = 'cuda' if torch.cuda.is_available() else 'cpu'
# print(device)
# zeros, ones, rand, empty, randint, linspace, eye, 
# multinomial(has math involved, understand), cat, arange, unsqueeze(learn), masked_fill 
# stack, triu, tril, transpose, softmax, 
# Embedding, Linear functions, data loading
# view, broadcasting semantics, transforms

y6 = torch.tensor([1])
# print(y6.shape)  # Size([1])

a = torch.zeros(1, 2)  # 1 row and 2 cols 
# print(a)

# ones
b = torch.ones(2, 2)  # 2 row and 2 cols
# print(b)

# rand
c = torch.rand(10, 10)  # 10 rows and 10 cols
# print(c)

# empty
d = torch.empty(5, 3)  # 5 rows and 3 cols
# print(d)

# randint
e = torch.randint(low=10, high=100,
                  size=(3, 2))  # 3 row and 2 cols random number between 10 and 100
# print(e)

# linspace
f = torch.linspace(start=0, end=13, steps=4, dtype=torch.int32)  # linear space between 0 to 7 with steps of 3
# can control the type of the output without worrying about type error
# print(f)
# can change the dimensions of linspace data with view
# eye or identity matrix
g = torch.eye(n=5, m=5)
# print(g)

# following are methods that check the efficiency or provides some easy way of manipulating the data

h = torch.rand(size=[100, 100, 100, 100])
# print(h.shape)

i = torch.rand(size=[100, 100, 100, 100])

# do torch multiplication
tm = (h @ i)
# print(h[0][0][0][0], 'h')
# print(i[0][0][0][0], 'i')
# print(tm[0][0][0][0], 'hm')
# do numpy multiplication
nm = np.multiply(h, i)
# print(nm[0][0][0][0], 'nm')

# embeddings, torch.stack, torch.multinomial, torch.tril, torch.triu
# input.T / input.transpose, nn.Linear, torch.cat, F.softmax
# unsqueeze and squeeze ( so squeeze(-1) would remove the last dimension and unsqueeze(-1) 
ys = torch.rand(3)  # torch.Size([3])
# tensor([0.3803, 0.9533, 0.1612])
# Size([3]) is single tensor with 3 elements, no rows or cols
# print(ys.unsqueeze(dim=0))  # Size(1, 3) is single row with 3 cols 
# tensor([[0.3803, 0.9533, 0.1612]])
# print(ys.unsqueeze(dim=1))  # Size(3, 1) is 3 rows with single col
"""
tensor([[0.0418],
        [0.9801],
        [0.9711]])
"""
# would add a new dimension after the current last.)
# (show all the examples of functions/methods with pytorch docs)
j = torch.tensor([0.2, 0.3, 0.5])
samples = torch.multinomial(input=j, num_samples=10, replacement=True)
# draws samples with 0, 1, 2 
# print(samples)

m2 = torch.tensor([[5, 0, 1,],
                  [8, 10, 9],
                  [0.1, 0.7, 0.9]], dtype=torch.float32)

p2 = torch.multinomial(m2, 5, True)  # 3 rows and 5 cols
# print(p2)
k = torch.tensor([1, 2, 3, 4, 5])
l = torch.tensor([5])  # torch.Size([1])
# print(l.shape)
m = torch.tensor(5)  # this will have no size torch.Size([])
# print(m.shape)

o = torch.cat((k, l),dim=0)
# print(o)
# n = torch.cat((k, m), dim=0)  # will throw zero-dimensional tensor cannot be concatenated
# print(n)

p = torch.randint(low=5, high=10, size=(2, 3))
q = torch.randint(low=10, high=25, size=(2, 4))
# print(p)
# print(q)

r = torch.cat((p, q), dim=1)  # tensor 1 is in 2nd position, dim = 0 / 1 will work on two axes only
# print(r)

# stack expects each tensor to be equal size, but got [5] at entry 0 and [4] at entry 3
s1 = torch.arange(0, 5)  # 1 r and 5 c
s2 = torch.arange(1, 6)  # 1 r and 5 c
s3 = torch.arange(2, 7)
s4 = torch.arange(4, 9)
s5 = torch.stack((s1, s2, s3, s4))
# print(s5.shape)
# print(s5)

s1 = torch.rand(1, 3)
s2 = torch.rand(1, 3)
s3 = torch.rand(1, 3)

s4 = torch.stack((s1, s2, s3), dim=0)  # 3 row * 1 row and 3 cols

# print(s4.shape)  # 3 * 1 row and 3 cols tensor

s5 = torch.stack((s1, s3, s2), dim=1)  # 1 row * 3 row and 3 cols

"stack batches the data, while cat concatenates the data"

# print(s5.shape)
# diagonal in triu and tril tell where the diagonal "is" inside the matrix
tl = torch.tril(torch.ones(3, 3) * 5)  # scalar int multiplication works
# print(tl)
tu = torch.triu(torch.ones(3, 3) * torch.tensor([5]))  # What happens when 
# another tensor is involved? Same result
# print(tu)

tu_try = torch.triu(torch.ones(3, 3) * torch.tensor(5))  # What happens when 
# another tensor with None size is involved? 
# print(tu_try)
# There has to be a base tensor, on which a mask is placed, and where the conditions 
# return True, update the value
maskout = torch.zeros(5, 5).masked_fill(torch.tril(torch.ones(5, 5)) == 0,
                                        float('-inf'))
# print(maskout, 'maskout')
# print(torch.exp(maskout), 'exponentiating maskout')

# print(torch.exp(torch.tensor([0])), 'mask out')
# print(torch.exp(torch.tensor([float('-inf')])), 'mask out')

# masked = torch.masked_fill(torch.zeros(5, 5), make_triu == 0, torch.tensor(67))
#  * (Tensor input, Tensor mask, Tensor value)
# print(masked)

input = torch.zeros(2, 3, 4)
# print(input.shape, 'input')

out1 = input.transpose(0, 1)
# help(torch.transpose)
out2 = input.transpose(-2, -1)
# The resulting :attr:`out`
# tensor shares its underlying storage with the :attr:`input` tensor, so
# changing the content of one would change the content of the other.
# LOOK AT THE SHAPE...

# print(out1.shape, 'out1')
# print(out2.shape, 'out2')

# How the linear works?

import torch.nn.functional as F

ten1 = torch.tensor([1., 2., 3.])
# print(type(ten1))
# the tensor is int64 type by default, need to make it float by adding a '.' point
lin1 = nn.Linear(3, 1, bias=False)
lin2 = nn.Linear(1, 1, bias=False)
# print(lin1(ten1))
# print(lin2(ten1))  # will error out as the dims don't match
# mat1 and mat2 shapes cannot be multiplied (1x3 and 1x1)

# How softmax works?
s_out = F.softmax(ten1)
# print(s_out)

# How embedding works 
vocab_size = 80
embedding_dim = 6

r_in = nn.Embedding(num_embeddings=vocab_size,
                     embedding_dim=embedding_dim)
# Facing IndexError index out of range error.
# print(emb.weight)
input = torch.LongTensor([12, 8, 5, 0])
# The values used to embed must be less than num_embeddings

# creates a dictionary??
data_ind = torch.tensor([1, 5, 6, 8])
e_out = r_in(data_ind)
# print(e_out)
# print(e_out.shape)
"""
tensor([[-0.5251, -2.2980, -1.2629, -0.2184, -0.3236, -1.1250],
        [-2.0372, -0.7762,  1.1529, -1.7969,  0.3080, -0.4566],
        [ 0.3185,  1.7108, -0.4360,  1.5348, -1.1450,  0.2744],
        [-0.0502, -1.8797,  1.3616, -0.0599, -0.4435,  0.0271]],
       grad_fn=<EmbeddingBackward0>)
"""
# Matrix Multiplication
a = torch.tensor([[1, 2], [3, 4], [5, 6]])
b = torch.tensor([[7, 2, 9], [6, 3, 4]])

# print(a @ b)
# print(a.matmul(b))
# print(torch.matmul(a, b))

# playing with shapes

input = torch.rand((3, 8, 10))
B, T, C = input.shape
output = input.view(B * T, C)

# g = d.view(3, -1, -1)  # only one dimension can be inferred, runtime error  

# print(output.shape)
# print(output[:2, :-1])

b = torch.tensor([[1, 72, 68, 74, 67, 57, 72,  0],
                  [74, 73, 58, 71,  0, 56, 54, 75]], dtype=torch.float32)

d = torch.tensor([[1, 72, 68, 74, 67, 57, 72,  0, 73],
                  [74, 73, 58, 71,  0, 56, 54, 75, 58]], dtype=torch.float32)

# print(b.shape)
# print(d.shape)

# print(b.view(2 * 8))
# print(d.view(2 * 9))

# ce = F.cross_entropy(b.view(2*8), d.view(2*9))
## print(ce)

# some additional home work on cat and stack
part1 = torch.rand(size=(2, 2))  # 2 row / 2 col matrix
part2 = torch.rand(size=(2, 1))  # 2 row 1 col matrix
part3 = torch.rand(size=(1, 2))  # 1 row 2 col matrix

cat2 = torch.cat((part1, part3))  # will go through 
# print(cat2)
# cat1 = torch.cat((part1, part2))  # will inform the expected dimensions are not present

part4 = torch.rand((4, 3))
part5 = torch.randint(high=100, low=10, size=(4, 3))

partstack = torch.stack([part4, part5])

# print(partstack.shape)  # 2 tensors of 4 rows and 3 cols 

# partstackx0 = torch.stack(part4, part5)  # will throw syntax-error 

# print(partstackx0.shape)  # 2 tensors of 4 rows and 3 cols

catparts_dim0 = torch.cat((part4, part5), dim=0)
catparts_dim1 = torch.cat((part4, part5), dim=1)

# print(catparts_dim0.shape)  # 8 rows and 3 cols
# key is to expect the how the dimension will change
# print(catparts_dim1.shape)  # 4 rows and 6 cols

part9 = torch.linspace(start=10, end=20, steps=30)  # steps is required args, and ensure it is more than 1, else it will form a Size[1] tensor

# print(part9.shape)

# print(part9.view(size=(10,3)))
# print(part9.view(size=(5,6)))
# print(part9.view(size=(3,10)))
# print(part9.view(size=(4,10)))  # RuntimeError: shape '[4, 10]' is invalid for input of size 30

# print(part9.view(size=(-1, 3)))
# print(part9.view(size=(-1, 4)))  # will be invalid

class WineDataset(Dataset):
    # just use the init to load the data into the torch objects
    def __init__(self, x_data, y_data):
        self.x = torch.from_numpy(x_data)
        self.y = torch.from_numpy(y_data)
        self.n_samples = x_data.shape[0]

    def __getitem__(self, index):
        return self.x[index], self.y[index]

    def __len__(self):
        return self.n_samples

# wine_ds = WineDataset(x_data=x_data, y_data=y_data)
# winedataloader = DataLoader(wine_ds, shuffle=True, batch_size=3)

# batch1 = next(iter(winedataloader))
# print(batch1)  # List of tensor objects

# need to include the transforms 

# pytorch semantics
# Each tensor has at least one dimension.

# When iterating over the dimension sizes, starting at the trailing dimension, the dimension sizes must either be equal, one of them is 1, or one of them does not exist.

x = torch.empty(5, 7, 8)
y = torch.empty(5, 7, 8)  # tensor of same shapes are broadcastable

x = torch.empty((0, ))
x = torch.empty(2, 2)
# cannot broadcast as one of the dimension is not 1

a = torch.rand((3, 3, 1))
b = torch.rand((3, 1))

# 1st trailing dimension: both have size 1
# 2nd trailing dimension: a size == b size
# 3rd trailing dimension: b dimension doesn't exist 

# When it comes to Matrix Multiplication, there are following pairs one has to identify
# vector * vector, matrix * vector, batched mat * vector(bc) 
# batched matrix * batched matrix, batched matrix * broadcasted matrix
# A vector is of shape 1 row n col

# vector X vector is acceptable, and return dot product
tensor2 = torch.rand(3)  # Size([3]) 

tensor1 = torch.tensor([5, 6, 8], dtype=torch.float32)  # Size([3])

matrix = torch.tensor([[1, 2, 4],
                      [5, 6, 8],
                      [9, 6, 5]])  # Size([3, 3])

# print(tensor1)
# print(tensor2)

tm1 = torch.matmul(tensor1, tensor2)
# print(tm1)  # scalar

# matrix X vector is acceptable and returns a tensor broadcast
tensor3 = torch.rand(3, 4)  # 3 * 4 cols
tensor4 = torch.rand(4)  # 4 cols

tm2 = torch.matmul(tensor3, tensor4)
# print(tm2)  # 1 row 3 col

# batched matrix with broadcasted vector
tensor5 = torch.rand(3, 3, 4)
tensor_b = torch.tensor([[[1, 2, 4, 5], [5, 6, 8, 9], [5, 6, 4, 2]],
                         [[1, 9, 0, 8], [7, 2, 4, 5], [9, 8, 6, 2]],
                         [[7, 6, 2, 3], [7, 6, 3, 5], [6, 7, 3, 4]]
                         ])
tensor6 = torch.rand(4)

tm3 = torch.matmul(tensor5, tensor6)
# print(tm3)

# batched matrix with batched matrix
tensor7 = torch.rand(3, 4, 3)
tensor8 = torch.tensor([[[1, 2, 4, 5], [5, 6, 8, 9], [5, 6, 4, 2]],
                         [[1, 9, 0, 8], [7, 2, 4, 5], [9, 8, 6, 2]],
                         [[7, 6, 2, 3], [7, 6, 3, 5], [6, 7, 3, 4]]
                         ], dtype=torch.float32)
tm6 = torch.matmul(tensor7, tensor8)

# print(tm6)

# batched matrix with broadcasted matrix
tensor9 = torch.rand(10, 3, 4)
tensorh = torch.rand(4, 5)

mt6 = torch.matmul(tensor9, tensorh)
# print(mt6)

# Network layers learning
# flatten the tensor, given a nD tensor make them tensor that contains 
# multiple 1D tensors with the number of cols increased proportionaly
flatten = nn.Flatten(start_dim=1, end_dim=-1)
# create a 3 by 4 tensor
test_data = torch.tensor([[3, 5, 7, 9,],
                          [7, 6, 12, 3],
                          [3, 43, 21, 78]], dtype=torch.float32)
# print(test_data.shape)
# print(flatten(test_data).shape)  # Size([3, 4])

test_data2 = torch.rand(5, 28, 28)
print(flatten(test_data2).shape)  # Size([5, 784])

l1 = nn.Linear(4, 2)
hid1 = l1(test_data)
# print(hid1.shape)  # Size([5, 20])

r1 = nn.ReLU()
hid2 = nn.ReLU()(hid1)
# print(hid2)
# move the data through each layer inside sequentially
sequential = nn.Sequential(
    flatten,
    l1,
    r1,
    nn.Linear(2, 1)
)
# learn from 4 features, and provide 1 output features

fin = sequential(test_data)

# print(fin)
# print(fin.shape)  # Size([3, 1])

seq2 = nn.Sequential(
    flatten,
    nn.Linear(28 * 28, 512),
    r1,
    nn.Linear(512, 512),
    r1,
    nn.Linear(512, 10)
)

fin2 = seq2(test_data2)

print(fin2.shape)

softmax = nn.Softmax(dim=1) # softmax the columns

pred_prob = softmax(fin2)

# print(pred_prob)

# Getting at the model parameter

for name, params in seq2.named_parameters():
    print(f'Layer: {name} | size: {params.size()} | vals : {params[:2]}')

# Basic model (need to practice)
x = torch.ones(5)
y = torch.zeros(3)

w = torch.randn(5, 3, requires_grad=True)
b = torch.randn(3, requires_grad=True)

z = torch.matmul(x, w) + b

loss = F.binary_cross_entropy_with_logits(z, y)
print(loss)

print(f"The z grad fn: {z.grad_fn}")
print(f"The loss grad fn: {loss.grad_fn}")

with torch.no_grad():
    a = torch.matmul(x, w) + b
print(z.requires_grad)  # returns False

f = torch.matmul(x, w) + b
f_det = f.detach()
print(f_det.requires_grad)  # returns false

# going hyper with the below functions and parameters

learning_rate = 1e-3
batch_size = 64
epochs = 5

# supporting functions
loss_fn = nn.CrossEntropyLoss()   # softmax is implemented in the class already
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)


def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)

    model.train()

    for batch, (X, y) in enumerate(dataloader):
        # forward
        pred = model(X)
        loss = loss_fn(pred, y)
        # backward
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        if batch % 100 == 0:
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f} [{current:>5d} / {size:>5d}]")


def test_loop(dataloader, model, loss_fn):
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    with torch.no_grad():
        for x, y in dataloader:
            pred = model(x)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size

    print(f"Test Error: \n Accuracy: {(100 * correct):>1f} avg_loss: {test_loss:>8f}")
