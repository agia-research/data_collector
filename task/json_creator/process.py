from db.db_utils import open_database, get_section_extracted_papers, get_paper_sections, update_paper_dataset_version, \
    get_section_extracted_paper_by_id
from task.json_creator.paper_data import create_map
from util.file_util import list_to_jsonline, save_to_file, create_directory


def create_json_files(args, logger):
    global success_count
    global failed_count

    conn, cur = open_database(args.db_host, args.db_username, args.db_password)

    if args.paper_id:
        papers = get_section_extracted_paper_by_id(conn, cur, args.paper_id)
    else:
        papers = get_section_extracted_papers(conn, cur, args.dataset_version, args.order_type, args.processing_limit,
                                              args.offset)
    loaded_count = len(papers)
    items_in_file = []
    file_number = 1
    create_directory(args.dataset_version, logger)
    output_file = "../"+args.dataset_version + "/" + args.output_file + "_" + str(args.offset)
    for i in range(loaded_count):
        paper = papers[i]
        paper_id = paper[0]
        try:
            sections = get_paper_sections(conn, cur, paper_id)
            obj = create_map(paper, sections)
            items_in_file.append(obj)
            if ((i > 0 and i % args.items_limit_in_file == 0) or i == loaded_count - 1):
                line = list_to_jsonline(items_in_file)
                save_to_file(output_file + "_" + str(file_number * args.items_limit_in_file) + ".jsonl", line)
                file_number += 1
                items_in_file = []
            if not args.paper_id:  # update dataset version only if testing
                update_paper_dataset_version(conn, cur, paper_id, args.dataset_version)
            success_count += 1
        except Exception as e:
            failed_count += 1
            logger.error("Error processing: %s", paper_id)
            conn, cur = open_database(args.db_host, args.db_username, args.db_password)

        if i % args.logs_per_count == 0 or i == loaded_count - 1:
            logger.info("checked= %s", i + 1)
            logger.info("success count= %s", success_count)
            logger.info("fail count= %s", failed_count)


def run(args, logger):
    global success_count
    global failed_count

    success_count = 0
    failed_count = 0

    create_json_files(args, logger)
