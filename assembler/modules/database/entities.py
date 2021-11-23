"""
Low level database manipulations:
Create Read Update Delete database entities
Classes for database tables
"""

import sqlite3
from modules.settings import settings

# Get path to the SQL database file
settings = settings.get_settings()


def get_page(page_id):

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM pages WHERE "
                   "id=:id ",

                   {'id': page_id})

    page_tuple = cursor.fetchone()
    connection.close()

    if page_tuple:
        return Converter.convert_to_page([page_tuple])[0]


def get_page_by_number(page_number):

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM pages WHERE "
                   "page_number=:page_number ",

                   {'page_number': page_number})

    page_tuple = cursor.fetchone()
    connection.close()

    if page_tuple:
        return Converter.convert_to_page([page_tuple])[0]


def add_page(page):

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO pages VALUES ("
                   ":id,"
                   ":page_number,"
                   ":published_id,"
                   ":sent_id,"
                   ":description)",

                   {'id': cursor.lastrowid,
                    'page_number': page.page_number,
                    'published_id': page.published_id,
                    'sent_id': page.sent_id,
                    'description': page.description})

    connection.commit()
    page.id = cursor.lastrowid  # Add database ID to the asset object
    connection.close()

    return page


def update_page(page):

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("UPDATE pages SET "
                   "page_number=:page_number, "
                   "published_id=:published_id, "
                   "sent_id=:sent_id, "
                   "description=:description "

                   "WHERE id=:id",

                   {'id': page.id,
                    'page_number': page.page_number,
                    'published_id': page.published_id,
                    'sent_id': page.sent_id,
                    'description': page.description})

    connection.commit()
    connection.close()


def get_published_snapshot(snapshot_id):

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM published "
                   "WHERE id=:id ",

                   {'id': snapshot_id})

    snapshot_tuple = cursor.fetchone()
    connection.close()

    if snapshot_tuple:
        return Converter.convert_to_snapshot([snapshot_tuple])[0]


def get_sent_snapshot(snapshot_id):

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM sent "
                   "WHERE id=:id ",

                   {'id': snapshot_id})

    snapshot_tuple = cursor.fetchone()
    connection.close()

    if snapshot_tuple:
        return Converter.convert_to_snapshot([snapshot_tuple])[0]


def get_published_snapshot_by_version(page_id, version):
    """

    """

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM published "
                   "WHERE page_id=:page_id "
                   "AND version=:version",

                   {'page_id': page_id,
                    'version': version})

    snapshot_tuple = cursor.fetchone()
    connection.close()

    if snapshot_tuple:
        return Converter.convert_to_snapshot([snapshot_tuple])[0]


def get_sent_snapshot_by_version(page_id, version):
    """

    """

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM sent "
                   "WHERE page_id=:page_id "
                   "AND version=:version",

                   {'page_id': page_id,
                    'version': version})

    snapshot_tuple = cursor.fetchone()
    connection.close()

    if snapshot_tuple:
        return Converter.convert_to_snapshot([snapshot_tuple])[0]


def add_published_snapshot(snapshot):
    """
    """

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO published VALUES ("
                   ":id,"
                   ":page_id,"
                   ":version,"
                   ":description)",

                   {'id': cursor.lastrowid,
                    'page_id': snapshot.page_id,
                    'version': snapshot.version,
                    'description': snapshot.description})

    connection.commit()
    snapshot.id = cursor.lastrowid
    connection.close()

    return snapshot


def add_sent_snapshot(snapshot):
    """
    """

    connection = sqlite3.connect(settings.sql_file_path)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO sent VALUES ("
                   ":id,"
                   ":page_id,"
                   ":version,"
                   ":description)",

                   {'id': cursor.lastrowid,
                    'page_id': snapshot.page_id,
                    'version': snapshot.version,
                    'description': snapshot.description})

    connection.commit()
    snapshot.id = cursor.lastrowid
    connection.close()

    return snapshot


class Page:
    def __init__(self, page_number):

        self.id = None
        self.page_number = page_number
        self.published_id = None
        self.sent_id = None
        self.description = ''

    def get_published_version(self):

        snapshot = get_published_snapshot(self.published_id)
        if snapshot:
            return snapshot.version

    def get_sent_version(self):

        snapshot = get_sent_snapshot(self.sent_id)
        if snapshot:
            return snapshot.version


class VersionSnapshot:
    """
    Published or sent version of the page file
    """

    def __init__(self, page_id, version):
        self.id = None
        self.page_id = page_id
        self.version = version
        self.description = ''


class Converter:
    """
    Convert data from DB to objects
    """

    @staticmethod
    def convert_to_page(page_tuples):
        """
        Convert list of page tuples to list of Page() objects
        (id, page_number, published_id, sent_id, description)
        """

        pages = []

        for page_tuple in page_tuples:
            page = Page(page_tuple[1])
            page.id = page_tuple[0]
            page.published_id = page_tuple[2]
            page.sent_id = page_tuple[3]
            page.description = page_tuple[4]
            pages.append(page)

        return pages

    @staticmethod
    def convert_to_snapshot(snapshot_tuples):
        """
        (id, page_id, version, description)
        :param snapshot_tuples:
        :return:
        """

        snapshots = []
        for snapshot_tuple in snapshot_tuples:
            snapshot = VersionSnapshot(snapshot_tuple[1], snapshot_tuple[2])
            snapshot.id = snapshot_tuple[0]
            snapshot.description = snapshot_tuple[3]
            snapshots.append(snapshot)

        return snapshots


