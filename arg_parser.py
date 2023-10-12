import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    # task
    parser.add_argument("--task", type=str, help="break_sections,download,json_creator,...")

    # db
    parser.add_argument("--db_host", type=str, help="Database host url")
    parser.add_argument("--db_username", type=str, help="Database username")
    parser.add_argument("--db_password", type=str, help="Database password")

    # files

    # process limits
    parser.add_argument("--order_type", type=str, default='asc', help="asc or desc")
    parser.add_argument("--processing_limit", type=int, default=1000, help="Number of papers to process")
    parser.add_argument("--offset", type=int, default=0, help="Starting index of processing")
    parser.add_argument("--logs_per_count", type=int, default=100, help="Number of papers to process")
    parser.add_argument("--timeout", type=int, default=60, help="Number of papers to process")

    # json creator params
    parser.add_argument("--dataset_version", type=str, default="test_v0", help="Dataset version of json creation")
    parser.add_argument("--items_limit_in_file", type=int, default=1000, help="Number of papers in a single file")
    parser.add_argument("--output_file", type=str, default="output", help="Output file name")

    return parser.parse_args()
