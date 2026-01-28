import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import re
import json
from multiprocessing import Pool


def clean_text(text):
    # Remove citation markers like [1]
    text = re.sub(r"\[ \d+ \]", "", text)
    text = re.sub(r"\[\d+\]", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Remove space before punctuation
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)

    return text


def extract_text_and_urls(content_div):
    texts = []
    urls = []

    for element in content_div.children:
        if element.name == "h2":
            print(element.name)
            break

        if element.name == "p":
            paragraph_text = clean_text(element.get_text())
            if paragraph_text:
                texts.append(paragraph_text)

            for a in element.find_all("a", href=True):
                href = a["href"]
                if href.startswith("/wiki/"):
                    urls.append({
                        "text": clean_text(a.get_text(strip=True)),
                        "url": urljoin("https://en.wikipedia.org", href)
                    })

    return texts, urls


def get_div_content(url):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    print(response.status_code)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find("div", class_="mw-content-ltr mw-parser-output")


def get_data_from_url(url):
    content_div = get_div_content(url)
    paragraths, links = extract_text_and_urls(content_div)
    return {
        "main_url": url,
        "text": paragraths,
        "urls": links
    }


if __name__ == "__main__":
    url = 'https://en.wikipedia.org/wiki/Teutonic_Order'
    #headers = {
        "User-Agent": "TeutonicResearchBot/1.0 (contact: example@mail.com)"
    }


    content_div = get_div_content(url)
    paragraths, links = extract_text_and_urls(content_div)

    data = {"pages": []}
    data["pages"].append({
        "main_url": url,
        "text": paragraths,
        "urls": links
    })


    urls = [link["url"] for link in links]

    with Pool(processes=5) as p:
        results = p.map(get_data_from_url, urls)

    data["pages"].extend(results)
    '''
    for link in links:
        page_data = get_data_from_url(link["url"])
        data["pages"].append(page_data)
    '''

    with open("teutonic_order.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)