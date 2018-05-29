#!/usr/bin/env python3

import math


class Route(object):
    def __init__(self, max_distance, db):
        self.max_distance = max_distance
        self.db = db
        self.location_address = None
        self.destination_address = None
        self.roads = None

    def find_closest_road_to_address(self, start_address, finish_coords):
        min_distance = self.max_distance
        closest_road = ()

        for road in self.db.select_road(start_address[0], start_address[1]):
            distance = math.sqrt((road[0] - finish_coords[0]) ** 2 + (road[1] - finish_coords[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_road = road

            distance = math.sqrt((road[2] - finish_coords[0]) ** 2 + (road[3] - finish_coords[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_road = road

        return closest_road

    def find_closest_road_to_coordinates(self, coords):
        min_distance = self.max_distance
        closest_road = ()

        for road in self.db.select_roads():
            distance = math.sqrt((road[0] - coords[0]) ** 2 + (road[1] - coords[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_road = road

            distance = math.sqrt((road[2] - coords[0]) ** 2 + (road[3] - coords[1]) ** 2)
            if distance < min_distance:
                min_distance = distance
                closest_road = road

        return closest_road

    def find_closest_road(self, road, dest_coords):
        min_distance = self.max_distance
        closest_road = ()

        for adjacent_road in self.db.select_adjasent_roads(*road):
            if adjacent_road[0] != road[0] and \
                    adjacent_road[1] != road[1] and \
                    adjacent_road[0] != road[2] and \
                    adjacent_road[1] != road[3]:
                distance = math.sqrt(
                    (adjacent_road[0] - dest_coords[0]) ** 2 + (adjacent_road[1] - dest_coords[1]) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_road = adjacent_road
            else:
                distance = math.sqrt(
                    (adjacent_road[2] - dest_coords[0]) ** 2 + (adjacent_road[3] - dest_coords[1]) ** 2)
                if distance < min_distance:
                    min_distance = distance
                    closest_road = adjacent_road

        return closest_road

    def calculate_route(self, loc_address, dest_address, loc_coords, dest_coords):
        roads = [self.find_closest_road_to_address(dest_address, loc_coords),
                 self.find_closest_road_to_address(loc_address, dest_coords)]
        destination_reached = False
        last_road = 1

        while not destination_reached:
            current_road = self.find_closest_road(roads[last_road], dest_coords)
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

    def calculate_route_int(self, loc_coords, dest_coords):
        roads = [self.find_closest_road_to_coordinates(dest_coords),
                 self.find_closest_road_to_coordinates(loc_coords)]
        destination_reached = False
        last_road = 1

        while not destination_reached:
            try:
                current_road = self.find_closest_road(roads[last_road], dest_coords)
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
            except IndexError:
                destination_reached = True

        return roads

    def get_roads(self):
        self.roads = None
        location_coords = None
        destination_coords = None

        if self.location_address:
            location_coords = self.db.select_address(self.location_address[0], self.location_address[1])
        if self.destination_address:
            destination_coords = self.db.select_address(self.destination_address[0], self.destination_address[1])

        if self.location_address and self.destination_address and self.location_address != self.destination_address:
            self.roads = self.calculate_route(self.location_address, self.destination_address, location_coords,
                                              destination_coords)
        return self.roads

    def get_roads_int(self, location_coords, destination_coords):
        self.roads = None

        if location_coords and destination_coords and location_coords != destination_coords:
            self.roads = self.calculate_route_int(location_coords, destination_coords)

        return self.roads
