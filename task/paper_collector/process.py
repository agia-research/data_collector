from db.db_utils import open_database, close_database
from task.paper_collector.page_processor import process_page


def collect_papers(args, logger):

    global collect_success_count
    global download_success_count
    global download_failed_count
    global no_source_count
    global already_exist_count

    conn, cur = open_database(args.db_host, args.db_username, args.db_password)

    download_root_url = "https://export.arxiv.org/e-print"
    base_url = 'https://arxiv.org/'

    from_date = args.from_date  # @param {type: "string"}
    to_date = args.to_date  # @param {type: "string"}

    intial_page_url = "https://arxiv.org/search/advanced?advanced=&terms-0-operator=AND&terms-0-term=&terms-0-field=all&classification-physics_archives=all&classification-include_cross_list=include&date-year=&date-filter_by=date_range&date-from_date=" + str(
        from_date) + "&date-to_date=" + str(
        to_date) + "&date-date_type=submitted_date&abstracts=hide&size=200&order=-announced_date_first"

    has_next_page = True
    next_page_url = intial_page_url
    while (has_next_page):
        has_next_page, next_page_url_part = process_page(conn, cur, next_page_url, download_root_url, logger)
        logger.info("has_next_page = %s", has_next_page)
        if has_next_page:
            next_page_url = base_url + next_page_url_part
        else:
            logger.info("No more pages")

    close_database(conn, cur)
    pass


def run(args, logger):
    global collect_success_count
    global download_success_count
    global download_failed_count
    global no_source_count
    global already_exist_count

    collect_success_count = 0
    download_success_count = 0
    download_failed_count = 0
    no_source_count = 0
    already_exist_count = 0

    collect_papers(args, logger)