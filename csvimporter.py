import csv

from hash_table import HashMap
from wgupspackage import WGUPSPackage

distance_table = "WGUPS Distance Table.csv"
package_table = "WGUPS Package File.csv"

# this method will open the csv file passed in and parse it returning a usable list format
def csv_import(file_name):
    csv_as_list = []
    with open(file_name, "r") as raw_CSV:
        iterable_CSV = csv.reader(raw_CSV)
        for i in iterable_CSV:
            csv_as_list.append(i)
        return csv_as_list

# this method creates an instance of the custom HashMap containing packages from the package_table
def get_packages():
    hash_table = HashMap(len(csv_import(package_table)))
    for i in csv_import(package_table):
        package = WGUPSPackage(i)
        hash_table.insert_item(int(package.package_id), package)
    return hash_table


def get_distances():
    # this returns a tuple. [0] is a 2 dimensional list of distances
    # [1] is a dictionary assigning each key(address) to it's index for use
    # in the 2 dimensional list
    lists_of_distances = []
    key_dict = {}
    raw_data = csv_import(distance_table)
    keys_list = []
    raw_data.pop(0)
    for line in raw_data:
        keys_list.append(line.pop(0))
        lists_of_distances.append(line)
    for key in keys_list:
        key_dict[key] = len(key_dict)
    return lists_of_distances, key_dict
