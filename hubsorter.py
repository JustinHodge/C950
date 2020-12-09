import csvimporter
from trucks import Truck
import re


def separate_packages():
    # I think I want to separate by package_zip
    # how to deal with special instructions though?
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

    for package in unsorted_packages:
        if package.package_notes != '':
            if re.search("Can only be on truck", package.package_notes):
                truck_required = package.package_notes[-1]
                truck_dict[truck_required].add_package(package)
                unsorted_packages.remove(package)

            elif (re.search("Wrong address", package.package_notes)
                    or re.search("Delayed on flight", package.package_notes)):
                truck_3.add_package(package)
                unsorted_packages.remove(package)

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


# separate_packages()
