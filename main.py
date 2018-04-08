#!/usr/bin/env python3

import cv2


class MapWindow(object):
    def __init__(self, img, window_name = 'Window'):
        self.WINDOW_NAME = window_name
        self.img = img
        self.img_height, self.img_width, self.channels = img.shape
        self.map_y, self.map_x = 1000, 1000 # coordinates of top left corner of the map
        self.window_width, self.window_height = 1000, 700
        self.mouse_moving = False
        self.x_before_move, self.y_before_move = 0, 0

        cv2.namedWindow(self.WINDOW_NAME)
        cv2.setMouseCallback(self.WINDOW_NAME, self.onMouse)

        self.redrawImage()

    def onMouse(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_moving = True
            self.x_before_move, self.y_before_move = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.mouse_moving and x >= 0 and y >= 0 and x < self.window_width and y < self.window_height:
                self.map_x += int((self.x_before_move - x) / 5)
                self.map_y += int((self.y_before_move - y) / 5)

                if self.map_x < 0:
                    self.map_x = 0
                if self.map_y < 0:
                    self.map_y = 0
                if self.map_x > self.img_width - self.window_width:
                    self.map_x = self.img_width - self.window_width
                if self.map_y > self.img_height - self.window_height:
                    self.map_y = self.img_height - self.window_height

                self.redrawImage()

                print(x, y)
                print(self.x_before_move, self.y_before_move)
        elif event == cv2.EVENT_LBUTTONUP:
            self.mouse_moving = False

    def redrawImage(self):
        img_cropped = self.img[
                      self.map_y: self.map_y + self.window_height,
                      self.map_x: self.map_x + self.window_width]
        cv2.imshow(self.WINDOW_NAME, img_cropped)


def main():
    in_file = 'vilnius.png'
    map = cv2.imread(in_file)
    window = MapWindow(map, "Route finder")
    key = -1
    while key != ord('q') and key != 27 and cv2.getWindowProperty(window.WINDOW_NAME, 0) >= 0:
        key = cv2.waitKey(1)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
