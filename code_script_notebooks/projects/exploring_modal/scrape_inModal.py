import re
#import sys
import modal
import urllib.request

stub = modal.Stub(name='Modal-Scraper')

@stub.function()
def get_links(url):
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf8")
    links = []
    for match in re.finditer('href="(.*?)"', html):
        links.append(match.group(1))
    return links

@stub.local_entrypoint()
def main(url):
    links = get_links.call(url)
    print(links)
"""
if __name__ == "__main__":
    links = get_links(sys.argv[1])
    print(links)"""
