#!/usr/bin/env python3

import sys


def check_input(value):
    address = value.rsplit(' ', 1)
    if len(address) != 2:
        print('Invalid address format provided.')
        sys.exit(1)
    elif address[0] is '' or address[1] is '':
        print('Invalid address format provided.')
        sys.exit(1)
    return address


class Ui(object):
    def __init__(self, db, map, window, route):
        self.db = db
        self.exit = False

        command = raw_input('Enter command: ')

        if command == 'exit':
            self.exit = True
        if command == 'change location':
            self.change_location(map, window, route)
        elif command == 'change destination':
            self.change_destination(map, window, route)

    def change_location(self, map, window, route):
        input_location = raw_input('Input location address: ')
        location_address = check_input(input_location)
        location_coord = self.db.select_address(location_address[0], location_address[1])

        window.set_location(map, location_coord)
        route.set_location(location_address)

        window.draw_road(route.get_roads())

    def change_destination(self, map, window, route):
        input_destination = raw_input('Input destination address: ')
        destination_address = check_input(input_destination)
        destination_coord = self.db.select_address(destination_address[0], destination_address[1])

        window.set_destination(map, destination_coord)
        route.set_destination(destination_address)

        window.draw_road(route.get_roads())

    def get_exit(self):
        return self.exit
