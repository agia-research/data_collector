import requests
from bs4 import BeautifulSoup

from db.db_utils import is_already_added, add_paper_to_db


def process_page(conn, cur, url, download_base_url, logger):
    global collect_success_count
    global download_success_count
    global download_failed_count
    global no_source_count
    global already_exist_count

    logger.info("processing url= %s", url)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    ppr_links = soup.find_all("li", {"class": "arxiv-result"})

    for ppr_link in ppr_links:
        id, link, tags, is_primary_cl, title, has_latex_source, latex_url = get_papper_details(ppr_link)

        # print(id,link,tags,is_primary_cl,title,has_latex_source,latex_url)
        if is_already_added(conn, cur, id) == False:
            if has_latex_source:
                download_url = download_base_url + "/" + id
                add_paper_to_db(conn, cur, id, title, tags, latex_url, download_url)
                # print("\r✅ Added to db. Session Number = {} : Id = {} : Title = {} : Download Url = {}".format(collect_success_count,id,title,download_url))
                collect_success_count = collect_success_count + 1
            else:
                no_source_count = no_source_count + 1
                # print("⚠️ Source not found - Id = {} : Title = {}".format( id, title ))

        else:
            already_exist_count = already_exist_count + 1
            # print("❗ Paper alerady exists - Id = {} : Title = {}".format( id, title ))
    print_summary(logger)

    next_page_url_block = soup.find("a", {"class": "pagination-next"})
    has_next_page = False
    next_page_url = None
    if next_page_url_block:
        has_next_page = True
        next_page_url = next_page_url_block["href"]
    else:
        print(soup)

    return has_next_page, next_page_url


# get zip file name from paper id
def trim_id(id):
    return id.split("arXiv:", 1)[1].replace("/", "-")


# get zip file name from paper id
def trim_title(title):
    return title.strip()


def get_papper_details(paper_result):
    id_block = paper_result.find_all('p', {"class": "list-title"})[0]
    id = None
    link = None
    tags = list(map(lambda x: x.text, paper_result.find_all("span", {"class": "tag"})))
    is_primary_cl = False
    has_latex_source = False
    latex_url = None
    title = paper_result.find('p', {"class": "title"}).text
    if title:
        title = trim_title(title)
    if id_block:
        if id_block.a:
            id = trim_id(id_block.a.text)
            link = id_block.a["href"]
        if id_block.span:
            format_blocks = id_block.span.find_all()
            for f in format_blocks:
                if f.text == "other":
                    has_latex_source = True
                    latex_url = f["href"]
    if len(tags) > 0:
        is_primary_cl = tags[0] == 'cs.CL'
    return id, link, tags, is_primary_cl, title, has_latex_source, latex_url


def print_summary(logger):
    global collect_success_count
    global download_success_count
    global download_failed_count
    global no_source_count
    global already_exist_count

    logger.info()
    logger.info("Success collects : %s", collect_success_count)
    logger.info("Success downloads : %s", download_success_count)
    logger.info("Failed downloads : %s", download_failed_count)
    logger.info("No source papers : %s", no_source_count)
    logger.info("Already added papers : %s", already_exist_count)
    logger.info("Total checked: %s", collect_success_count + no_source_count + already_exist_count)
    logger.info()
