#!/usr/bin/env python3
''' a function called filter_datum that returns the log message obfuscated'''

import re
from typing import List
import logging
import os
import mysql.connector


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    '''returns the log message obfuscated
    Args:
        fields: a list of strings representing all fields to obfuscate
        redaction: a string representing by what the field will be obfuscated
        message: a string representing the log line
        separator: a string representing by which character is separating
        all fields in the log line (message)
    '''
    for field in fields:
        message = re.sub(rf"{field}=.*?{separator}",
                         f"{field}={redaction}{separator}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initialize RedactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """filter values in incoming log records using filter_datum"""
        message = super().format(record)
        ms = filter_datum(self.fields, self.REDACTION, message, self.SEPARATOR)
        return ms


PII_FIELDS = ('name',
              'email',
              'phone',
              'ssn',
              'password')


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream = logging.StreamHandler()
    stream.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(stream)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""

    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database_name = os.getenv('PERSONAL_DATA_DB_NAME')
    connection = mysql.connector.connect(user=user, password=password,
                                         host=host, database=database_name)
    return connection
