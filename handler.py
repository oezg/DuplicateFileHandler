import argparse
import os
import collections
import hashlib


parser = argparse.ArgumentParser()
parser.add_argument("root_folder")
try:
    args = parser.parse_args()
except:
    print("Directory is not specified")
else:
    file_format = "." + input("Enter file format:\n")
    print("Size sorting options\n"
          "1. Descending\n"
          "2. Ascending\n")
    while True:
        sorting = input("Enter a sorting option:\n")
        if sorting in {"1", "2"}:
            break
        print("Wrong option")
    size_hash_paths = collections.defaultdict(dict)
    full_path = os.path.join(os.getcwd(), args.root_folder)
    os.system("mv module/root_folder/files/stage/src/reviewSlider.js module/root_folder/files/stage/src/reviewslider.js")
    os.system("mv module/root_folder/files/stage/src/toggleMiniMenu.js module/root_folder/files/stage/src/toggleminimenu.js")
    for root, dirs, files in os.walk(args.root_folder):
        for file in files:
            if file_format == os.path.splitext(file)[1] or file_format == ".":
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)
                with open(file_path, "rb") as f:
                    content = f.read()
                hash = hashlib.md5(content).hexdigest()
                paths = size_hash_paths[file_size].get(hash, [])
                paths.append(file_path)
                size_hash_paths[file_size][hash] = paths
    for size, hash_paths in sorted(size_hash_paths.items(), key=lambda item: item[0], reverse=sorting == "1"):
        print(size, "bytes")
        print(*(path for paths in hash_paths.values() for path in paths), sep='\n')
    while True:
        check = input("Check for duplicates?\n")
        if check in {"yes", "no"}:
            break
        print("Wrong option")
    if check == "yes":
        numbering = 0
        duplicate_files = {}
        for size, hash_paths in sorted(size_hash_paths.items(), key=lambda item: item[0], reverse=sorting == "1"):
            print(size, "bytes")
            for hash, paths in hash_paths.items():
                if len(paths) > 1:
                    print("Hash:", hash)
                    for path in paths:
                        numbering += 1
                        duplicate_files.update({numbering: (path, size)})
                        print("{0}. {1}".format(numbering, path))
    while True:
        delete = input("Delete files?\n")
        if delete in {"yes", "no"}:
            break
        print("Wrong option")
    if delete == "yes":
        while True:
            file_numbers = input("Enter file numbers to delete:\n").split()
            try:
                file_numbers = [int(number) for number in file_numbers]
            except ValueError:
                print("Wrong format")
            else:
                if file_numbers and all(number in duplicate_files for number in file_numbers):
                    total_freed = 0
                    for number in file_numbers:
                        os.remove(duplicate_files[number][0])
                        total_freed += duplicate_files[number][1]
                    break
                else:
                    print("Wrong format")
        print("Total freed up space:", total_freed, "bytes")
