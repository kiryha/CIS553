"""
Low level database manipulations:
Create Read Update Delete database entities
Classes for database tables
"""

import sqlite3
from modules.settings import settings

# Get path to the SQL database file
settings = settings.get_settings()


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


class Page:
    def __init__(self, page_number):

        self.id = None
        self.page_number = page_number
        self.published_id = None
        self.sent_id = None
        self.description = ''

    def update_page(self):

        connection = sqlite3.connect(settings.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("UPDATE pages SET "
                       "page_number=:page_number, "
                       "published_id=:published_id, "
                       "sent_id=:sent_id, "
                       "description=:description "

                       "WHERE id=:id",

                       {'id': self.id,
                        'page_number': self.page_number,
                        'published_id': self.published_id,
                        'sent_id': self.sent_id,
                        'description': self.description})

        connection.commit()

        connection.close()

    def get_published_version(self):

        connection = sqlite3.connect(settings.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM published "
                       "WHERE id=:id ",

                       {'id': self.published_id})

        snapshot_tuple = cursor.fetchone()
        connection.close()

        if snapshot_tuple:
            snapshot = Converter.convert_to_snapshot([snapshot_tuple])[0]
            return snapshot.version

    def get_sent_version(self):

        connection = sqlite3.connect(settings.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM sent "
                       "WHERE id=:id ",

                       {'id': self.sent_id})

        snapshot_tuple = cursor.fetchone()
        connection.close()

        if snapshot_tuple:
            snapshot = Converter.convert_to_snapshot([snapshot_tuple])[0]
            return snapshot.version

    def get_published_snapshot_by_version(self, version):

        connection = sqlite3.connect(settings.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM published "
                       "WHERE page_id=:page_id "
                       "AND version=:version",

                       {'page_id': self.id,
                        'version': version})

        snapshot_tuple = cursor.fetchone()
        connection.close()

        if snapshot_tuple:
            return Converter.convert_to_snapshot([snapshot_tuple])[0]

    def add_published_snapshot(self, version):

        snapshot = VersionSnapshot(self.id, version)

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

    def add_sent_snapshot(self, version):

        snapshot = VersionSnapshot(self.id, version)

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

    def get_sent_snapshot_by_version(self, version):

        connection = sqlite3.connect(settings.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM sent "
                       "WHERE page_id=:page_id "
                       "AND version=:version",

                       {'page_id': self.id,
                        'version': version})

        snapshot_tuple = cursor.fetchone()
        connection.close()

        if snapshot_tuple:
            return Converter.convert_to_snapshot([snapshot_tuple])[0]


class VersionSnapshot:
    """
    Published or sent version of the page file
    """

    def __init__(self, page_id, version):
        self.id = None
        self.page_id = page_id
        self.version = version
        self.description = ''


class Book:
    def __init__(self, page_files):
        self.page_files = page_files
        self.list_pages = []

    def parse_page_path(self, file_path):

        file_path = file_path.replace('\\', '/')
        file_name = file_path.split('/')[-1]
        page_name = file_name.split('.')[0]
        page_number, page_version = page_name.split('_')

        return page_number, page_version

    def collect_page_numbers(self, page_files):
        """
        Get list of page numbers without versions
        """

        page_numbers = []

        for page_file in page_files:
            page_number, page_version = self.parse_page_path(page_file)
            if page_number not in page_numbers:
                page_numbers.append(page_number)

        return sorted(page_numbers)

    def get_page(self, page_id):

        connection = sqlite3.connect(settings.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM pages WHERE "
                       "id=:id ",

                       {'id': page_id})

        page_tuple = cursor.fetchone()
        connection.close()

        if page_tuple:
            return Converter.convert_to_page([page_tuple])[0]

    def get_page_by_number(self, page_number):

        connection = sqlite3.connect(settings.sql_file_path)
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM pages WHERE "
                       "page_number=:page_number ",

                       {'page_number': page_number})

        page_tuple = cursor.fetchone()
        connection.close()

        if page_tuple:
            return Converter.convert_to_page([page_tuple])[0]

    def add_page(self, page):

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

    def get_pages(self):
        """
        Get list of pages from JPG folder
        If page is not in database - create entity in page table
        """

        page_numbers = self.collect_page_numbers(self.page_files)

        for page_number in page_numbers:

            page = self.get_page_by_number(page_number)

            # Create page record in the database
            if not page:
                page = Page(page_number)
                page = self.add_page(page)

            self.list_pages.append(page)

    def update_page(self, page):
        """
        Update existing page in page list
        """

        for _page in self.list_pages:
            if _page.id == page.id:
                self.list_pages.remove(_page)
                self.list_pages.append(page)

        self.list_pages.sort(key=lambda page: page.page_number)


