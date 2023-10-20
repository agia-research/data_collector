import psycopg2

schema = "agia"


# open database of the result
def open_database(host, username, password):
    connection = psycopg2.connect(
        database="postgres",
        user=username,
        password=password,
        host=host,
        port="5432"
    )
    cursor = connection.cursor()
    return connection, cursor


# close database
def close_database(conn, cur):
    cur.close
    conn.close()


#  list loaders

def get_not_downloaded_papers(conn, cur, order_type, limit, offset=0):
    global schema
    cur.execute(
        '''SELECT paper_id, download_url FROM ''' + schema + '''.paper where stage=-1 
        order by submission_date ''' + order_type + ''' limit %s offset %s''',
        (limit, offset))
    return cur.fetchall()


def get_not_section_extracted_papers(conn, cur, order_type, limit, offset=0):
    global schema
    cur.execute(
        '''select p.paper_id, pt.text from ''' + schema + '''.paper p join ''' + schema + '''.paper_text pt on 
        p.paper_id = pt.paper_id  where p.stage = 1 and p.abstract_added=true and (p.section_extracted is null or 
        p.section_extracted=false) order by p.submission_date ''' + order_type + ''' limit %s offset %s''',
        (limit, offset))
    return cur.fetchall()


def get_not_section_extracted_paper_ids(conn, cur, order_type, limit, offset=0):
    global schema
    cur.execute(
        '''select p.paper_id from ''' + schema + '''.paper p where p.stage = 1 and p.abstract_added=true and (
        p.section_extracted is null or p.section_extracted=false) order by p.submission_date ''' + order_type + '''
         limit %s offset %s''',
        (limit, offset))
    return cur.fetchall()


def get_section_extracted_papers(conn, cur, dataset_version, order_type, limit, offset=0):
    global schema
    cur.execute(
        '''select p.paper_id, p.name, p.tags, p.submission_date from ''' + schema + '''.paper p  where 
        p.section_extracted=true order by p.submission_date ''' + order_type + ''' limit %s offset %s''',
        (limit, offset))
    return cur.fetchall()

def get_raw_data_papers(conn, cur, dataset_version, order_type, limit, offset=0):
    global schema
    cur.execute(
        '''select p.paper_id, p.name, p.tags, p.submission_date from ''' + schema + '''.paper p 
         join paper_text pt on p.paper_id =pt.paper_id where pt."text" is not null order by p.submission_date ''' + order_type + ''' limit %s offset %s''',
        (limit, offset))
    return cur.fetchall()

def get_section_extracted_top_papers(conn, cur, dataset_version, order_type, limit, offset=0):
    global schema
    cur.execute(
        '''select p.paper_id, p.name, p.tags, p.submission_date from ''' + schema + '''.paper p  where 
        p.paper_id in (select
            distinct paper_id
          from
            agia.paper_section
          where
            paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'introduction')
            and paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'related_work')
            and paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'methodology')
            and paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'results')
            and paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'conclusion'))''')
    return cur.fetchall()

def get_evaluating_paper_ids(conn, cur):
    cur.execute(
        '''select
            distinct paper_id
          from
            agia.paper_section
          where
            paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'introduction')
            and paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'related_work')
            and paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'methodology')
            and paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'results')
            and paper_id in (
            select
              paper_id
            from
              agia.paper_section
            where
              generalized_section_name = 'conclusion')''')
    return cur.fetchall()

def get_section_extracted_paper_by_id(conn, cur, paper_id):
    global schema
    cur.execute(
        '''select p.paper_id, p.name, p.tags, p.submission_date from ''' + schema + '''.paper p  where 
        p.paper_id = %s''',
        (paper_id,))
    return cur.fetchall()


def get_not_abstract_added_papers(conn, cur, order_type, limit, offset=0):
    global schema
    cur.execute(
        '''SELECT paper_id FROM ''' + schema + '''.paper where abstract_added is null or abstract_added=false 
        order by submission_date ''' + order_type + ''' limit %s offset %s''',
        (limit, offset))
    return cur.fetchall()


# other getters

def get_paper_text(conn, cur, paper_id):
    global schema
    cur.execute(
        '''select pt."text" from ''' + schema + '''.paper p join ''' + schema + '''.paper_text pt on 
        p.paper_id = pt.paper_id  where p.paper_id = %s''',
        (paper_id,))
    return cur.fetchone()


def get_paper_abstract(conn, cur, paper_id):
    global schema
    cur.execute(
        '''select ps."text" from ''' + schema + '''.paper_section ps where ps.section_name = %s and ps.paper_id 
        = %s''',
        ('abstract',paper_id,))
    return cur.fetchone()

def get_paper_sections(conn, cur, paper_id):
    global schema
    cur.execute(
        '''select ps.section_name, ps.generalized_section_name, ps.text from agia.paper_section ps where ps.paper_id = %s order by section_index''',
        (paper_id,))
    return cur.fetchall()


# counts
def get_total_paper_count(conn, cur):
    global schema
    cur.execute('''SELECT count(paper_id) FROM ''' + schema + '''.paper''')
    count = cur.fetchone()[0]
    return count


## get number of papers in stage
def get_paper_count(conn, cur, stage):
    global schema
    cur.execute('''SELECT count(paper_id) FROM ''' + schema + '''.paper where stage=%s''', (stage,))
    count = cur.fetchone()[0]
    return count


## get number of papers in work status
def get_paper_work_status_count(conn, cur, work_status_key, work_status_value):
    global schema
    cur.execute('''SELECT count(paper_id) FROM ''' + schema + '''.paper where ''' + work_status_key + '''= %s''',
                (work_status_value,))
    count = cur.fetchone()[0]
    return count


# save
def add_paper_text_to_db(conn, cur, id, text):
    global schema
    cur.execute('''INSERT INTO ''' + schema + '''.paper_text(paper_id,text) values (%s, %s)''', (id, text))
    conn.commit()


def add_paper_section_to_db_atomic(conn, cur, id, section, section_index, generalized_section_name, text):
    global schema
    cur.execute(
        '''INSERT INTO ''' + schema + '''.paper_section(paper_id,section_name,section_index,generalized_section_name,text) values (%s, %s, %s, %s, %s)''',
        (id, section, section_index, generalized_section_name, text))


def add_paper_section_to_db(conn, cur, id, section, section_index, generalized_section_name, text):
    global schema
    cur.execute(
        '''INSERT INTO ''' + schema + '''.paper_section(paper_id,section_name,section_index,generalized_section_name,text) values (%s, %s, %s, %s, %s)''',
        (id, section, section_index, generalized_section_name, text))
    conn.commit()


# update
def update_paper_stage(conn, cur, paper_id, stage):
    cur.execute('''update ''' + schema + '''.paper set stage=%s where paper_id=%s;''', (stage, paper_id))
    conn.commit()


def update_paper_work_status(conn, cur, id, work_status_key, status):
    global schema
    cur.execute('''update ''' + schema + '''.paper set ''' + work_status_key + '''= %s where paper_id= %s''',
                (status, id))
    conn.commit()


def update_paper_dataset_version(conn, cur, id, dataset_version):
    global schema
    cur.execute('''update ''' + schema + '''.paper set dataset_version = %s where paper_id= %s''',
                (dataset_version, id))
    conn.commit()


def update_paper_date(conn, cur, paper_id, date):
    cur.execute('''update ''' + schema + '''.paper set submission_date=%s where paper_id=%s;''', (date, paper_id))
    conn.commit()
