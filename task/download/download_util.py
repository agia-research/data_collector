import requests


# download a file from url
def download_file(index, url, paper_id):
    try:
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open("Downloads/" + paper_id, "wb") as file:
                for block in r.iter_content(chunk_size=1024):
                    if block:
                        file.write(block)
            return True
        else:
            return False
    except:
        return False
