from db.db_utils import open_database, get_not_downloaded_papers, update_paper_stage, close_database
from task.download.download_util import download_file
from task.download.text_extractor import locate_main_text_and_save
from task.download.unzip_util import unzip_file
from util.common import get_percentage
from util.file_util import create_directory, delete_file, delete_directory


def process_paper_d_z_t(args, logger):
    global download_success_count
    global download_fail_count
    global unzip_success_count
    global unzip_fail_count
    global text_success_count
    global text_fail_count

    create_directory("Downloads", logger)
    create_directory("Unzipped", logger)

    conn, cur = open_database(args.db_host, args.db_username, args.db_password)

    unprocessed_papers = get_not_downloaded_papers(conn, cur, args.order_type, args.processing_limit,  args.offset)

    length = len(unprocessed_papers)
    logger.info("total loaded: %s", length)
    for i in range(length):
        paper_id, download_url = unprocessed_papers[i]

        try:
            downloaded = download_file(i, download_url, paper_id)
            if downloaded:
                download_success_count += 1

                unzipped = unzip_file(paper_id)
                if unzipped:
                    unzip_success_count += 1

                    text_extracted = locate_main_text_and_save(conn, cur, paper_id)
                    if text_extracted:
                        text_success_count += 1
                        update_paper_stage(conn, cur, paper_id, 1)
                    else:
                        text_fail_count += 1
                        update_paper_stage(conn, cur, paper_id, 42)

                else:
                    unzip_fail_count += 1
                    update_paper_stage(conn, cur, paper_id, 41)


            else:
                download_fail_count += 1
                update_paper_stage(conn, cur, paper_id, 40)

            delete_file('Downloads/' + paper_id)
            delete_directory('Unzipped/' + paper_id)
        except:
            logger.error("\r❌ Precessing failed. Id = {}".format(paper_id))
            conn, cur = open_database(args.db_host, args.db_username, args.db_password)

        if (i + 1) % args.logs_per_count == 0:
            logger.info(
                "%s  checked= %s  d.success= %s  d.fail= %s  unz.success= %s  unz.fail= %s  t.success= %s  t.fail= %s",
                get_percentage(length, i),
                i + 1,
                download_success_count, download_fail_count, unzip_success_count, unzip_fail_count, text_success_count,
                text_fail_count)

    logger.info(
        "checked= %s  d.success= %s  d.fail= %s  unz.success= %s  unz.fail= %s  t.success= %s  t.fail= %s",
        length,
        download_success_count, download_fail_count, unzip_success_count, unzip_fail_count, text_success_count,
        text_fail_count)
    close_database(conn, cur)


def run(args, logger):
    global download_success_count
    global download_fail_count
    global unzip_success_count
    global unzip_fail_count
    global text_success_count
    global text_fail_count

    download_success_count = 0
    download_fail_count = 0
    unzip_success_count = 0
    unzip_fail_count = 0
    text_success_count = 0
    text_fail_count = 0

    process_paper_d_z_t(args, logger)
