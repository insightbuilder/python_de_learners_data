import numpy as np
from collections import defaultdict
from collections import Counter

def count_letter(word):
    # declare a counter dict
    counter = {}
    # enumerate the letters in word
    for letter in word:
        # check if letter already in dict
        if letter not in counter:
            # no, then create a key with value of 0
            counter[letter] = 0
        # letter available, then increment it
        counter[letter] += 1
    # after enumeration, then return counter 
    return counter


def default_dict_counter(word):
    # declare default dict
    counter = defaultdict(int)
    # enumerate 
    for letter in word:
        counter[letter] += 1 
    return counter


word = 'Thinunelveli Rani'
counter = Counter(word)
# print(counter)

# print(counter.most_common())  # [('i', 3), ('n', 3), ('e', 2)]
# print(counter.most_common(1))  # [('i', 3)]


a = Counter(
    apple=6,
    orange=7,
    paste=7
)

print(a.keys())
print(a.most_common())

a.update(monitor=2)

print(a.keys())

# what if I send some different data
a.update('localdata')  # it accepts...

print(a.keys())

def print_ascii_bar_chart(data, symbol="#"):
    # get the most commmon letters
    counter = Counter(data).most_common()
    # create a dictionary with letter as category and freq multiplied with symbol
    chart = {category: symbol * frequency for category, frequency in counter}
    
    max_len = max(len(category) for category in chart)
    for category, frequency in chart.items():
        padding = (max_len - len(category)) * " "
        print(f"{category}{padding} |{frequency}")


# Utils
def r2_score(y_true, y_pred):
    corr_matrix = np.corrcoef(y_true, y_pred)
    corr = corr_matrix[0, 1]  # 2 by 2 matrix
    return corr ** 2 


def mean_squared_error(y_true, y_pred):
    # error is square and average is taken
    return np.mean((y_true - y_pred) ** 2)


def accuracy(y_true, y_pred):
    # get the number of data points that are classified correctly
    accuracy = np.sum(y_true == y_pred) / len(y_true)
    return accuracy


def sigmoid(self, x):
    # returns between 0 to 1
    return 1 / (np.exp(-x) + 1)

def predict(self, X):
    linear_model = np.dot(X, self.weights) + self.bias
    y_predicted = self._sigmoid(linear_model)
    y_predicted_cls = [1 if i > 0.5 else 0 for i in y_predicted]
    return np.array(y_predicted_cls)


def sigmoid_t(x, *args, **kwargs):
    if args:
        print(args)
    if kwargs:
        print(kwargs)
    # returns between 0 to 1
    return 1 / (np.exp(-x) + 1)


sigmoid_t(5, 57, t='hen')
