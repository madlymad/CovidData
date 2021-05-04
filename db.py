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

    except Error as e:  # pylint: disable=undefined-variable
        print(e)

    return conn


def convid_conversation(conn):
    cur = conn.cursor()
    sql = """
        SELECT ChatID
        FROM ChatInfo
        WHERE name = "Ελληνική Κυβέρνηση" AND PGTabLine like "%COVID-19%"
    """
    cur.execute(sql)

    rows = cur.fetchall()
    return rows[0][0]


def select_covid(conn, chatId):
    """
    """
    cur = conn.cursor()
    sql = f"""
        SELECT Body
        FROM MessageInfo
        WHERE ChatID = {chatId} AND Body like "%covid19-live-analytics%" AND Timestamp > 0
    """
    cur.execute(sql)

    rows = cur.fetchall()
    return rows
