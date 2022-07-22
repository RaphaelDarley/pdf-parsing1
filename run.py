from timeit import default_timer as timer
import scrape
import parse

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
        print(pdfs)
        parse.process_doc(path=pdfs[0][0])
        break

    print(f"time elapsed: {timer() - start_time}")
