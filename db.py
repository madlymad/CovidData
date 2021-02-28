import sqlite3


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_covid(conn):
    """
    """
    cur = conn.cursor()
    sql = """
    SELECT Body
    FROM MessageInfo
    WHERE ChatID = 2 AND Body like "%Ενημέρωση για τον κορωνοϊό%"
    """
    cur.execute(sql)

    rows = cur.fetchall()
    return rows