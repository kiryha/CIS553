from PySide import QtCore, QtGui
import os
import glob

from ui import ui_assembler_main


root_pages = 'E:/projects/workbook_A/PAGES/JPG'

def parse_page_path(file_path):
    file_path = file_path.replace('\\', '/')
    file_name = file_path.split('/')[-1]
    page_name = file_name.split('.')[0]
    page_number, page_version = page_name.split('_')

    return page_number, page_version


def read_book_data():

    with open(book_database, 'r') as file_content:
        book_data = json.load(file_content)

    return book_data


def write_book_data(book_data):

    with open(book_database, 'w') as file_content:
        json.dump(book_data, file_content, indent=4)


class Page:
    def __init__(self, page_number):

        self.page_number = page_number
        self.last_version = '01'
        self.sent_version = '01'
        self.page_name = ''

        # self.init_page()

    def init_page(self):

        # Get last version
        page_files = glob.glob('{0}/{1}_*.jpg'.format(root_pages, self.page_number))

        page_versions = []
        for file_path in page_files:
            page_number, page_version = parse_page_path(file_path)
            page_versions.append(int(page_version))

        self.last_version = '{0:02d}'.format(max(page_versions))

        # Get sent version
        book_data = read_book_data()
        if self.page_number in book_data.keys():
            self.sent_version = book_data[self.page_number]['sent_version']
            self.page_name = book_data[self.page_number]['page_name']

            # if not 'page_name' in book_data[self.page_number].keys():
            #     book_data[self.page_number]['page_name'] = ''
            #     with open(book_database, 'w') as file_content:
            #         json.dump(book_data, file_content, indent=4)


class Book:
    def __init__(self):
        self.list_pages = []

    def page_exists(self, page_number):

        # Check if page_number exists in list_pages
        for page in self.list_pages:
            if page.page_number == page_number:
                return True

    def get_pages(self):

        page_files = glob.glob('{0}/*.jpg'.format(root_pages))
        # book_data = read_book_data()
        page_data = {'sent_version': '', 'page_name': ''}

        for file_path in page_files:

            # Update Book object
            page_number, page_version = parse_page_path(file_path)
            if not self.page_exists(page_number):
                page = Page(page_number)
                self.list_pages.append(page)

            # # Update JSON
            # if not page_number in book_data.keys():
            #     book_data[page_number] = page_data
            #     write_book_data(book_data)

    def update_sent_version(self, page):

        for current_page in self.list_pages:
            if current_page.page_number == page.page_number:
                current_page.sent_version = page.last_version

                # Update JSON
                book_data = read_book_data()
                book_data[page.page_number]['sent_version'] = page.last_version
                write_book_data(book_data)

    def update_name(self, page, page_name):

        for current_page in self.list_pages:
            if current_page.page_number == page.page_number:
                current_page.page_name = page_name

                # Update JSON
                book_data = read_book_data()
                book_data[page.page_number]['page_name'] = page_name
                write_book_data(book_data)


class AlignDelegate(QtGui.QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = QtCore.Qt.AlignCenter
        QtGui.QItemDelegate.paint(self, painter, option, index)


class PagesModel(QtCore.QAbstractTableModel):
    def __init__(self, book, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.book = book
        self.header = ['  Page  ', '  Last ', '  Sent ', '  Name  ']  # , '  Notes  '

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
                if page.last_version != page.sent_version:
                    return QtGui.QBrush(QtGui.QColor('#c90404'))

        if role == QtCore.Qt.UserRole + 1:
            return page

        if role == QtCore.Qt.DisplayRole:  # Fill table data to DISPLAY
            if column == 0:
                return page.page_number

            if column == 1:
                return page.last_version

            if column == 2:
                return page.sent_version

            if column == 3:
                return page.page_name

        if role == QtCore.Qt.EditRole:
            if column == 3:
                return page.page_name

    def setData(self, index, cell_data, role=QtCore.Qt.EditRole):
        """
        When table cell is edited
        """

        row = index.row()
        column = index.column()
        page = self.book.list_pages[row]

        if role == QtCore.Qt.EditRole:

            if column == 3:
                self.book.update_name(page, cell_data)

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
        self.page_files = 'E:/projects/workbook_A/PAGES/JPG'
        self.book_data = None
        self.book_model = None
        self.page_version = None

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
        # self.btnReload.clicked.connect(self.init_ui)
        # self.btnSendLatest.clicked.connect(self.send_latest)
        # self.btnGeneratePDF.clicked.connect(self.generate_pdf)

    # UI
    def init_ui(self):

        self.book_data = Book()
        self.book_data.get_pages()

        self.book_model = PagesModel(self.book_data)
        self.tabPages.setModel(self.book_model)

    # Functionality
    def show_page(self, shift=None):
        """
        Display image in UI
        Show higher or lover versions with [ + ] or [ - ] buttons
        """

        indexes = self.tabPages.selectionModel().selectedIndexes()
        page = indexes[0].data(QtCore.Qt.UserRole + 1)

        if type(shift) == int:  # [ + ] or [ - ] buttons

            if self.page_version:
                version = self.page_version
            else:
                version = page.last_version

            # Handle edge cases. Need to implement smarter way
            int_version = int(version) + shift
            if int_version <= 0 or int_version >= 99:
                return

            version = '{0:02d}'.format(int_version)
            self.page_version = version

        else:
            version = page.last_version
            self.page_version = None

        jpg_path = '{0}/{1}_{2}.jpg'.format(root_pages, page.page_number, version)

        if os.path.exists(jpg_path):
            pixmap = QtGui.QPixmap(jpg_path)
            height = self.grp_images.height() - 30
            self.labPage.resize(height/1.295, height)
            self.labPage.setPixmap(pixmap.scaled(self.labPage.size(), QtCore.Qt.IgnoreAspectRatio))
            print '>> Loaded {} version.'.format(version)

        else:
            # If version does not exists recursively find existing version
            self.show_page(shift)

    def copy_file_locally(self, page):
        """
        Copy versioned files to "to_layout" folder without version
        """

        file_src = '{0}/{1}_{2}.jpg'.format(root_pages, page.page_number, page.last_version)
        file_out = '{0}/to_layout/{1}.jpg'.format(root_pages, page.page_number)

        copyfile(file_src, file_out)

        self.book_model.layoutAboutToBeChanged.emit()
        self.book_data.update_sent_version(page)
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

        for page in self.book_data.list_pages:

            # Skip unselected pages
            if self.chbSelected.isChecked():
                if not page.page_number in selected_pages:
                    continue

            # Skip versions without update
            if page.last_version == page.sent_version:
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

        for num, page in enumerate(self.book_data.list_pages):

            if not num == 0:  # Make next page
                pdf_file.showPage()

            version = page.last_version
            jpg_path = '{0}/{1}_{2}.jpg'.format(root_pages, page.page_number, version)
            pdf_file.drawImage(jpg_path, 0, 0, size_x, size_y)
            self.add_page_number(pdf_file, num, page)

        pdf_file.save()

        print 'PDF file saved at {}'.format(path_pdf)


if __name__ == "__main__":
    app = QtGui.QApplication([])
    ketamine = Assembler()
    ketamine.show()
    app.exec_()
