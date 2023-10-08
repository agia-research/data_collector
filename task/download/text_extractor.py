from os import walk

from db.db_utils import add_paper_text_to_db


def get_files_in_directory(dir_path):
    f = []
    for (dirpath, dirnames, filenames) in walk(dir_path):
        f.extend(filenames)
        break
    return f


def get_main_tex_file(files):
    main_file = None
    tex_files = []
    main_tex_files = []
    bbl_file = None
    for f in files:
        if f.lower().endswith('.tex'):
            tex_files.append(f)
        if f.lower().endswith('.bbl'):
            bbl_file = f
    if len(tex_files) == 1:
        main_file = tex_files[0]
    elif len(tex_files) > 1:
        if bbl_file:
            main_file_temp = bbl_file[:-4] + ".tex"
            if main_file_temp in main_tex_files:
                main_file = main_file_temp
    return main_file


def get_text(base_path, file_name):
    try:
        with open(base_path + "/" + file_name, errors='ignore') as file:
            return file.read()
    except Exception as e:
        return None


def locate_main_text_and_save(conn, cur, paper_id):
    try:
        dir_path = "Unzipped" + "/" + paper_id
        files = get_files_in_directory(dir_path)
        main_tex = get_main_tex_file(files)
        if main_tex is not None:
            raw_text = get_text(dir_path, main_tex)
            add_paper_text_to_db(conn, cur, paper_id, raw_text)
            return True
        else:
            return False
    except:
        return False
