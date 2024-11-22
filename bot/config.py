import psycopg2

def connect_to_db():
    connection = psycopg2.connect(
        dbname="postgres",
        user="postgre",
        password="BdBxeX?dsO^Z9",
        host="91.243.71.86",
        port="5432"
    )
    return connection


BOT_TOKEN = "7777000113:AAHZ-irduLYqc9sK8LwT5eULFrKgTfFpXOI"
