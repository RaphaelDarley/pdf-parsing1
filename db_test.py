import mysql.connector
cnx = mysql.connector.connect(
    host="localhost",
    user="energystats",
    password="energystats",
    #   port = 8888, #for Mamp users
    database='energystats'
)
# print(cnx)
# print(cnx.get_server_info())


def main():
    cursor = cnx.cursor()

    # add_test = ("INSERT INTO test"
    #             "(content)"
    #             "VALUES (%(content)s)")
    add_test = ("INSERT INTO test "
                "(content) "
                "VALUES (\"item from python\")")

    # data_test = ('important item from python')
    data_test = {'conent': 'important item from python'}

    # cursor.execute(add_test, data_test)

    # cursor.execute(add_test, data_test)

    # cnx.commit()

    cursor.close()

    print_all_rows(cnx, "test")

    cnx.close()


def print_all_rows(cnx, table):
    cursor = cnx.cursor()
    query = ("SELECT * FROM %s")

    cursor.execute(query, (table, ))

    print(cursor.fetchall())

    # for row in cursor:
    #     print(row)
    cursor.close()


if __name__ == "__main__":
    main()
