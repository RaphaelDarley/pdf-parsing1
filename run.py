from timeit import default_timer as timer
import scrape
import parse_db
import faulthandler
faulthandler.enable()


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
            # break  # testing

    count = 0
    # print(links)
    for link in links:
        if (pdfs := scrape.process_paper_page(link)) is None:
            continue
        # print(f"pdfs: {pdfs}")
        for pdf in pdfs:
            count += 1
            if count < 65:  # seg fault on pdf 65
                continue
            (path, url) = pdf
            parse_db.process_doc(path, url)
            print(f"finished pdf no: {count} in {timer()-start_time}({path})")

    print(f"time elapsed: {timer() - start_time}")
