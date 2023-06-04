import os
import re
from dataclasses import dataclass
from typing import List

import modal

stub = modal.Stub(name="example-news-summarizer")
MODEL_NAME = "google/pegasus-xsum"
CACHE_DIR = "/cache"

stub["deep_learning_image"] = modal.Image.debian_slim().pip_install(
    "transformers==4.16.2", "torch", "sentencepiece"
)

stub["scraping_image"] = modal.Image.debian_slim().pip_install(
    "requests", "beautifulsoup4", "lxml"
)

volume = modal.SharedVolume().persist("pegasus-modal-vol")

if stub.is_inside(stub["deep_learning_image"]):
    from transformers import PegasusForConditionalGeneration, PegasusTokenizer

    TOKENIZER = PegasusTokenizer.from_pretrained(
        MODEL_NAME, cache_dir=CACHE_DIR
    )
    MODEL = PegasusForConditionalGeneration.from_pretrained(
        MODEL_NAME, cache_dir=CACHE_DIR
    )


if stub.is_inside(stub["scraping_image"]):
    import requests
    from bs4 import BeautifulSoup

@dataclass
class NYArticle:
    title: str
    image_url: str = ""
    url: str = ""
    summary: str = ""
    text: str = ""

@stub.function(
    secret=modal.Secret.from_name("nytimes"), image=stub["scraping_image"]
)
def latest_science_stories(n_stories: int = 5) -> List[NYArticle]:
    # query api for latest science articles
    params = {
        "api-key": os.environ["NYTIMES_API_KEY"],
    }
    nyt_api_url = "https://api.nytimes.com/svc/topstories/v2/science.json"
    response = requests.get(nyt_api_url, params=params)

    # extract data from articles and return list of NYArticle objects
    results = response.json()
    reject_urls = {"null", "", None}
    articles = [
        NYArticle(
            title=u["title"],
            image_url=u.get("multimedia")[0]["url"]
            if u.get("multimedia")
            else "",
            url=u.get("url"),
        )
        for u in results["results"]
        if u.get("url") not in reject_urls
    ]

    # select only a handful of articles; this usually returns 25 articles
    articles = articles[:n_stories]
    print(f"Retrieved {len(articles)} from the NYT Top Stories API")
    return articles

@stub.function(image=stub["scraping_image"])
def scrape_nyc_article(url: str) -> str:
    print(f"Scraping article => {url}")

    # fetch article; simulate desktop browser
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    # get all text paragraphs & construct single string with article text
    article_text = ""
    article_section = soup.find_all(
        "div", {"class": re.compile(r"\bStoryBodyCompanionColumn\b")}
    )
    if article_section:
        paragraph_tags = article_section[0].find_all("p")
        article_text = " ".join([p.get_text() for p in paragraph_tags])

    # return article with scraped text
    return article_text

@stub.function(
    image=stub["deep_learning_image"],
    gpu=False,
    shared_volumes={CACHE_DIR: volume},
    memory=4096,
)
def summarize_article(text: str) -> str:
    print(f"Summarizing text with {len(text)} characters.")

    # summarize text
    batch = TOKENIZER(
        [text], truncation=True, padding="longest", return_tensors="pt"
    ).to("cpu")
    translated = MODEL.generate(**batch)
    summary = TOKENIZER.batch_decode(translated, skip_special_tokens=True)[0]

    return summary

@stub.function(schedule=modal.Period(days=1))
def trigger():
    #Get the articles links
    articles = latest_science_stories.call()

    # parallelize article scraping
    for i, text in enumerate(scrape_nyc_article.map([a.url for a in articles])):
        articles[i].text = text

    # parallelize summarization
    for i, summary in enumerate(
        summarize_article.map([a.text for a in articles if len(a.text) > 0])
    ):
        articles[i].summary = summary

    # show all summaries in the terminal
    for article in articles:
        print(f'Summary of "{article.title}" => {article.summary}')

@stub.local_entrypoint()
def main():
    trigger.call()
