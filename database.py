#!/usr/bin/env python3

import sqlite3
import sys


class Database(object):
    def __init__(self, file):
        self.conn = sqlite3.connect(file)
        # self.conn.text_factory = str
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE address(
                              street text, 
                              house integer,
                              x_coord integer,
                              y_coord integer)''')

    def insert_address(self, values):
        try:
            self.cursor.executemany('INSERT INTO address VALUES (?,?,?,?)', values)
        except sqlite3.ProgrammingError:
            print('Invalid argument count given for address insertion.')
            sys.exit(1)

    def select_address(self, street, house):
        self.cursor.execute(
            "SELECT x_coord, y_coord FROM address WHERE street = '{0}' AND house = '{1}'".format(street, house))
        return self.cursor.fetchone()

    def show_table_contents(self, table_name):
        for row in self.cursor.execute("SELECT * FROM " + table_name):
            print(row)