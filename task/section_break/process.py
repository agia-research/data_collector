from func_timeout import FunctionTimedOut, func_timeout

from db.db_utils import open_database, get_not_section_extracted_paper_ids, get_paper_text, add_paper_section_to_db, \
    update_paper_work_status, close_database
from task.section_break.latex_parser import parse_latex
from util.common import get_percentage


def process_paper_parse_sections(args, logger):
    global section_parsed_success_count
    global section_parsed_fail_count

    conn, cur = open_database(args.db_host, args.db_username, args.db_password)

    unprocessed_paper_ids = get_not_section_extracted_paper_ids(conn, cur,args.order_type, args.processing_limit, args.offset)

    length = len(unprocessed_paper_ids)
    logger.info("total loaded: %s", length)
    for pi in range(length):
        paper_id, = unprocessed_paper_ids[pi]
        _, paper_text = get_paper_text(conn, cur, paper_id)

        try:
            # sec_map = parse_latex(paper_text)
            sec_map = func_timeout(args.timeout, parse_latex, args=(paper_text,))
            sec_index = 1  # 0 is given to abstract and it is added by a seperate process
            for sec in sec_map:
                add_paper_section_to_db(conn, cur, paper_id, sec.strip(), sec_index, None, sec_map[sec].strip())
                sec_index += 1
            section_parsed_success_count += 1
            update_paper_work_status(conn, cur, paper_id, 'section_extracted', True)
        except FunctionTimedOut:
            logger.error("\r❌ Precessing failed by Timeout. Id = {}".format(paper_id))
            section_parsed_fail_count += 1
        except Exception as e:
            logger.error("\r❌ Precessing failed. Id = {} {}".format(paper_id, e))
            section_parsed_fail_count += 1
            conn.rollback()
            conn, cur = open_database(args.db_host, args.db_username, args.db_password)

        if (pi + 1) % args.logs_per_count == 0:
            logger.info("%s checked= %s  success= %s  fail= %s", get_percentage(length, pi), pi + 1,
                        section_parsed_success_count,
                        section_parsed_fail_count)

    logger.info("checked= %s  success= %s  fail= %s", len(unprocessed_paper_ids), section_parsed_success_count,
                section_parsed_fail_count)
    close_database(conn, cur)


def run(args, logger):
    global section_parsed_success_count
    global section_parsed_fail_count

    section_parsed_success_count = 0
    section_parsed_fail_count = 0

    process_paper_parse_sections(args, logger)
