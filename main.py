#!/usr/bin/env python3

import cv2 as cv

from map_window import MapWindow
from database import Database


def main():
    in_file = 'vilnius.png'
    img = cv.imread(in_file)

    db = Database('data.sqlite')
    addresses = [('Test address', 0, 1, -1),
                 ('Test address2', 1, 2, -2),
                 ('Test address3', 3, 3, -3),
                 ]
    db.insert_address(addresses)
    # db.show_table_contents('address')
    print(db.select_address('Test address2', 1))



    # window = MapWindow(img, "Route finder")
    # key = -1
    # while key != ord('q') and key != 27 and cv.getWindowProperty(window.WINDOW_NAME, 0) >= 0:
    #     key = cv.waitKey(1)
    # cv.destroyAllWindows()

    # db.conn.commit()
    db.conn.close()


if __name__ == '__main__':
    main()
