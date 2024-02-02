import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re


from datasets import ClassLabel, Sequence
import random
import pandas as pd
from IPython.display import display, HTML

# oneline logic with mulitple else if
task = 'cola'
num_labels = 3 if task.startswith("mnli") else 1 \
            if task == "stsb" else 2


def create_corpus(raw_text: str):
    """Tokenizes, removes stopwords, stems and cleans spl characters"""
    token_text = nltk.word_tokenize(raw_text)
    # download the stop words for english using nltk.download first
    stp_word = set(stopwords.words('english'))  # get the set of stop_words
    # remove the stop words
    filter_text = [word for word in token_text if word not in stp_word]
    stemmer = PorterStemmer()
    # stem the words
    stem_text = [stemmer.stem(word) for word in filter_text]
    # remove spl chars
    nospl_text = [re.sub(r'[^a-zA-Z\s]', '', word) for word in stem_text]
    # remove spaces
    fin_text = [word for word in nospl_text if word != '']
    # send the final list of words
    return list(set(fin_text))


example = """Autograd is a reverse automatic differentiation system.
Conceptually, autograd records a graph recording all of the operations
that created the data as you execute operations, giving you a directed
acyclic graph whose leaves are the input tensors and roots are the
output tensors. By tracing this graph from roots to leaves,
you can automatically compute the gradients using the chain rule."""

print(len(create_corpus(example)))
# the returned list contains the words in random order, and order 
# changes every run, so checking only len of the list

assert len(create_corpus(example)) == 28


def group_texts(examples, block_size):
    """Function takes the datasets that have input_ids & attention_masks
    as keys. Returns the lists as concatenated & chunked list
    under the input_ids and attention_masks """
    concatenated_examples = {k: sum(examples[k], []) for k in examples.keys()}
    # above will make sub_list inside input_ids and attention_masks to be extended
    total_length = len(concatenated_examples[list(examples.keys())[0]])
    # provide the total_length of input_ids
    # we drop the remainder of the sentence, like truncating
    tot_length = (total_length // block_size) * block_size
    # split by chunks of max_len
    result = {
        k: [t[i : i + block_size] for i in range(0, tot_length, block_size)]
            for k, t in concatenated_examples.items()
    }
    # k will be keys while t will be values
    result["labels"] = result["input_ids"].copy() # inputs are duplicated as labels
    # transformers library will apply the "shifting to right"
    return result


def show_random_elements(dataset, num_examples=5):
    assert num_examples <= len(dataset)
    picks = []
    for _ in range(num_examples):
        pick = random.randint(0, len(dataset) - 1)
        picks.append(pick)
    print(picks)
    df = pd.DataFrame(dataset[picks])
    for column, typ in dataset.features.items():
        if isinstance(typ, ClassLabel):
            df[column] = df[column].transform(lambda i: typ.names(i))
        elif isinstance(typ, Sequence) and isinstance(typ.feature, ClassLabel):
            df[column] = df[column].transform(lambda x: [typ.feature.names[i] for i in x])
    
    display(HTML(df.to_html()))



def tokenize_and_align_labels(examples, tokenizer,
                              task='ner', label_all_tokens=True):
    """Function that aligns the tokens with their task related ids 
    in NER, POS and Chunking"""
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True,
                                 is_split_into_words=True)
    # tokenize the tokens
    labels = []
    # enumerate on the "ner"_tags in the example
    for i, label in enumerate(examples[f"{task}_tags"]):
        # get the word_ids from the tokenized tokens!!!
        word_ids = tokenized_inputs.word_ids(batch_index=i)
        previous_word_idx = None
        label_ids = []
        for word_idx in word_ids:
            # Special tokens have a word id that is None. We set the label to -100 so they are automatically
            # ignored in the loss function.
            if word_idx is None: 
                label_ids.append(-100)
            # We set the label for the first token of each word.
            elif word_idx != previous_word_idx:
                label_ids.append(label[word_idx])
            # For the other tokens in a word, we set the label to either the current label or -100, depending on
            # the label_all_tokens flag.
            else:
                label_ids.append(label[word_idx] if label_all_tokens else -100)
            previous_word_idx = word_idx

        labels.append(label_ids)

    tokenized_inputs["labels"] = labels
    return tokenized_inputs


def show_one(example):
    print(f"Context: {example['sent1']}")
    print(f"  A - {example['sent2']} {example['ending0']}")
    print(f"  B - {example['sent2']} {example['ending1']}")
    print(f"  C - {example['sent2']} {example['ending2']}")
    print(f"  D - {example['sent2']} {example['ending3']}")
    print(f"\nGround truth: option {['A', 'B', 'C', 'D'][example['label']]}")

# Need to add Question_answering, multi-choice, translation, summarisation and related metrics here