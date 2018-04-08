#!/usr/bin/env python3

import cv2 as cv

from map_window import MapWindow


def main():
    in_file = 'vilnius.png'
    img = cv.imread(in_file)
    window = MapWindow(img, "Route finder")
    key = -1
    while key != ord('q') and key != 27 and cv.getWindowProperty(window.WINDOW_NAME, 0) >= 0:
        key = cv.waitKey(1)
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()
