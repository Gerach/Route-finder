#!/usr/bin/env python3

import cv2 as cv


class MapWindow(object):
    def __init__(self, img, window_name='Window'):
        self.WINDOW_NAME = window_name
        self.img = img
        self.img_height, self.img_width = img.shape[:2]
        self.map_y, self.map_x = 1000, 1000  # coordinates of top left corner of the map
        self.window_width, self.window_height = 1000, 700
        self.mouse_moving = False
        self.mouse_lb_pressed = False
        self.mouse_rb_pressed = False
        self.x_before_move, self.y_before_move = 0, 0

        cv.namedWindow(self.WINDOW_NAME)
        cv.setMouseCallback(self.WINDOW_NAME, self.on_mouse)

        self.redraw_image()

    def on_mouse(self, event, x, y, flags, param):
        if 0 <= x < self.window_width and 0 <= y < self.window_height:
            if event == cv.EVENT_LBUTTONDOWN:
                self.mouse_lb_pressed = True
                self.mouse_moving = True
                self.x_before_move, self.y_before_move = x, y
            if event == cv.EVENT_RBUTTONDOWN:
                self.mouse_rb_pressed = True
                self.mouse_moving = True
                self.x_before_move, self.y_before_move = x, y
            elif event == cv.EVENT_MOUSEMOVE:
                if self.mouse_moving:
                    if self.mouse_lb_pressed:
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

                        self.redraw_image()
                    # elif self.mouse_rb_pressed:
                    #     multiplier = 0.0001 * abs(y-self.y_before_move)
                    #     self.img = cv.resize(self.img, None, fx=1+multiplier, fy=1+multiplier, interpolation=cv.INTER_CUBIC)
                    #
                    #     self.redraw_image()
                    #
                    #     print(y, self.y_before_move, y-self.y_before_move)
            elif event == cv.EVENT_LBUTTONUP:
                self.mouse_lb_pressed = False
                self.mouse_moving = False
            elif event == cv.EVENT_RBUTTONUP:
                self.mouse_rb_pressed = False
                self.mouse_moving = False
        else:
            self.mouse_rb_pressed = False
            self.mouse_lb_pressed = False
            self.mouse_moving = False

    def redraw_image(self):
        img_cropped = self.img[
                      self.map_y: self.map_y + self.window_height,
                      self.map_x: self.map_x + self.window_width]
        cv.imshow(self.WINDOW_NAME, img_cropped)
