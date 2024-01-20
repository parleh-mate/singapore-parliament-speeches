import os


def get_root_path():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_directory, _ = os.path.split(script_dir)

    return root_directory


def join_path(root_path, file_path):
    return os.path.join(root_path, file_path)
