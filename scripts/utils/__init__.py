import os


def get_source_file_path(csv_subfolder):
    """
    This assumes that the Python Script
    is in one subfolder layer from the root.
    """

    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_directory, _ = os.path.split(script_dir)

    return os.path.join(root_directory, csv_subfolder)


def current_folder_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)
