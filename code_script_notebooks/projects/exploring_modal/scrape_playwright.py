import re
#import sys
import modal
import urllib.request

stub = modal.Stub(name='Modal-Scraper')

playwright_image = modal.Image.debian_slim(python_version="3.10").run_commands(
    "apt-get install -y software-properties-common",
    "apt-add-repository non-free",
    "apt-add-repository contrib",
    "apt-get update",
    "pip install playwright==1.30.0",
    "playwright install-deps chromium",
    "playwright install chromium",
)

@stub.function(image=playwright_image)
async def get_links(url):
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        links = await page.eval_on_selector_all("a[href]", "elements => elements.map(element => element.href)")
        await browser.close()

    print("Links", links)
    return links
   
@stub.local_entrypoint()
def main():
    """Function takes url list and works on it"""
    urls = ["http://modal.com", "http://github.com"]
    for link in get_links.map(urls):
        for l in link:
            print(l)

"""
if __name__ == "__main__":
    links = get_links(sys.argv[1])
    print(links)"""
