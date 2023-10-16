# Data Collector

This collect research papers from [arXiv](https://arxiv.org/), extract texts from the papers and devide paper sections.
These are done by separate tasks.

Tasks are,

1. Initial paper information extractor
2. Add abstract and submission date
3. Download latex source, Unzip, Extract text
4. Break sections of extracted texts
5. Generate `jsonl` files of extracted data

## Setting up database

1. PostgreSQL database is needed with these 3 tables

```sql
CREATE TABLE paper (
	paper_id varchar(20) NOT NULL,
	"name" varchar(255) NULL,
	tags varchar(255) NULL,
	paper_page varchar(255) NULL,
	download_url varchar(512) NULL,
	stage int4 NULL,
	submission_date timestamp NULL,
	abstract_added bool NULL,
	section_extracted bool NULL,
	dataset_version varchar(30) NULL,
	CONSTRAINT paper_pkey PRIMARY KEY (paper_id)
);
```

```sql
CREATE TABLE paper_text (
	paper_id varchar(20) NOT NULL,
	"text" text NOT NULL,
	CONSTRAINT paper_text_pkey PRIMARY KEY (paper_id)
);

-- paper_text foreign keys
ALTER TABLE paper_text ADD CONSTRAINT paper_text_paper_id_fkey FOREIGN KEY (paper_id) REFERENCES paper(paper_id);
```

```sql
CREATE TABLE paper_section (
	paper_id varchar(20) NOT NULL,
	section_name varchar(255) NOT NULL,
	section_index int2 NOT NULL,
	"text" text NOT NULL,
	generalized_section_name varchar(255) NULL,
	CONSTRAINT paper_section_pkey PRIMARY KEY (paper_id, section_name, section_index)
);

-- paper_section foreign keys
ALTER TABLE paper_section ADD CONSTRAINT paper_section_paper_id_fkey FOREIGN KEY (paper_id) REFERENCES paper(paper_id);
```

2. Update the `schema` name in file `db/db_utils.py`

# Tasks

## Paramters

```shell
  --task                Task name : break_sections,download,json_creator,...
  --db_host             Database host url
  --db_username         Database username
  --db_password         Database password
  --order_type          asc or desc
  --processing_limit    Number of papers to process
  --offset              Starting index of processing
  --logs_per_count      Number of papers to process
  --timeout             Number of papers to process
  --paper_id            Specific paper id for processing
  --dataset_version     Dataset version of json creation
  --items_limit_in_file Number of papers in a single file
  --output_file         Output file name

```

## 0. Check database status

```shell
python3 main.py --task=status \
  --db_host=<_host_url_> --db_username=<_username_> --db_password=<_password_>
```

## 1. Initial paper information extractor

yet to be added

## 2. Add abstract and submission date

```shell
python3 main.py --task=abstract --order_type=desc --processing_limit=50000 --offset=0 \
  --timeout=10 --logs_per_count=100 \
  --db_host=<_host_url_> --db_username=<_username_> --db_password=<_password_>
```

## 3. Download latex source, Unzip, Extract text

```shell
python3 main.py --task=download --order_type=asc --processing_limit=50000 --offset=0 \
  --timeout=10 --logs_per_count=100 \
  --db_host=<_host_url_> --db_username=<_username_> --db_password=<_password_>
```

## 4. Break sections of extracted texts

```shell
python3 main.py --task=break_sections --processing_limit=50000 --offset=0 \
  --timeout=10 --logs_per_count=100 \
  --db_host=<_host_url_> --db_username=<_username_> --db_password=<_password_>
```

## 5. Generate `jsonl` files of extracted data

```shell
python3 main.py --task=json_creator --processing_limit=1000000 --offset=0 \
  --items_limit_in_file=10000 --logs_per_count=1000 \
  --dataset_version=loval_v1 \
  --db_host=<_host_url_> --db_username=<_username_> --db_password=<_password_>
```

