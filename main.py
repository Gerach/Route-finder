#!/usr/bin/env python3

import cv2 as cv
import gtk

from map_window import MapWindow
from database import Database
from route import Route
from ui import Ui


def main():
    in_file = 'vilnius.png'
    db = Database('data.sqlite')

    # db.create_tables()
    # addresses = [('Naugarduko', 24, 2400, 2870),
    #              ('Didlaukio', 47, 2210, 1020),
    #              ('Sauletekio', 6, 3492, 1124),
    #              ('Antakalnio', 17, 3130, 2114),
    #              ('Saltoniskiu', 29, 2068, 2130),
    #              ]
    # roads = [('Naugarduko', 24, None, 2374, 2862, 2424, 2832),
    #          ('Naugarduko', 24, None, 2424, 2832, 2433, 2879),
    #          ('Naugarduko', 24, None, 2433, 2879, 2379, 2891),
    #          ('Naugarduko', 24, None, 2379, 2891, 2374, 2862),
    #          ('Didlaukio', 47, None, 2195, 1042, 2161, 1007),
    #          ('Sauletekio', 6, None, 3504, 1134, 3487, 1159),
    #          ('Antakalnio', 17, None, 3161, 2121, 3143, 2142),
    #          (None, None, None, 2374, 2862, 2312, 2900),
    #          (None, None, None, 2312, 2900, 2278, 2737),
    #          (None, None, None, 2278, 2737, 2248, 2663),
    #          (None, None, None, 2248, 2663, 2241, 2629),
    #          (None, None, None, 2241, 2629, 2238, 2564),
    #          (None, None, None, 2238, 2564, 2286, 2491),
    #          (None, None, None, 2286, 2491, 2298, 2452),
    #          (None, None, None, 2298, 2452, 2313, 2406),
    #          (None, None, None, 2313, 2406, 2344, 2329),
    #          (None, None, None, 2344, 2329, 2286, 2266),
    #          (None, None, None, 2286, 2266, 2238, 2251),
    #          (None, None, None, 2238, 2251, 2219, 2248),
    #          (None, None, None, 2219, 2248, 2214, 2083),
    #          (None, None, None, 2214, 2083, 2118, 2075),
    #          (None, None, None, 2118, 2075, 2084, 2125),
    #          (None, None, None, 2374, 2862, 2356, 2776),
    #          (None, None, None, 2356, 2776, 2344, 2720),
    #          (None, None, None, 2344, 2720, 2330, 2652),
    #          (None, None, None, 2330, 2652, 2305, 2642),
    #          (None, None, None, 2305, 2642, 2248, 2663),
    #          (None, None, None, 2313, 2406, 2214, 2377),
    #          (None, None, None, 2214, 2377, 2240, 2276),
    #          (None, None, None, 2240, 2276, 2238, 2251),
    #          ('Saltoniskiu', 29, None, 2084, 2125, 2064, 2157),
    #         ]
    # db.insert_address(addresses)
    # db.insert_road(roads)

    window_width = gtk.gdk.screen_width()
    window_height = gtk.gdk.screen_height()

    window = MapWindow(in_file, int(window_width * 0.8), int(window_height * 0.8), "Route finder")
    route = Route(window.get_max_distance(), db)

    run_program = True
    while run_program and cv.getWindowProperty(window.WINDOW_NAME, 0) >= 0:
        cv.waitKey(1)
        ui = Ui(db, window, route)
        if ui.get_exit():
            run_program = False

    cv.destroyAllWindows()
    db.conn.close()


if __name__ == '__main__':
    main()
