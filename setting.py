#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

LOGGING = {
    'version': 1,

    'formatters': {
        'simple': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'simple',
            'filename': 'log.log',
            'encoding': 'UTF-8'
        },
    },
    'loggers': {
        'ExcelHandler': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
        }
    }
}

headers = {
    'user-agent':
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/53.0.2785.143 Safari/537.36'
}

error_json = {
    'timestamp': '...',
    'url': '...',
    'error': {
        'exception_type': '...',
        'exception_value': '...',
        'stack_info': '...'
    }
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

path_to_error = BASE_DIR + '\json_files\\'
path_to_log = BASE_DIR + '\log.log'
path_to_DB_SQLite3 = BASE_DIR + '\db_from_excel.db'

SETTING = {
    'timeout': 5,
    'number_threads': 5,
    'path_to_error': path_to_error,
    'path_to_log': path_to_log,
    'path_to_DB_SQLite3': path_to_DB_SQLite3
}

