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


def print_help():
    help_text = [{'command': '?', 'help': 'display help.'},
                 {'command': 'change location', 'help': 'enter location address to set it.'},
                 {'command': 'change destination', 'help': 'enter destination address to set it.'},
                 {'command': 'change location int', 'help': 'choose location from map (interactive).'},
                 {'command': 'change destination int', 'help': 'choose destination from map (interactive).'},
                 {'command': 'exit', 'help': 'exit the program'},
                 ]

    for one in help_text:
        print('\033[91m' + one['command'] + '\033[0m' + ' - ' + one['help'])


class Ui(object):
    def __init__(self, db, map_file, window, route):
        commands = ["exit",
                    "change location",
                    "change destination"
                    "change location int",
                    "change destination int",
                    "?",
                    ]

        self.db = db
        self.exit = False

        command = raw_input('Enter command: ')

        if command not in commands:
            print('Invalid command entered, type "?" to see all possible commands')

        if command == 'exit':
            self.exit = True
        elif command == 'change location':
            self.change_location(map_file, window, route)
        elif command == 'change destination':
            self.change_destination(map_file, window, route)
        elif command == '?':
            print_help()

    def change_location(self, map, window, route):
        input_location = raw_input('Input location address: ')
        location_address = check_input(input_location)
        location_coord = self.db.select_address(location_address[0], location_address[1])

        window.set_location(map, location_coord)
        route.set_location(location_address)

        window.draw_road(route.get_roads())

    def change_destination(self, map_img, window, route):
        input_destination = raw_input('Input destination address: ')
        destination_address = check_input(input_destination)
        destination_coord = self.db.select_address(destination_address[0], destination_address[1])

        window.set_destination(map_img, destination_coord)
        route.set_destination(destination_address)

        window.draw_road(route.get_roads())

    def get_exit(self):
        return self.exit
