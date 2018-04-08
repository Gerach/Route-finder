#!/usr/bin/env python3

import cv2

moving = False
map_x, map_y = 1000, 1000 # top left corner of the map
window_width, window_height = 1000, 700 # window resolution
ix, iy = 0, 0 # mouse coordinates before movement
img_width, img_height = 0, 0


def navigate_image(event, x, y, flags, param):
    global moving, map_x, map_y, ix, iy
    if event == cv2.EVENT_LBUTTONDOWN:
        moving = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if moving and x >= 0 and y >= 0 and x <window_width and y < window_height:
            map_x += int((ix - x)/5)
            map_y += int((iy - y)/5)

            if map_x < 0:
                map_x = 0
            if map_y < 0:
                map_y = 0
            if map_x > img_width - window_width:
                map_x = img_width - window_width
            if map_y > img_height - window_height:
                map_y = img_height - window_height

            print(x, y)
            print(ix, iy)
    elif event == cv2.EVENT_LBUTTONUP:
        moving = False


def main():
    img = cv2.imread('vilnius.png')
    global img_height, img_width, channels
    img_height, img_width, channels = img.shape
    cv2.namedWindow("Route finder")
    cv2.setMouseCallback("Route finder", navigate_image)

    while True:
        img_cropped = img[map_y: map_y + window_height, map_x: map_x + window_width]
        cv2.imshow('Route finder', img_cropped)
        key = cv2.waitKey(1) & 0xFF
        if key == 27:
            break

    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
