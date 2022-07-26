from timeit import default_timer as timer
import scrape
import parse_db
import faulthandler
faulthandler.enable()


if __name__ == '__main__':
    start_time = timer()

    link = "https://aspofrance.org/2019/06/17/world-ngl-production/"

    pdfs = scrape.process_paper_page(link)

    for pdf in pdfs:
        (path, url) = pdf
        parse_db.process_doc(path, url)
        # print(f"finished in {timer()-start_time}({path})")

    print(f"time elapsed: {timer() - start_time}")
