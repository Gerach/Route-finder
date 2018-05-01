#!/usr/bin/env python3

import cv2 as cv
import sqlite3

from map_window import MapWindow


def create_tables(cursor):
    cursor.execute('''CREATE TABLE address(
                          street text, 
                          house integer,
                          x_koord integer,
                          y_koord integer)''')

def insert_into_table(cursor, table_name, *values):
    # print(str(list(values)))
    # cursor.execute("INSERT INTO "+table_name+" VALUES ("+str(list(values))+")")
    # cursor.execute("INSERT INTO "+table_name+" VALUES ('Test address 2', 0, 2, -2)")
    # cursor.execute("INSERT INTO "+table_name+" VALUES ('Test address 3', 1, 3, -3)")

def show_table_contents(cursor, table_name):
    for row in cursor.execute("SELECT * FROM "+table_name):
        print(row)


def main():
    in_file = 'vilnius.png'
    img = cv.imread(in_file)

    database = 'data.sqlite'
    conn = sqlite3.connect(database)
    c = conn.cursor()
    # create_tables(c)
    insert_into_table(c, 'address', 'Test address', 0, 1, -1)
    show_table_contents(c, 'address')

    window = MapWindow(img, "Route finder")
    key = -1
    while key != ord('q') and key != 27 and cv.getWindowProperty(window.WINDOW_NAME, 0) >= 0:
        key = cv.waitKey(1)
    cv.destroyAllWindows()
    conn.close()


if __name__ == '__main__':
    main()
