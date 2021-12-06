"""
Module to read settings from JSON file
Extension: to edit settings and save them back to a file
"""

import os
import json

assembler_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')


class Settings:
    def __init__(self, settings_data):

        self.project_root = None
        self.versioned_pages = None
        self.final_pages = None
        self.pdf_files = None
        self.sql_file_path = None
        self.jpeg_folder = None

        self.set_attributes(settings_data)

    def set_attributes(self, settings_data):
        """
        Set class attributes from JSON file

        :param settings_data:
        :return:
        """

        self.project_root = settings_data['project_root']['string']
        self.jpeg_folder = settings_data['jpeg_folder']['string']
        project_root = self.project_root  # Required for eval() to

        for attribute in settings_data:

            if attribute == 'project_root' or attribute == 'jpeg_folder':
                continue

            evaluated_token = eval(settings_data[attribute]['token'])
            attribute_value = settings_data[attribute]['string'].format(evaluated_token)
            setattr(self, attribute, attribute_value)


def get_settings():
    """
    Read Book Assembler settings from file
    :return: Settings() instance holding string paths
    """

    settings_file = '{}/data/settings.json'.format(assembler_root)

    with open(settings_file, 'r') as file_content:
        settings_data = json.load(file_content)

        return Settings(settings_data)
