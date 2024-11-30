import duckdb


def connect_to_db():
    print("connect to db...")
    db_file = "db/akinator.db"
    connection = duckdb.connect(db_file)
    return connection


def close_connection(connection):
    print("close connection...")
    connection.close()


def sql_db(connection, sql: str):
    result = connection.sql(sql)
    return result


def show_table(connection, table_name: str):
    connection.table(table_name).show()
