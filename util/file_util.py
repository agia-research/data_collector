import json
import os
import shutil


def create_directory(dir, logger):
    if not os.path.exists(dir):
        os.makedirs(dir)
        logger.info("Directory created successfully! Dir: %s", dir)


def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def delete_directory(dir_path):
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)


def list_to_jsonline(json_list):
    total_json_lines = ""
    first = True
    for j in json_list:
        if not first:
            total_json_lines += "\n"
        total_json_lines += json.dumps(j)
        first = False
    return total_json_lines


def save_to_file(file_name, data):
    with open(file_name, "w") as text_file:
        text_file.write(data)


def read_file(file_name):
    data = []
    with open(file_name) as f:
        for line in f:
            data.append(json.loads(line))
    return data
