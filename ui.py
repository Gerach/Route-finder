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
    def __init__(self, db, window, route):
        commands = ["exit",
                    "change location",
                    "change destination",
                    "change location int",
                    "change destination int",
                    "?",
                    ""
                    ]

        self.db = db
        self.exit = False

        if window.loc_x and window.dest_x and not route.location_address and not route.destination_address:
            window.draw_road(route.get_roads_int([window.loc_x, window.loc_y], [window.dest_x, window.dest_y]))

        command = raw_input('Enter command: ')

        if command not in commands:
            print('Invalid command entered, type "?" to see all possible commands')

        if command == 'exit':
            self.exit = True
        elif command == 'change location':
            self.change_location(window, route)
        elif command == 'change destination':
            self.change_destination(window, route)
        elif command == '?':
            print_help()
        elif command == 'change location int':
            self.change_location_int(window)
        elif command == 'change destination int':
            self.change_destination_int(window)

    def check_address(self, direction):
        input_address = raw_input('Input {} address: '.format(direction))
        location_coord = None
        address_exists = False

        while not address_exists:
            if input_address != 'exit':
                if not check_input(input_address):
                    print('Invalid address format provided. Correct format : <Street name> <House nr.>')
                    input_address = raw_input('Input {} address: '.format(direction))
                else:
                    location_coord = self.db.select_address(input_address.rsplit(' ', 1)[0],
                                                            input_address.rsplit(' ', 1)[1])
                    if not location_coord:
                        input_address = raw_input('Address not found, try another one: ')
                    else:
                        address_exists = True
            else:
                return

        return input_address.rsplit(' ', 1), location_coord

    def change_location(self, window, route):
        try:
            location_address, location_coord = self.check_address('location')
            window.set_location(location_coord)
            route.location_address = location_address

            window.draw_road(route.get_roads())
        except TypeError:
            return

    def change_destination(self, window, route):
        try:
            destination_address, destination_coord = self.check_address('destination')
            window.set_destination(destination_coord)
            route.destination_address = destination_address

            window.draw_road(route.get_roads())
        except TypeError:
            return

    @staticmethod
    def change_location_int(window):
        print('Please select location from map, use right mouse click to choose a place.')
        window.set_location_mouse()

    @staticmethod
    def change_destination_int(window):
        print('Please select destination from map, use right mouse click to choose a place.')
        window.set_destination_mouse()

    def get_exit(self):
        return self.exit
