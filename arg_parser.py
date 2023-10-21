import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    # task
    parser.add_argument("--task", type=str, help="Task name : collect_papers,download,break_sections,json_creator,...")

    # db
    parser.add_argument("--db_host", type=str, help="Database host url")
    parser.add_argument("--db_username", type=str, help="Database username")
    parser.add_argument("--db_password", type=str, help="Database password")

    # paper collector
    parser.add_argument("--from_date", type=str, default="2023-01-01", help="From date")
    parser.add_argument("--to_date", type=str, default="2023-02-01", help="To date")

    # files

    # process limits
    parser.add_argument("--order_type", type=str, default='asc', help="asc or desc")
    parser.add_argument("--processing_limit", type=int, default=1000, help="Number of papers to process")
    parser.add_argument("--offset", type=int, default=0, help="Starting index of processing")
    parser.add_argument("--logs_per_count", type=int, default=100, help="Number of papers to process")
    parser.add_argument("--timeout", type=int, default=60, help="Number of papers to process")
    parser.add_argument("--paper_id", type=str, help="Specific paper id for processing")

    # json creator params
    parser.add_argument("--dataset_version", type=str, default="test_v0", help="Dataset version of json creation")
    parser.add_argument("--items_limit_in_file", type=int, default=1000, help="Number of papers in a single file")
    parser.add_argument("--output_file", type=str, default="output", help="Output file name")

    return parser, parser.parse_args()
