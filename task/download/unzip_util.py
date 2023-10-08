import shutil


# unzip file
def unzip_file(paper_id):
    try:
        shutil.unpack_archive("Downloads/" + paper_id, "Unzipped/" + paper_id, format="gztar")
        return True
    except:
        return False
