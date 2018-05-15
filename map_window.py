#!/usr/bin/env python3

import cv2 as cv


class MapWindow(object):
    def __init__(self, img, window_width, window_height, location, destination, window_name='Window'):
        self.WINDOW_NAME = window_name
        self.window_width, self.window_height = window_width, window_height

        self.map_y = location[1] - self.window_height/2  # coordinates of top left corner of the map
        self.map_x = location[0] - self.window_width/2

        self.img = img
        self.img_height, self.img_width = img.shape[:2]

        self.loc_x, self.loc_y = location[0], location[1]
        self.dest_x, self.dest_y = destination[0], destination[1]

        self.mouse_moving = False
        self.mouse_lb_pressed = False
        self.mouse_rb_pressed = False
        self.x_before_move, self.y_before_move = 0, 0

        cv.namedWindow(self.WINDOW_NAME)
        cv.setMouseCallback(self.WINDOW_NAME, self.on_mouse)

        cv.circle(self.img, (self.loc_x, self.loc_y), 7, (0, 0, 255), -1)
        cv.circle(self.img, (self.dest_x, self.dest_y), 7, (255, 0, 0), -1)

        self.redraw_image()

    def on_mouse(self, event, x, y, flags, param):
        if 0 <= x < self.window_width and 0 <= y < self.window_height:
            if event == cv.EVENT_LBUTTONDOWN:
                self.mouse_lb_pressed = True
                self.mouse_moving = True
                self.x_before_move, self.y_before_move = x, y
                print(self.map_x + self.x_before_move, self.map_y + self.y_before_move)
            if event == cv.EVENT_RBUTTONDOWN:
                self.mouse_rb_pressed = True
                self.mouse_moving = True
                self.x_before_move, self.y_before_move = x, y
            elif event == cv.EVENT_MOUSEMOVE:
                if self.mouse_moving:
                    if self.mouse_lb_pressed:
                        self.map_x += int((self.x_before_move - x) / 5)
                        self.map_y += int((self.y_before_move - y) / 5)
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
            # elif event == cv.EVENT_RBUTTONUP:
            #     self.mouse_rb_pressed = False
            #     self.mouse_moving = False
        else:
            # self.mouse_rb_pressed = False
            self.mouse_lb_pressed = False
            self.mouse_moving = False

    def redraw_image(self):
        if self.map_x < 0:
            self.map_x = 0
        if self.map_y < 0:
            self.map_y = 0
        if self.map_x > self.img_width - self.window_width:
            self.map_x = self.img_width - self.window_width
        if self.map_y > self.img_height - self.window_height:
            self.map_y = self.img_height - self.window_height
        img_cropped = self.img[
                      self.map_y: self.map_y + self.window_height,
                      self.map_x: self.map_x + self.window_width]
        cv.imshow(self.WINDOW_NAME, img_cropped)

    def draw_road(self, roads):
        for road in roads:
            cv.line(self.img, (road[0], road[1]), (road[2], road[3]), (0, 0, 0), 10)
        self.redraw_image()

