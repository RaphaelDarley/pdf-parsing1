import mysql.connector

paper_table = "test_paper"
image_table = "test_graph"


def init():
    cnx = mysql.connector.connect(
        host="localhost",
        user="energystats",
        password="energystats",
        #   port = 8888, #for Mamp users
        database='energystats'
    )
    return cnx


def insert_image_info(cnx, paper_url, paper_date, page_num, image_path, page_text, img_text):
    paper_id = get_paper_id_or_add(cnx, paper_url, paper_date)
    insert_info_with_paper_id(cnx, paper_id, page_num,
                              image_path, page_text, img_text)


def insert_info_with_paper_id(cnx, paper_id, page_num, image_path, page_text, img_text):
    cursor = cnx.cursor()
    insert_data = {"paper_id": paper_id,
                   "page_num": page_num,
                   "image_path": image_path,
                   "page_text": page_text,
                   "img_text": img_text,
                   }
    cursor.execute(
        f"INSERT INTO {image_table}(paper_id, page_num, image_path, page_text, img_text) VALUES"
        "(%(paper_id)s, %(page_num)s, %(image_path)s, %(page_text)s, %(img_text)s)", insert_data)
    cnx.commit()
    cursor.close()


def get_paper_id_or_add(cnx, paper_url, paper_date):
    cursor = cnx.cursor()
    cursor.execute(
        f"SELECT id from {paper_table} WHERE paper_url = '{paper_url}'")

    if (id := cursor.fetchone()) is None:
        insert_data = {
            # "paper_table": paper_table,
            "paper_url": paper_url,
            "date": paper_date
        }
        query = "INSERT INTO " + paper_table + \
            " (paper_url, date) VALUES (%(paper_url)s, %(date)s)"
        # cursor.execute(
        #     f"INSERT INTO {paper_table} (paper_url, date) VALUES ('{paper_url}', '{paper_date}')")
        cursor.execute(query, insert_data)
        id = cursor.lastrowid
    else:
        id = id[0]

    cnx.commit()
    cursor.close()
    return id
