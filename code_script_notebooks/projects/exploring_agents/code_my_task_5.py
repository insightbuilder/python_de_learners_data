
def search_sentences(text, keyword):
    sentences = text.split(". ")
    result = [sentence for sentence in sentences if keyword.lower() in sentence.lower()]
    return result

# Example
text_content = "Python is a popular programming language. It is used for web development, data analysis, machine learning, etc."
keyword = "programming"
search_results = search_sentences(text_content, keyword)
for result in search_results:
    print(result)
