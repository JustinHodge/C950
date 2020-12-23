import csvimporter
from trucks import Truck
import re


# this method simulates a sorting warehouse for the logistics. a place where all
# packages scheduled for this day can be put on the truck they are most efficient on
# to facilitate easier application of the greedy algorithm and allow accounting for special instructions
# as needed.
# O(N)
def separate_packages():
    # maximum of 16 packs per truck
    # package 9, Third District Juvenile Court, will be corrected at 10:20 a.m.
    #                           The correct address is 410 S State St., Salt Lake City, UT 84111

    unsorted_packages = csvimporter.get_packages().get_all_values()

    truck_1 = Truck()
    truck_2 = Truck()
    truck_3 = Truck()
    truck_dict = {
        '1': truck_1,
        '2': truck_2,
        '3': truck_3
    }
    list_of_joint_packages = []

    # This filters out packages with special instructions to deal with accordingly
    for package in unsorted_packages:
        if package.package_notes != '':
            # This catches all packages that are required to be sent on truck 2 and load them accordingly.
            if re.search("Can only be on truck", package.package_notes):
                truck_required = package.package_notes[-1]
                truck_dict[truck_required].add_package(package)
                unsorted_packages.remove(package)

            # This will fix the address on the known error in the original package list then push it onto truck 3
            elif re.search("Wrong address", package.package_notes):
                package.package_address = "410 S State St"
                package.package_city = "Salt Lake City"
                package.package_state = "UT"
                package.package_zip = "84111"
                truck_3.add_package(package)
                unsorted_packages.remove(package)

            # This will catch any packages that will not be available to load until later and push them on truck 3
            elif re.search("Delayed on flight", package.package_notes):
                truck_3.add_package(package)
                unsorted_packages.remove(package)

            # This will accumulate all packages that are required to be delivered simultaneously and assure they are
            # placed on a single truck
            elif re.search("Must be delivered with", package.package_notes):
                list_of_joint_packages.append(package)
                unsorted_packages.remove(package)

    for package in list_of_joint_packages:
        truck_1.add_package(package)
    while len(unsorted_packages) > 0 and len(truck_1.unordered_cargo) < 16:
        truck_1.add_package(unsorted_packages.pop())
    while len(unsorted_packages) > 0 and len(truck_2.unordered_cargo) < 16:
        truck_2.add_package(unsorted_packages.pop())
    while len(unsorted_packages) > 0 and len(truck_3.unordered_cargo) < 16:
        truck_3.add_package(unsorted_packages.pop())
    truck_1.plan_route()
    truck_2.plan_route()
    truck_3.plan_route()
    return truck_1, truck_2, truck_3
