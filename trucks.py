import datetime

import csvimporter

# this is a helper function to be used as the filter key for sorting in the plan_route method
def get_package_delivery_time(item):
    return item.package_delivery_deadline


class Truck:

    # here we create a nice empty truck object
    def __init__(self, cargo_list=None):
        self.distances, self.distance_keys = csvimporter.get_distances()
        self.unordered_cargo = cargo_list or []
        self.ordered_cargo = []
        self.delivered_cargo = []
        self.stop_distances = []
        self.total_distance_traveled = 0
        self.current_location = "4001 South 700 East(84107)"

    # very simple method to add a package to the end of what this truck is carrying
    def add_package(self, package):
        self.unordered_cargo.append(package)

    # this method is find what time the next package in the ordered list of packages would be delivered
    def drop_off_next_package(self, last_delivery_time):
        distance_traveled = self.stop_distances[0]
        # self.total_distance_traveled += distance_traveled
        time_passed = distance_traveled / 18.0
        this_delivery_time = last_delivery_time + datetime.timedelta(hours=time_passed)
        return this_delivery_time

    # this method will convert the next package in ordered_cargo to delivered status
    def set_package_delivered(self, this_delivery_time):
        if self.ordered_cargo:
            self.ordered_cargo[0].time_delivered = this_delivery_time
            self.delivered_cargo.append(self.ordered_cargo[0])
            self.ordered_cargo.remove(self.ordered_cargo[0])
            distance_traveled = self.stop_distances.pop()
            self.total_distance_traveled += distance_traveled

    # this method will take all packages assigned to this truck and order them in the most efficient delivery pattern
    def plan_route(self):
        early_delivery_packages = []
        # this will allow plan_route to be called safely to re-plan a route in case of package changes
        if not self.unordered_cargo:
            self.unordered_cargo = self.ordered_cargo.copy()
            self.ordered_cargo = []
            self.stop_distances = []
        # I used the greedy algorithm at this point to order the packages.
        next_stop = None
        ordered_stop_list = []
        ###############################################################################
        ###########ADD IN ORDERING FOR DELIVERY DEADLINE HERE##########################
        ###############################################################################
        # repeatedly cycle cargo removing the next shortest until all are sorted
        for package in self.unordered_cargo:
            if package.package_delivery_deadline != 'EOD':
                early_delivery_packages.append(package)
                self.unordered_cargo.remove(package)
                destination_key = self.distance_keys[package.get_full_destination()]
                current_location_key = self.distance_keys[self.current_location]
                distance = self.distances[current_location_key][destination_key]
                # this exists to flip the indexes since the table is incomplete
                if distance == '':
                    distance = self.distances[destination_key][current_location_key]
                self.stop_distances.append(float(distance))
        early_delivery_packages.sort(key=get_package_delivery_time)
        for package in early_delivery_packages:
            destination_key = self.distance_keys[package.get_full_destination()]
            current_location_key = self.distance_keys[self.current_location]
            distance = self.distances[current_location_key][destination_key]
            # this exists to flip the indexes since the table is incomplete
            if distance == '':
                distance = self.distances[destination_key][current_location_key]
            self.stop_distances.append(float(distance))
            ordered_stop_list.append(next_stop)
            self.ordered_cargo.append(package)
            self.current_location = package.get_full_destination()
        while len(self.unordered_cargo) > 0:
            shortest_distance = 100.0
            chosen_item = None
            # Cycle through remaining unordered cargo to find the next shortest stop
            for package in self.unordered_cargo:
                destination_key = self.distance_keys[package.get_full_destination()]
                current_location_key = self.distance_keys[self.current_location]
                distance = self.distances[current_location_key][destination_key]
                # this exists to flip the indexes since the table is incomplete
                if distance == '':
                    distance = self.distances[destination_key][current_location_key]
                # continually replace the shortest distance when a new one is found
                if float(distance) < shortest_distance:
                    shortest_distance = float(distance)
                    next_stop = package.get_full_destination()
                    chosen_item = package
            self.stop_distances.append(shortest_distance)
            ordered_stop_list.append(next_stop)
            self.unordered_cargo.remove(chosen_item)
            self.ordered_cargo.append(chosen_item)
            self.current_location = chosen_item.get_full_destination()
        for package in early_delivery_packages:
            pass
        self.ordered_cargo = early_delivery_packages + self.ordered_cargo
        destination = "4001 South 700 East(84107)"
        destination_key = self.distance_keys[destination]
        current_location_key = self.distance_keys[self.current_location]
        distance = self.distances[current_location_key][destination_key]
        if distance == '':
            distance = self.distances[destination_key][current_location_key]
        self.stop_distances.append(float(distance))
        self.current_location = destination


    def check_status(self):
        # returns a tuple of current location, current total travel distance, and the next stop
        return self.current_location, self.total_distance_traveled, self.ordered_cargo[0]
