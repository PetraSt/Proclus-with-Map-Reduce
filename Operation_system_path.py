import os
import platform


def write_file(name, data):
    file_with_path = os.path.join(os.path.dirname(__file__), name)
    file_with_path = check_operation_system_path(file_with_path)
    new_file = open(file_with_path, "w+")
    for datum in data:
        new_file.write("{}\n".format(str(datum)))
    new_file.close()


def get_local_path(file):
    path = os.path.join(os.path.dirname(__file__), file)
    return check_operation_system_path(path)


def check_operation_system_path(path):
    if platform.system() == "Windows":
        path = path.replace("/", "\\")
    else:
        path = path.replace("\\", "/")
    return path

