import logging
from datetime import datetime

from pytz import timezone

import arg_parser
from task.abstract.process import run as abstract_run
from task.download.process import run as download_run
from task.json_creator.process import run as json_creator_run
from task.section_break.process import run as section_break_run
from task.status.process import show_chart as show_chart


def get_logger(log_file):
    logging.Formatter.converter = lambda *args: datetime.now(tz=timezone('Asia/Kolkata')).timetuple()
    logger = logging.getLogger('DC_APP')
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    # stdout_handler = logging.StreamHandler(sys.stdout)
    # stdout_handler.setLevel(logging.DEBUG)
    # stdout_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    # logger.addHandler(stdout_handler)
    return logger


if __name__ == '__main__':

    parser, args = arg_parser.parse_args()
    logging.info('Args : %s', args)

    if args.task == 'break_sections':
        logger = get_logger('break_sections.log')
        logger.info("Section breaking started")
        section_break_run(args, logger)
        logger.info("Section breaking finished")

    if args.task == 'download':
        logger = get_logger('download_' + args.order_type + '.log')
        logger.info("Downloading started")
        download_run(args, logger)
        logger.info("Downloading finished")

    if args.task == 'json_creator':
        logger = get_logger('json_creator_' + args.order_type + '.log')
        logger.info("Json creator started")
        json_creator_run(args, logger)
        logger.info("Json creator finished")

    if args.task == 'abstract':
        logger = get_logger('abstract_' + args.order_type + '.log')
        logger.info("Abstract adding started")
        abstract_run(args, logger)
        logger.info("Abstract adding finished")

    if args.task == 'status':
        show_chart(args)

    if args.task == 'help':
        parser.print_help()
