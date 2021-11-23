"""
Create database table for Book Assembler
"""

import sqlite3


def build_database(sql_file_path):

    connection = sqlite3.connect(sql_file_path)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE pages (
                        id integer primary key autoincrement,
                        page_number text,
                        published_id integer,
                        sent_id integer,
                        description text,
                        FOREIGN KEY(published_id) REFERENCES published(id)
                        FOREIGN KEY(sent_id) REFERENCES sent(id)
                        )''')

    cursor.execute('''CREATE TABLE published (
                        id integer primary key autoincrement,
                        page_id integer,
                        version text,
                        description text
                        )''')

    cursor.execute('''CREATE TABLE sent (
                        id integer primary key autoincrement,
                        page_id integer,
                        version text,
                        description text
                        )''')

    connection.commit()
    connection.close()
