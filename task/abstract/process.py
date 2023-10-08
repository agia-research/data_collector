import re

import requests
from bs4 import BeautifulSoup
from dateutil import parser

from db.db_utils import open_database, get_not_abstract_added_papers, add_paper_section_to_db, update_paper_work_status, \
    update_paper_date, close_database


def process_for_abstract(paper_id, soup, logger):
    try:
        abstract_block = soup.find('blockquote', {"class": "abstract"})
        abs = abstract_block.text.strip().replace('\n', ' ')
        text = re.findall(r'^Abstract:\s*([\s\S]*)', abs)[0]
        return text
    except:
        logger.info("error processing abstract for : %s", paper_id)


def process_for_date(paper_id, soup, logger):
    try:
        date_block = soup.find('div', {"class": "submission-history"})
        date_str = re.findall(r"\b\d{1,2} \w{3} \d{4} \d{1,2}:\d{2}:\d{2}\b", date_block.text)[0]
        date = parser.parse(date_str)
        return date
    except:
        logger.info("error processing date for : %s", paper_id)


def run(args, logger):
    global abs_base_url
    global abstract_success_count
    global abstract_fail_count
    global date_success_count
    global date_fail_count

    abstract_success_count = 0
    abstract_fail_count = 0
    date_success_count = 0
    date_fail_count = 0

    abs_base_url = 'https://export.arxiv.org/abs/'

    conn, cur = open_database(args.db_host, args.db_username, args.db_password)

    paper_ids = get_not_abstract_added_papers(conn, cur, args.processing_limit)

    loaded_count = len(paper_ids)
    logger.info("Loaded = %s", loaded_count)
    for i in range(loaded_count):
        paper_id = paper_ids[i][0]
        try:
            url = abs_base_url + paper_id
            # print ("processing url=",url)
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            abstract = process_for_abstract(paper_id, soup, logger);

            # abstract
            if abstract:
                add_paper_section_to_db(conn, cur, paper_id, 'abstract', 0, 'abstract', abstract)
                update_paper_work_status(conn, cur, paper_id, 'abstract_added', True)
                abstract_success_count += 1
            else:
                update_paper_work_status(conn, cur, paper_id, 'abstract_added', False)
                abstract_fail_count += 1

            # submission date
            submission_date = process_for_date(paper_id, soup, logger)
            if submission_date:
                update_paper_date(conn, cur, paper_id, submission_date)
                date_success_count += 1
            else:
                date_fail_count += 1
        except Exception as e:
            logger.error("\r❌ Precessing failed. Id = %s %s", paper_id, e)
            conn, cur = open_database(args.db_host, args.db_username, args.db_password)

        if i % args.logs_per_count == 0:
            logger.info("checked= %s", i)
            logger.info("abstract success count= %s", abstract_success_count)
            logger.info("abstract fail count= %s", abstract_fail_count)
            logger.info("date success count= %s", date_success_count)
            logger.info("date fail count= %s", date_fail_count)

    logger.info(
        "checked= %s  a.success= %s  a.fail= %s  d.success= %s d.fail= %s",
        loaded_count,
        abstract_success_count, abstract_fail_count, date_success_count, date_fail_count)

    close_database(conn, cur)
