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
