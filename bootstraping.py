import MySQLdb
import csv
from config import *


def insert_stations_in_db(tsv_path: str):
    conn = MySQLdb.connect(passwd=DB_PASSWORD, user=DB_USER, host=DB_HOST, db=DB_NAME)
    cursor = conn.cursor()
    with open(tsv_path, newline='') as tsvf:
        reader = csv.reader(tsvf, delimiter='\t', quotechar='|')
        next(reader)  # discard title
        for name, code in reader:
            cursor.execute("INSERT INTO stations (name, code) VALUES(%s, %s)", (name, code))
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    insert_stations_in_db("./stazioni.tsv")