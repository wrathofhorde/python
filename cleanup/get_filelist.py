import os
import re
from icecream import ic

# ic.disable()

def is_mp4_file(filename):
    return filename.endswith("mp4")

def is_original_file(filename):
    return True if not re.search(r"\(\d+\)", filename) else False

def is_encoded_file(filename):
    return True if re.search(r"\(\d+\)", filename) else False

def select_mp4(path):
    dir_list = os.listdir(path)
    mp4_list = list(filter(is_mp4_file, dir_list))
    ic(mp4_list)
    return mp4_list

def select_encoded_files(mp4_list):
    encoded_list = list(filter(is_encoded_file, mp4_list))
    ic(encoded_list)
    return encoded_list

def select_original_files(mp4_list):
    org_list = list(filter(is_original_file, mp4_list))
    ic(org_list)
    return org_list

def select_files_to_be_removed(org_list, encoded_list):
    removed = []

    for org in org_list:
        name = org[0: -4]
        for encoded in encoded_files:
            if name in encoded:
                removed.append(org)
                break
    
    ic(removed)
    return removed

def remove_files(path, files):
    dir = path if path[-1] is "/" else path + "/"
    ic(dir)

    fullnames = []
    for file in files:
        fullnames.append(dir + file)

    ic(fullnames)
    for name in fullnames:
        os.remove(name)

def rename_files(path, files):
    dir = path if path[-1] is "/" else path + "/"
    ic(dir)

    for file in files:
        [name, ext] = file.split(".")
        new_name = f"{dir}[{name[0:-3]}].{ext}"
        os.rename(dir + file, new_name)

if __name__ == "__main__":
    path = "C:/Users/wrath/Videos/test"
    mp4_files = select_mp4(path)
    encoded_files = select_encoded_files(mp4_files)
    original_files = select_original_files(mp4_files)
    to_be_removed = select_files_to_be_removed(original_files, encoded_files)
    remove_files(path, to_be_removed)
    rename_files(path, encoded_files)
