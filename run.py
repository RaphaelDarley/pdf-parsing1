from timeit import default_timer as timer
import scrape
import parse_db

if __name__ == '__main__':
    start_time = timer()
    links = []
    base_url = "https://aspofrance.org/tag/jean-laherrere/page/"
    i = 0
    while True:
        i += 1
        urls = scrape.scrape_page_article_urls(f"{base_url}{i}")
        if urls == False:
            break
        else:
            links.extend(urls)
            break  # testing

    for link in links:
        pdfs = scrape.process_paper_page(link)
        print(f"pdfs: {pdfs}")
        (path, url) = pdfs[0]
        print(path)
        print(url)
        parse_db.process_doc(path, url)
        break

    print(f"time elapsed: {timer() - start_time}")
