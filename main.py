#!/usr/bin/env python3

import cv2 as cv
import sys

from map_window import MapWindow
from database import Database


def check_input(value):
    address = value.rsplit(' ', 1)
    if len(address) != 2:
        print('Invalid address format provided.')
        sys.exit(1)
    elif address[0] is '' or address[1] is '':
        print('Invalid address format provided.')
        sys.exit(1)
    return address


def main():
    in_file = 'vilnius.png'
    img = cv.imread(in_file)

    loc_address = check_input(sys.argv[1])
    dest_address = check_input(sys.argv[2])

    db = Database('data.sqlite')
    addresses = [('Naugarduko', 24, 2400, 2870),
                 ('Didlaukio', 47, 2210, 1020),
                 ]
    db.insert_address(addresses)
    # db.show_table_contents('address')
    loc_coord = db.select_address(loc_address[0], loc_address[1])
    dest_coord = db.select_address(dest_address[0], dest_address[1])

    window = MapWindow(img, loc_coord, dest_coord, "Route finder")
    key = -1
    while key != ord('q') and key != 27 and cv.getWindowProperty(window.WINDOW_NAME, 0) >= 0:
        key = cv.waitKey(1)
    cv.destroyAllWindows()

    # db.conn.commit()
    db.conn.close()


if __name__ == '__main__':
    main()
