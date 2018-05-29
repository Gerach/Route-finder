#!/usr/bin/env python3


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


def check_input(value):
    address = value.rsplit(' ', 1)
    if len(address) != 2:
        return
    return address


class Ui(object):
    def __init__(self, db, map_file, window, route):
        commands = ["exit",
                    "change location",
                    "change destination",
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

    def check_address(self, direction):
        input_location = raw_input('Input {} address: '.format(direction))
        location_coord = None
        address_exists = False

        while not address_exists:
            if not check_input(input_location):
                print('Invalid address format provided. Correct format : <Street name> <House nr.>')
                input_location = raw_input('Input {} address: '.format(direction))
            else:
                location_coord = self.db.select_address(input_location.rsplit(' ', 1)[0],
                                                        input_location.rsplit(' ', 1)[1])
                if not location_coord:
                    input_location = raw_input('Address not found, try another one: ')
                else:
                    address_exists = True

        return input_location, location_coord

    def change_location(self, map_file, window, route):
        location_address, location_coord = self.check_address('location')

        window.set_location(map_file, location_coord)
        route.set_location(location_address)

        window.draw_road(route.get_roads())

    def change_destination(self, map_img, window, route):
        destination_address, destination_coord = self.check_address('destination')

        window.set_destination(map_img, destination_coord)
        route.set_destination(destination_address)

        window.draw_road(route.get_roads())

    def get_exit(self):
        return self.exit
