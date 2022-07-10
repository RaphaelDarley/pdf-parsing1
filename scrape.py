import requests
from bs4 import BeautifulSoup
import urllib


# get pdf urls


def scrape_page_article_urls(url):
    page = requests.get(url)
    if not page.status_code == 200:
        return False
    # print(page.text)
    soup = BeautifulSoup(page.content, "html.parser")
    content = soup.find_all('article')
    links = []
    for article in content:
        # print(article.a.get('href'))
        links.append(article.a.get('href'))
    return links


# download pdfs
def process_paper_page(url):
    try:
        pdf_urls = get_pdf_urls(url)
    except Exception as e:
        print(f"Error {e} for: {url}")
        return
    for pdf_url in pdf_urls:
        split_url = url.split("/")
        paper_name = split_url[-1] if not split_url[-1] == '' else split_url[-2]
        file_name = pdf_url.split("/")[-1].split(".")[0]
        download_pdf(pdf_url, f"scraped/{paper_name}({file_name}).pdf")


# def get_pdf_url(url):
#     page = requests.get(url)
#     soup = BeautifulSoup(page.content, "html.parser")
#     return soup.find('a', class_='wp-block-file__button').get('href')

def get_href(anchor):
    return anchor.get('href')


def check_pdf(url):
    if not url:
        return False
    return url.endswith(".pdf")


def get_pdf_urls(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    links = map(get_href, soup.find_all('a'))
    pdf_links = set(filter(check_pdf, links))
    # print(pdf_links)
    if len(pdf_links) == 0:
        raise Exception(f"could not find pdf on page")
    return pdf_links


def download_pdf(url, path):
    r = requests.get(url, allow_redirects=True)
    open(path, "wb").write(r.content)


if __name__ == '__main__':
    links = []
    base_url = "https://aspofrance.org/tag/jean-laherrere/page/"
    i = 0
    while True:
        i += 1
        urls = scrape_page_article_urls(f"{base_url}{i}")
        if urls == False:
            break
        else:
            links.extend(urls)

    # print(links)
    for link in links:
        process_paper_page(link)
    # download_pdf(
    #     "https://aspofrance.files.wordpress.com/2022/05/temp30mai2022.pdf", "scraped/test.pdf")
