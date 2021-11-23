"""
Book class
All data required to manage book
"""

import entities


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

    def get_pages(self):
        """
        Get list of pages from JPG folder
        If page is not in database - create entity in page table
        """

        page_numbers = self.collect_page_numbers(self.page_files)

        for page_number in page_numbers:

            page = entities.get_page_by_number(page_number)

            # Create page record in the database
            if not page:
                page = entities.Page(page_number)
                page = entities.add_page(page)

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