#!/usr/bin/env python3

import cv2 as cv
import sys
import gtk
import math

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


def find_closest_road_to_address(db, start_address, finish_coords):
    min_distance = 999999
    closest_road = ()

    for road in db.select_road(start_address[0], start_address[1]):
        distance = math.sqrt((road[0] - finish_coords[0]) ** 2 + (road[1] - finish_coords[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_road = road

        distance = math.sqrt((road[2] - finish_coords[0]) ** 2 + (road[3] - finish_coords[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_road = road

    return closest_road


def find_closest_road(db, road, dest_coords):
    min_distance = 999999
    closest_road = ()

    for adjacent_road in db.select_adjasent_roads(*road):
        if adjacent_road[0] != road[0] and \
                adjacent_road[1] != road[1] and \
                adjacent_road[0] != road[2] and \
                adjacent_road[1] != road[3]:
            distance = math.sqrt((adjacent_road[0] - dest_coords[0]) ** 2 + (adjacent_road[1] - dest_coords[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_road = adjacent_road
        else:
            distance = math.sqrt((adjacent_road[2] - dest_coords[0]) ** 2 + (adjacent_road[3] - dest_coords[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_road = adjacent_road

    return closest_road


def calculate_route(db, loc_address, dest_address, loc_coords, dest_coords):
    roads = [find_closest_road_to_address(db, dest_address, loc_coords), find_closest_road_to_address(db, loc_address, dest_coords)]
    destination_reached = False
    last_road = 1

    while not destination_reached:
        current_road = find_closest_road(db, roads[last_road], dest_coords)
        destination_road = roads[0]

        if current_road[0] == destination_road[0] and current_road[1] == destination_road[1] \
                or current_road[2] == destination_road[0] and current_road[3] == destination_road[1] \
                or current_road[0] == destination_road[2] and current_road[1] == destination_road[3] \
                or current_road[2] == destination_road[2] and current_road[3] == destination_road[3]:
            destination_reached = True
        if len(roads) > 1000:
            destination_reached = True
        roads.append(current_road)
        last_road += 1

    return roads


def main():
    in_file = 'vilnius.png'
    img = cv.imread(in_file)

    loc_address = check_input(sys.argv[1])
    dest_address = check_input(sys.argv[2])

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
    #          ('Didlaukio', 59, None, 2195, 1042, 2161, 1007),
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

    loc_coord = db.select_address(loc_address[0], loc_address[1])
    dest_coord = db.select_address(dest_address[0], dest_address[1])

    window_width = gtk.gdk.screen_width()
    window_height = gtk.gdk.screen_height()

    window = MapWindow(img, int(window_width * 0.8), int(window_height * 0.8), loc_coord, dest_coord, "Route finder")

    roads = calculate_route(db, loc_address, dest_address, loc_coord, dest_coord)
    window.draw_road(roads)

    key = -1
    while key != ord('q') and key != 27 and cv.getWindowProperty(window.WINDOW_NAME, 0) >= 0:
        key = cv.waitKey(1)
    cv.destroyAllWindows()

    db.conn.close()


if __name__ == '__main__':
    main()
