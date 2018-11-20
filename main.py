import os
import sys
import json
import xlrd
import hashlib
import sqlite3
import requests
import datetime
import logging.config
import traceback

from time import time
from multiprocessing.dummy import Pool as ThreadPool
from setting import LOGGING, SETTING, error_json, headers


def get_hash(file):
    file = file.encode('utf-8')
    hash_md5 = hashlib.md5()
    hash_md5.update(file)
    return hash_md5.hexdigest()


def exists_file(path_to_file):
    if os.path.isfile(path_to_file):
        logger.info('File found. File name: ' + path_to_file.split('\\')[-1])
    elif path_to_file[-3:] == '.db':
        logger.info('File not found. The file will be created.')
    else:
        logger.error('FileNotFoundError.\nPath to file: ' + path_to_file)
        raise FileNotFoundError


def create_error_json(url, e, ts):
    exc_type, exc_value, exc_tb = sys.exc_info()
    error_json['timestamp'] = ts
    error_json['url'] = url
    error_json['error']['exception_type'] = e.__class__.__name__
    error_json['error']['exception_value'] = str(exc_value)
    error_json['error']['stack_info'] = ''.join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.error(str(e))
    with open(SETTING['path_to_error'] + ts.replace(':', '-') + '_' + get_hash(url) + '.json', 'w',
              encoding='utf-8') as file:
        json.dump(error_json, file, sort_keys=True, indent=4, ensure_ascii=False)


def get_info_from_excel(path_to_excel):
    local_urls = []
    local_labels = []
    data = xlrd.open_workbook(filename=path_to_excel)
    table = data.sheets()[0]
    for row in range(1, table.nrows):
        if table.cell(row, 2).value == 'ИСТИНА' or table.cell(row, 2).value == 1:
            local_urls.append(table.cell(row, 0).value)
            local_labels.append(table.cell(row, 1).value)
    return local_urls, local_labels


def send_request(url, label):
    ts = datetime.datetime.today().strftime('%Y-%m-%d %H:%M:%S.%f')
    try:
        request = requests.request('GET', url, headers=headers, timeout=SETTING['timeout'])
        response_time = float(request.elapsed.microseconds)
        status_code = request.status_code
        if status_code == 200:
            content_length = len(request.content)
            cur.execute('''INSERT INTO MONITORING VALUES (?, ?, ?, ?, ?, ?)''',
                        (ts, url, label, response_time, status_code, content_length))
        else:
            content_length = None
            cur.execute('''INSERT INTO MONITORING VALUES (?, ?, ?, ?, ?)''',
                        (ts, url, label, response_time, status_code))
        logger.info('''
        Send to DB:
        TS              = {}
        URL             = {}
        LABEL           = {}
        RESPONSE_TIME   = {}
        STATUS_CODE     = {}
        CONTENT_LENGTH  = {}
        '''.format(ts, url, label, response_time, status_code, content_length))
    except requests.ConnectionError as e:
        create_error_json(url, e, ts)
    except requests.HTTPError as e:
        create_error_json(url, e, ts)
    except requests.URLRequired as e:
        create_error_json(url, e, ts)
    except requests.Timeout as e:
        create_error_json(url, e, ts)
    except requests.TooManyRedirects as e:
        create_error_json(url, e, ts)
    except requests.RequestException as e:
        create_error_json(url, e, ts)


def send_to_db(local_urls, local_labels):
    try:
        number_pool = SETTING['number_threads']
        pool = ThreadPool(number_pool)
        for k in range(0, len(local_urls), number_pool):
            if k + number_pool > len(local_urls):
                pool.starmap(send_request, zip(local_urls[k:], local_labels[k:]))
            else:
                pool.starmap(send_request, zip(local_urls[k: k + number_pool], local_labels[k: k + number_pool]))
        conn.commit()
        pool.close()
        pool.join()
    except sqlite3.ProgrammingError as e:
        logger.error(str(e))


if __name__ == '__main__':
    time_begin = time()
    logging.config.dictConfig(LOGGING)
    logger = logging.getLogger('ExcelHandler')
    logger.info('The program is started.')

    path_to_excel_file = sys.argv[1]
    exists_file(path_to_excel_file)

    exists_file(SETTING['path_to_DB_SQLite3'])

    conn = sqlite3.connect(SETTING['path_to_DB_SQLite3'], check_same_thread=False)
    cur = conn.cursor()

    cur.execute('''create table if not exists MONITORING (
                                TS              timestamp not null,
                                URL             string not null,
                                LABEL           string not null,
                                RESPONSE_TIME   float,
                                STATUS_CODE     integer default null,
                                CONTENT_LENGTH  integer default null)''')
    conn.commit()

    urls, labels = get_info_from_excel(path_to_excel_file)
    send_to_db(urls, labels)

    conn.close()

    logger.info('The execution time of the program (s): ' + str((time() - time_begin)))
    logger.info('The program is stopped.')