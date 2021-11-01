from PySide import QtCore, QtGui

from ui import ui_assembler_main


class Assembler(QtGui.QMainWindow, ui_assembler_main.Ui_Assembler):
    def __init__(self, parent=None):
        super(Assembler, self).__init__(parent=parent)

        # SETUP UI
        self.setupUi(self)

        # # Setup pages table
        # self.tabPages.verticalHeader().hide()
        # self.tabPages.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        # self.tabPages.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        # self.tabPages.horizontalHeader().setStretchLastSection(True)
        # self.tabPages.setItemDelegate(AlignDelegate())

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
        #
        # # Populate data
        # self.init_ui()
        #
        # # Setup UI
        # self.tabPages.clicked.connect(self.show_page)
        #
        # self.btnUpVersion.clicked.connect(lambda: self.show_page(1))
        # self.btnDownVersion.clicked.connect(lambda: self.show_page(-1))
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
            self.labPage.resize(1543, 2000)  # (self.labPage.width(), self.labPage.width()*1.295)  # 733, 950
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
