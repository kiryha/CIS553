from PySide import QtCore, QtGui
import os
import glob
import sqlite3

from ui import ui_assembler_main

assembler_root = os.path.dirname(os.path.abspath(__file__))
root_pages = 'E:/projects/workbook/pages/jpg'
sql_file_path = '{}/data/data.db'.format(assembler_root)


# DB
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


def get_page(page_id):

    connection = sqlite3.connect(sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM pages WHERE "
                   "id=:id ",

                   {'id': page_id})

    page_tuple = cursor.fetchone()
    connection.close()

    if page_tuple:
        return Converter.convert_to_page([page_tuple])[0]


def get_page_by_number(page_number):

    connection = sqlite3.connect(sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM pages WHERE "
                   "page_number=:page_number ",

                   {'page_number': page_number})

    page_tuple = cursor.fetchone()
    connection.close()

    if page_tuple:
        return Converter.convert_to_page([page_tuple])[0]


def add_page(page):

    connection = sqlite3.connect(sql_file_path)
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

    connection = sqlite3.connect(sql_file_path)
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

    connection = sqlite3.connect(sql_file_path)
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM published "
                   "WHERE id=:id ",

                   {'id': snapshot_id})

    snapshot_tuple = cursor.fetchone()
    connection.close()

    if snapshot_tuple:
        return Converter.convert_to_snapshot([snapshot_tuple])[0]


def get_published_snapshot_by_version(page_id, version):
    """

    """

    connection = sqlite3.connect(sql_file_path)
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


def add_published_snapshot(snapshot):
    """
    """

    connection = sqlite3.connect(sql_file_path)
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


class Page:
    def __init__(self, page_number):

        self.id = None
        self.page_number = page_number
        self.sent_id = None
        self.published_id = None
        self.description = ''


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


# STRINGS and FILES
def parse_page_path(file_path):
    file_path = file_path.replace('\\', '/')
    file_name = file_path.split('/')[-1]
    page_name = file_name.split('.')[0]
    page_number, page_version = page_name.split('_')

    return page_number, page_version


def get_jpg_path(page_number, version):
    """
    Get page file path by page number and version
    :param page_number:
    :param version:
    :return: string path to page file, None if JPG does not exists
    """

    jpg_path = '{0}/{1}_{2}.jpg'.format(root_pages, page_number, version)

    if not os.path.exists(jpg_path):
        return

    return jpg_path


def collect_page_numbers(page_files):
    """
    Get list of page numbers without versions
    """

    page_numbers = []

    for page_file in page_files:
        page_number, page_version = parse_page_path(page_file)
        if page_number not in page_numbers:
            page_numbers.append(page_number)

    return sorted(page_numbers)


class Book:
    def __init__(self):
        self.list_pages = []

    def get_pages(self):
        """
        Get list of pages from JPG folder
        If page is not in database - create entity in page table
        """

        page_files = glob.glob('{0}/*.jpg'.format(root_pages))
        page_numbers = collect_page_numbers(page_files)

        for page_number in page_numbers:

            page = get_page_by_number(page_number)

            # Create page record in the database
            if not page:
                page = Page(page_number)
                page = add_page(page)

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


class AlignDelegate(QtGui.QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        QtGui.QItemDelegate.paint(self, painter, option, index)


class BookModel(QtCore.QAbstractTableModel):
    def __init__(self, book, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.book = book
        self.header = ['  Page  ', '  Pub ', '  Sent ', '  Description  ']  # , '  Notes  '

    # Build-in functions
    def flags(self, index):

        column = index.column()
        if column == 3:
            return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header[col]

    def rowCount(self, parent):

        if not self.book.list_pages:
            return 0

        return len(self.book.list_pages)

    def columnCount(self, parent):

        return 4

    def data(self, index, role):

        if not index.isValid():
            return

        row = index.row()
        column = index.column()
        page = self.book.list_pages[row]

        if role == QtCore.Qt.ForegroundRole:
            if column == 2:
                if page.published_id != page.sent_id:
                    return QtGui.QBrush(QtGui.QColor('#c90404'))

        if role == QtCore.Qt.UserRole + 1:
            return page

        if role == QtCore.Qt.DisplayRole: 
            if column == 0:
                return page.page_number

            if column == 1:
                snapshot = get_published_snapshot(page.published_id)
                if snapshot:
                    return snapshot.version

            if column == 2:
                return page.sent_id

            if column == 3:
                return page.description

        if role == QtCore.Qt.EditRole:
            if column == 3:
                return page.description

    def setData(self, index, cell_data, role=QtCore.Qt.EditRole):
        """
        When "Description" table cell is edited
        """

        row = index.row()
        column = index.column()
        page = self.book.list_pages[row]

        if role == QtCore.Qt.EditRole:

            if column == 3:
                page.description = cell_data
                update_page(page)
                self.book.update_page(page)

            return True


class Assembler(QtGui.QMainWindow, ui_assembler_main.Ui_Assembler):
    def __init__(self, parent=None):
        super(Assembler, self).__init__(parent=parent)

        # SETUP UI
        self.setupUi(self)

        # Setup pages table
        self.tabPages.verticalHeader().hide()
        self.tabPages.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tabPages.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.tabPages.horizontalHeader().setStretchLastSection(True)
        self.tabPages.setItemDelegate(AlignDelegate())

        # Data
        self.book = None
        self.book_model = None
        self.current_version = None  # UI [ +/- ] counter for selected page

        # # # Google Drive
        # auth = GoogleAuth()
        # auth.LocalWebserverAuth()
        # self.google_drive = GoogleDrive(auth)
        # self.jpeg_folder = '1ZTL3GjCTP0GeD-BBG-DhFNgOOGvTC4se'

        # Populate data
        self.init_ui()

        # Setup UI
        self.tabPages.clicked.connect(self.show_page)

        self.btnUpVersion.clicked.connect(lambda: self.show_page(1))
        self.btnDownVersion.clicked.connect(lambda: self.show_page(-1))
        self.btnPublish.clicked.connect(self.publish_page)
        self.btnReload.clicked.connect(self.init_ui)
        # self.btnSendLatest.clicked.connect(self.send_latest)
        # self.btnGeneratePDF.clicked.connect(self.generate_pdf)

    # UI
    def init_ui(self):

        self.book = Book()
        self.book.get_pages()

        self.book_model = BookModel(self.book)
        self.tabPages.setModel(self.book_model)

    # Functionality
    def show_page(self, shift=None):
        """
        Display image in UI
        Show higher or lover versions with [ + ] or [ - ] buttons
        """

        # Get selected page
        indexes = self.tabPages.selectionModel().selectedIndexes()
        page = indexes[0].data(QtCore.Qt.UserRole + 1)

        # If [ + ] or [ - ] buttons pressed, get next or previous version
        if type(shift) == int:

            if self.current_version:
                version = self.current_version
            else:
                snapshot = get_published_snapshot(page.published_id)

                if not snapshot:
                    version = '01'
                else:
                    version = snapshot.version

            int_version = int(version) + shift
            version = '{0:02d}'.format(int_version)
            self.current_version = version

        # If page cell clicked in UI, get published version
        else:
            snapshot = get_published_snapshot(page.published_id)

            if not snapshot:
                version = '01'
            else:
                version = snapshot.version

            self.current_version = None

        # Show JPG
        jpg_path = get_jpg_path(page.page_number, version)

        if not jpg_path:
            self.labPage.setPixmap(None)
            self.statusbar.showMessage('Page {0} version {1} does not exists!'.format(page.page_number, version))
            return

        pixmap = QtGui.QPixmap(jpg_path)
        height = self.grp_images.height() - 40  # Get height of groupBox parent widget and scale JPG to fit it
        self.labPage.resize(height/1.295, height)
        self.labPage.setPixmap(pixmap.scaled(self.labPage.size(), QtCore.Qt.IgnoreAspectRatio))

        # Report page number and version shown
        self.statusbar.showMessage('Loaded page {0} version {1}'.format(page.page_number, version))

    def publish_page(self):
        """
        Publish current version for selected page
        """

        # Get selected page
        indexes = self.tabPages.selectionModel().selectedIndexes()

        if not indexes:
            self.statusbar.showMessage('ERROR! Select page to publish!')
            return

        page = indexes[0].data(QtCore.Qt.UserRole + 1)

        # Get current version
        version = self.current_version
        if not version:
            version = '01'

        # Get path to JPG
        jpg_path = get_jpg_path(page.page_number, version)
        if not jpg_path:
            self.statusbar.showMessage('ERROR! {} version of {} page does not exists!'.format(version, page.page_number))
            return

        # Check if snapshot of current version exists, create if not
        snapshot = get_published_snapshot_by_version(page.id, version)
        if not snapshot:
            snapshot = add_published_snapshot(VersionSnapshot(page.id, version))

        # Record published version to page
        page.published_id = snapshot.id
        update_page(page)

        # Update pages list with a new page data
        self.book_model.layoutAboutToBeChanged.emit()
        self.book.update_page(get_page(page.id))
        self.book_model.layoutChanged.emit()

        # Report
        self.statusbar.showMessage('Published {} version of page {}'.format(version, page.page_number))





    def copy_file_locally(self, page):
        """
        Copy versioned files to "to_layout" folder without version
        """

        file_src = '{0}/{1}_{2}.jpg'.format(root_pages, page.page_number, page.published_id)
        file_out = '{0}/to_layout/{1}.jpg'.format(root_pages, page.page_number)

        copyfile(file_src, file_out)

        self.book_model.layoutAboutToBeChanged.emit()
        self.book.update_sent_version(page)
        self.book_model.layoutChanged.emit()

        return file_out

    def copy_file_drive(self, existing_pages, page, file_out):
        """
        Upload file to Google Drive
        """

        # Delete existing file
        for existing_page in existing_pages:
            if existing_page['title'] == '{0}.jpg'.format(page.page_number):
                existing_page.Delete()

        # Upload new file
        google_file = self.google_drive.CreateFile({'parents': [{'id': self.jpeg_folder}],
                                                    'title': '{0}.jpg'.format(page.page_number)})
        google_file.SetContentFile(file_out)
        google_file.Upload()

        print '>> Page {0} uploaded.'.format(page.page_number)

    def get_selected_page_numbers(self):
        """
        Create a string list of selected pages
        """

        selected_pages = []

        indexes = self.tabPages.selectionModel().selectedIndexes()
        for index in indexes:
            page_number = index.data(QtCore.Qt.DisplayRole)
            selected_pages.append(page_number)

        return selected_pages

    def send_latest(self):
        """
        Copy files to layout folder and upload to Google Drive
        JPG = https://drive.google.com/drive/u/2/folders/1ZTL3GjCTP0GeD-BBG-DhFNgOOGvTC4se
        """

        print '>> Sending files to Google Drive...'

        selected_pages = self.get_selected_page_numbers()
        existing_pages = self.google_drive.ListFile({'q': "'{0}' in parents and trashed=false".format(self.jpeg_folder)
                                                     }).GetList()

        for page in self.book.list_pages:

            # Skip unselected pages
            if self.chbSelected.isChecked():
                if not page.page_number in selected_pages:
                    continue

            # Skip versions without update
            if page.published_id == page.sent_id:
                continue

            file_out = self.copy_file_locally(page)
            self.copy_file_drive(existing_pages, page, file_out)

        print '>> Files uploaded!'

    def add_page_number(self, pdf_file, num, page):

        pos_x = 20
        if num % 2 != 0:
            pos_x = 2450

        pdf_file.setFont('Helvetica', 60)
        pdf_file.drawString(pos_x, 20, page.page_number)

    def generate_pdf(self):

        path_pdf = '{0}/workbook_auto_{1}.pdf'.format(root_pdf, self.linPDFVersion.text())
        size_x = 2598
        size_y = 3366
        pdf_file = canvas.Canvas(path_pdf, pagesize=(size_x, size_y))
        pdf_file.setTitle('Quriotica')

        print '>> Building PDF file...'

        for num, page in enumerate(self.book.list_pages):

            if not num == 0:  # Make next page
                pdf_file.showPage()

            version = page.published_id
            jpg_path = '{0}/{1}_{2}.jpg'.format(root_pages, page.page_number, version)
            pdf_file.drawImage(jpg_path, 0, 0, size_x, size_y)
            self.add_page_number(pdf_file, num, page)

        pdf_file.save()

        print 'PDF file saved at {}'.format(path_pdf)


if __name__ == "__main__":

    # Init database
    if not os.path.exists(sql_file_path):
        build_database(sql_file_path)

    app = QtGui.QApplication([])
    ketamine = Assembler()
    ketamine.show()
    app.exec_()
