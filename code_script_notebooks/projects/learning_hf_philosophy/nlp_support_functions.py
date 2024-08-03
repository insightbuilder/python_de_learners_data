from typing import List
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import re


from datasets import ClassLabel, Sequence
import random
import pandas as pd
from IPython.display import display, HTML

import numpy as np
from tqdm import tqdm

from huggingface_hub import HfApi, ModelFilter

# Extracting Model based on given task
api = HfApi()

models = api.list_models(
    filter=ModelFilter(
        task="text-classification"
    )
)

models = list(models)
print(len(models))
print(models[0].modelId)


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


def get_maxlen(dataset, column: str):
    """Returns the max length of the given 
    column in the dataset"""
    all_len = [len(row[column]) for row in dataset]
    return max(all_len)

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


label_list = wnut["train"].features[f"ner_tags"].feature.names  # get features

def compute_metrics(p):
    """Metric computation for token_classification"""
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ] # for each datapoint, get prediction for each token
    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ] # for each datapoint, get label for each token

    results = seqeval.compute(predictions=true_predictions, references=true_labels)
    # return the result in form of precision, recall, f1 and accuracy
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

def show_one(example):
    print(f"Context: {example['sent1']}")
    print(f"  A - {example['sent2']} {example['ending0']}")
    print(f"  B - {example['sent2']} {example['ending1']}")
    print(f"  C - {example['sent2']} {example['ending2']}")
    print(f"  D - {example['sent2']} {example['ending3']}")
    print(f"\nGround truth: option {['A', 'B', 'C', 'D'][example['label']]}")


ending_names = ["ending0", "ending1", "ending2", "ending3"]
# Pre-Process function for the Multi-QnA task
def preprocess_function(examples: List, tokenizer, tokenized_examples):
    # Repeat each first sentence four times to go with the four possibilities of second sentences.
    first_sentences = [[context] * 4 for context in examples["sent1"]]
    # print(first_sentences)
    question_headers = examples["sent2"]
    # Grab all second sentences possible for each context, and enumerate them.
    second_sentences = [[f"{header} {examples[end][i]}" for end in ending_names] for i, header in enumerate(question_headers)]
    # print(second_sentences)
    # Flatten all sentences into a single list 
    first_sentences = sum(first_sentences, [])
 
    second_sentences = sum(second_sentences, [])
   
    # Tokenize
    tokenized_examples = tokenizer(first_sentences,
                                   second_sentences,
                                   truncation=True)
    # Un-flatten
    return {k: [v[i:i+4] for i in range(0, len(v), 4)] for k, v in tokenized_examples.items()}


def compute_metrics(eval_predictions):
    """accuracy metrics"""
    predictions, label_ids = eval_predictions
    preds = np.argmax(predictions, axis=1)
    return {"accuracy": (preds == label_ids).astype(np.float32).mean().item()}

def get_sentiment(row, column):
    text = row[column]
    tokened_text = tokenizer_from_name(text, truncation=True,
                                      padding=True, max_length=512,
                                      return_tensors='pt').to('cuda')
    model_out = trained_model(**tokened_text).logits
    prediction = model_out.argmax().item()
    return {'prediction': trained_model.config.id2label[prediction]}

# used for QnA training
def prepare_train_features(examples):
    # Some of the questions have lots of whitespace on the left, 
    # which is not useful and will make the
    # truncation of the context fail (the tokenized question will take a lots of space). So we remove that
    # left whitespace
    examples["question"] = [q.lstrip() for q in examples["question"]]

    # Tokenize our examples with truncation and padding, 
    # but keep the overflows using a stride. This results
    # in one example possible giving several features when 
    # a context is long, each of those features having a
    # context that overlaps a bit the context of the previous feature.
    tokenized_examples = tokeniser(
        examples["question" if pad_on_right else "context"],
        examples["context" if pad_on_right else "question"],
        truncation="only_second" if pad_on_right else "only_first",
        max_length=max_length,
        stride=doc_stride,
        return_overflowing_tokens=True,
        return_offsets_mapping=True,  # map the start and end positions of the answer to the original context by setting
        padding="max_length",
    )

    # Since one example might give us several features if it has a long context, 
    # we need a map from a feature to
    # its corresponding example. This key gives us just that.
    
    sample_mapping = tokenized_examples.pop("overflow_to_sample_mapping")
    # The offset mappings will give us a map from token to character 
    # position in the original context. This will
    # help us compute the start_positions and end_positions.
    offset_mapping = tokenized_examples.pop("offset_mapping")
    # offset_mapping is part of the tokenizer return dictionary
    # Let's label those examples!
    tokenized_examples["start_positions"] = []
    tokenized_examples["end_positions"] = []

    for i, offsets in enumerate(offset_mapping):
        # We will label impossible answers with the index of the CLS token.
        input_ids = tokenized_examples["input_ids"][i]
        cls_index = input_ids.index(tokeniser.cls_token_id)

        # Grab the sequence corresponding to that example 
        # (to know what is the context and what is the question).
        sequence_ids = tokenized_examples.sequence_ids(i)

        # One example can give several spans, this is the index of 
        # the example containing this span of text.
        sample_index = sample_mapping[i]
        answers = examples["answers"][sample_index]
        
        # If no answers are given, set the cls_index as answer.
        if len(answers["answer_start"]) == 0:
            tokenized_examples["start_positions"].append(cls_index)
            tokenized_examples["end_positions"].append(cls_index)
        else:
            # Start/end character index of the answer in the text.
            start_char = answers["answer_start"][0]
            end_char = start_char + len(answers["text"][0])

            # Start token index of the current span in the text.
            token_start_index = 0
            while sequence_ids[token_start_index] != (1 if pad_on_right else 0):
                token_start_index += 1

            # End token index of the current span in the text.
            token_end_index = len(input_ids) - 1
            while sequence_ids[token_end_index] != (1 if pad_on_right else 0):
                token_end_index -= 1

            # Detect if the answer is out of the span (in which case this feature is labeled with the CLS index).
            if not (offsets[token_start_index][0] <= start_char and \
                    offsets[token_end_index][1] >= end_char):
                tokenized_examples["start_positions"].append(cls_index)
                tokenized_examples["end_positions"].append(cls_index)
            else:
                # Otherwise move the token_start_index and token_end_index to the two ends of the answer.
                # Note: we could go after the last offset if the answer is the last word (edge case).
                while token_start_index < len(offsets) and \
                offsets[token_start_index][0] <= start_char:
                    token_start_index += 1
                tokenized_examples["start_positions"].append(token_start_index - 1)
                while offsets[token_end_index][1] >= end_char:
                    token_end_index -= 1
                tokenized_examples["end_positions"].append(token_end_index + 1)

    return tokenized_examples

# used in QnA training
def prepare_validation_features(examples):
    # Some of the questions have lots of whitespace on the left, which is not useful and will make the
    # truncation of the context fail (the tokenized question will take a lots of space). So we remove that
    # left whitespace
    examples["question"] = [q.lstrip() for q in examples["question"]]

    # Tokenize our examples with truncation and maybe padding, but keep the overflows using a stride. This results
    # in one example possible giving several features when a context is long, each of those features having a
    # context that overlaps a bit the context of the previous feature.
    tokenized_examples = tokeniser(
        examples["question" if pad_on_right else "context"],
        examples["context" if pad_on_right else "question"],
        truncation="only_second" if pad_on_right else "only_first",
        max_length=max_length,
        stride=doc_stride,
        return_overflowing_tokens=True,
        return_offsets_mapping=True,
        padding="max_length",
    )

    # Since one example might give us several features if it has a long context, we need a map from a feature to
    # its corresponding example. This key gives us just that.
    sample_mapping = tokenized_examples.pop("overflow_to_sample_mapping")

    # We keep the example_id that gave us this feature and we will store the offset mappings.
    tokenized_examples["example_id"] = []

    for i in range(len(tokenized_examples["input_ids"])):
        # Grab the sequence corresponding to that example (to know what is the context and what is the question).
        sequence_ids = tokenized_examples.sequence_ids(i)
        context_index = 1 if pad_on_right else 0

        # One example can give several spans, this is the index of the example containing this span of text.
        sample_index = sample_mapping[i]
        tokenized_examples["example_id"].append(examples["id"][sample_index])

        # Set to None the offset_mapping that are not part of the context so it's easy to determine if a token
        # position is part of the context or not.
        tokenized_examples["offset_mapping"][i] = [
            (o if sequence_ids[k] == context_index else None)
            for k, o in enumerate(tokenized_examples["offset_mapping"][i])
        ]

    return tokenized_examples

def postprocess_qa_predictions(examples, features, raw_predictions, n_best_size = 20, max_answer_length = 30):
    all_start_logits, all_end_logits = raw_predictions
    # Build a map example to its corresponding features.
    example_id_to_index = {k: i for i, k in enumerate(examples["id"])}
    features_per_example = collections.defaultdict(list)
    for i, feature in enumerate(features):
        features_per_example[example_id_to_index[feature["example_id"]]].append(i)

    # The dictionaries we have to fill.
    predictions = collections.OrderedDict()

    # Logging.
    print(f"Post-processing {len(examples)} example predictions split into {len(features)} features.")

    # Let's loop over all the examples!
    for example_index, example in enumerate(tqdm(examples)):
        # Those are the indices of the features associated to the current example.
        feature_indices = features_per_example[example_index]

        min_null_score = None # Only used if squad_v2 is True.
        valid_answers = []
        
        context = example["context"]
        # Looping through all the features associated to the current example.
        for feature_index in feature_indices:
            # We grab the predictions of the model for this feature.
            start_logits = all_start_logits[feature_index]
            end_logits = all_end_logits[feature_index]
            # This is what will allow us to map some the positions in our logits to span of texts in the original
            # context.
            offset_mapping = features[feature_index]["offset_mapping"]

            # Update minimum null prediction.
            cls_index = features[feature_index]["input_ids"].index(tokenizer.cls_token_id)
            feature_null_score = start_logits[cls_index] + end_logits[cls_index]
            if min_null_score is None or min_null_score < feature_null_score:
                min_null_score = feature_null_score

            # Go through all possibilities for the `n_best_size` greater start and end logits.
            start_indexes = np.argsort(start_logits)[-1 : -n_best_size - 1 : -1].tolist()
            end_indexes = np.argsort(end_logits)[-1 : -n_best_size - 1 : -1].tolist()
            for start_index in start_indexes:
                for end_index in end_indexes:
                    # Don't consider out-of-scope answers, either because the indices are out of bounds or correspond
                    # to part of the input_ids that are not in the context.
                    if (
                        start_index >= len(offset_mapping)
                        or end_index >= len(offset_mapping)
                        or offset_mapping[start_index] is None
                        or offset_mapping[end_index] is None
                    ):
                        continue
                    # Don't consider answers with a length that is either < 0 or > max_answer_length.
                    if end_index < start_index or end_index - start_index + 1 > max_answer_length:
                        continue

                    start_char = offset_mapping[start_index][0]
                    end_char = offset_mapping[end_index][1]
                    valid_answers.append(
                        {
                            "score": start_logits[start_index] + end_logits[end_index],
                            "text": context[start_char: end_char]
                        }
                    )
        
        if len(valid_answers) > 0:
            best_answer = sorted(valid_answers, key=lambda x: x["score"], reverse=True)[0]
        else:
            # In the very rare edge case we have not a single non-null prediction, we create a fake prediction to avoid
            # failure.
            best_answer = {"text": "", "score": 0.0}
        
        # Let's pick our final answer: the best one or the null answer (only for squad_v2)
        if not squad_v2:
            predictions[example["id"]] = best_answer["text"]
        else:
            answer = best_answer["text"] if best_answer["score"] > min_null_score else ""
            predictions[example["id"]] = answer

    return predictions
# Used for summmarisation task
def preprocess_function(examples, tokenizer,
                        prefix, max_input_length,
                        max_target_length):
    """Tokenises the inputs and results and returns a 
    single dictionary with input_ids and labels"""
    inputs = [prefix + doc for doc in examples['document']]
    model_inputs = tokenizer(inputs,
                             max_length=max_input_length,
                             truncation=True)
    labels = tokenizer(examples['summary'],
                       max_length=max_target_length,
                       truncation=True)
    # add labels to the model_inputs itself
    model_inputs['labels'] = labels['input_ids']
    return model_inputs


def compute_rouge(eval_pred, tokenizer, rouge):
    predictions, labels = eval_pred
    decoded_preds = tokenizer.batch_decode(predictions,
                                           skip_special_tokens=True)
    # Replace -100 with pad_token_id in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
 
    decoded_labels = tokenizer.batch_decode(labels,
                                            skip_special_tokens=True)
 
    # Rouge expects a newline after each sentence
    decoded_preds = ["\n".join(nltk.sent_tokenize(pred.strip())) \
                     for pred in decoded_preds]
    decoded_labels = ["\n".join(nltk.sent_tokenize(label.strip())) \
                      for label in decoded_labels]
 
    # Note that other metrics may not have a `use_aggregator` parameter
    # and thus will return a list, computing a metric for each sentence.
    result = rouge.compute(predictions=decoded_preds,
                           references=decoded_labels,
                           use_stemmer=True,
                           use_aggregator=True)
    # Extract a few results
    result = {key: value * 100 for key, value in result.items()}
    
    # Add mean generated length
    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) \
                       for pred in predictions]
    result["gen_len"] = np.mean(prediction_lens)
   
    return {k: round(v, 4) for k, v in result.items()}


# post process in translation task
def postprocess_text(preds, labels):
    preds = [pred.strip() for pred in preds]
    labels = [[label.strip()] for label in labels]

    return preds, labels


def compute_sacrebleu(eval_preds, tokenizer, metric):
    preds, labels = eval_preds
    if isinstance(preds, tuple):
        preds = preds[0]
    decoded_preds = tokenizer.batch_decode(preds, skip_special_tokens=True)

    # Replace -100 in the labels as we can't decode them.
    labels = np.where(labels != -100, labels, tokenizer.pad_token_id)
    decoded_labels = tokenizer.batch_decode(labels, skip_special_tokens=True)

    # Some simple post-processing
    decoded_preds, decoded_labels = postprocess_text(decoded_preds,
                                                     decoded_labels)

    result = metric.compute(predictions=decoded_preds,
                            references=decoded_labels)
    result = {"bleu": result["score"]}

    prediction_lens = [np.count_nonzero(pred != tokenizer.pad_token_id) for pred in preds]
    result["gen_len"] = np.mean(prediction_lens)
    result = {k: round(v, 4) for k, v in result.items()}
    return result


# define collate function - transform list of dictionaries [ {input_ids: [123, ..]}, {.. ] to single batch dictionary { input_ids: [..], labels: [..], attention_mask: [..] }
def collate(elements):
    tokenlist=[e["input_ids"] for e in elements]
    tokens_maxlen=max([len(t) for t in tokenlist])

    input_ids,labels,attention_masks = [],[],[]
    for tokens in tokenlist:
        pad_len=tokens_maxlen-len(tokens)

        # pad input_ids with pad_token, labels with ignore_index (-100) and set attention_mask 1 where content otherwise 0
        input_ids.append( tokens + [tokenizer.pad_token_id]*pad_len )   
        labels.append( tokens + [-100]*pad_len )    
        attention_masks.append( [1]*len(tokens) + [0]*pad_len ) 

    batch={
        "input_ids": torch.tensor(input_ids),
        "labels": torch.tensor(labels),
        "attention_mask": torch.tensor(attention_masks)
    }
    return batch