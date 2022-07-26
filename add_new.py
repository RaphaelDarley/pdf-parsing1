from timeit import default_timer as timer
import parse_db


if __name__ == "__main__":
    start_time = timer()
    file_name = "JHL Barnett paper - draft 18 July 2022.pdf"
    path = f"data/papers/{file_name}"
    parse_db.process_doc(path, path)
    print(f"finished in {timer()-start_time}")
