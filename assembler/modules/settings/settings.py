"""
Module to read/writes settings from/to JSON file
"""

import os
import json

assembler_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))).replace('\\', '/')


class Settings:
    """
    Object to store settings
    """

    def __init__(self, settings_data):
        # Setting attributes
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
        """

        self.project_root = settings_data['project_root']['string']
        self.jpeg_folder = settings_data['jpeg_folder']['string']
        project_root = self.project_root  # Required for eval() to expand strings

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


def set_settings(project_folder, versioned_pages, final_pages, pdf_files, sql_file_path):
    """
    Edit settings
    """

    settings_file = '{}/data/settings.json'.format(assembler_root)
    settings_src = get_settings()

    settings_data = {"project_root": {
                        "string": project_folder,
                        "token": None},

                     "versioned_pages": {
                        "string": "{}".format(versioned_pages.replace(settings_src.project_root, '{}')),
                        "token": "project_root"},

                     "final_pages": {
                        "string": "{}".format(final_pages.replace(settings_src.project_root, '{}')),
                        "token": "project_root"},

                     "pdf_files":  {
                         "string": "{}".format(pdf_files.replace(settings_src.project_root, '{}')),
                         "token": "project_root"},

                     "sql_file_path": {
                        "string": "{}".format(sql_file_path.replace(assembler_root, '{}')),
                        "token": "assembler_root"},

                     "jpeg_folder": {
                        "string": "1rgsj0IsRrk1jKjO1WfpnuJISiDgwze-O",
                        "token":  None}
                     }

    # Write new settings
    with open(settings_file, 'w') as file_content:
        json.dump(settings_data, file_content, indent=4)
