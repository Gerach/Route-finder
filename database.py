#!/usr/bin/env python3

import sqlite3
import sys


class Database(object):
    def __init__(self, file_name):
        self.conn = sqlite3.connect(file_name)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS address(
                              street TEXT NOT NULL, 
                              house INTEGER NOT NULL,
                              x_coord INTEGER NOT NULL,
                              y_coord INTEGER NOT NULL,
                              PRIMARY KEY(street, house)
                              )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS road(
                              road_id INTEGER NOT NULL PRIMARY KEY,
                              street TEXT,
                              house INTEGER,
                              speed_limit INTEGER,
                              x1_coord INTEGER NOT NULL,
                              y1_coord INTEGER NOT NULL,
                              x2_coord INTEGER NOT NULL,
                              y2_coord INTEGER NOT NULL,
                              FOREIGN KEY (street, house) REFERENCES address(street,house)
                              )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS traffic_light(
                              x_coord INTEGER NOT NULL,
                              y_coord INTEGER NOT NULL,
                              road_id INTEGER NOT NULL,
                              green_light INTEGER,
                              red_light INTEGER,
                              PRIMARY KEY (x_coord, y_coord),
                              FOREIGN KEY (road_id) REFERENCES road(road_id)
                              )''')
        self.conn.commit()

    def insert_address(self, values):
        try:
            self.cursor.executemany('INSERT INTO address VALUES (?,?,?,?)', values)
            self.conn.commit()
        except sqlite3.ProgrammingError:
            print('Invalid argument count given for address insertion.')
            sys.exit(1)

    def insert_road(self, values):
        try:
            self.cursor.executemany('INSERT INTO road(street, house, speed_limit, x1_coord, y1_coord, x2_coord, y2_coord) VALUES (?,?,?,?,?,?,?)', values)
            self.conn.commit()
        except sqlite3.ProgrammingError:
            print('Invalid argument count given for road insertion.')
            sys.exit(1)

    def insert_traffic_light(self, values):
        try:
            self.cursor.executemany('INSERT INTO traffic_light VALUES (?,?,?,?,?)', values)
            self.conn.commit()
        except sqlite3.ProgrammingError:
            print('Invalid argument count given for traffic light insertion.')
            sys.exit(1)

    def select_address(self, street, house):
        self.cursor.execute(
            "SELECT x_coord, y_coord FROM address WHERE street = ? AND house = ?", (street, house))
        return self.cursor.fetchone()

    def select_road(self, road_id):
        self.cursor.execute(
            "SELECT * FROM road WHERE road_id = ?", road_id)
        return self.cursor.fetchone()

    def show_table_contents(self, table_name):
        for row in self.cursor.execute("SELECT * FROM " + table_name):
            print(row)