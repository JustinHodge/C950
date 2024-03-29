from enum import Enum


class WGUPSPackage:
    # O(1)
    def __init__(self, package_info_list):
        if len(package_info_list) >= 8:
            self.package_info_list = package_info_list[:8]
            self.package_id = package_info_list[0]
            self.package_address = package_info_list[1]
            self.package_city = package_info_list[2]
            self.package_state = package_info_list[3]
            self.package_zip = package_info_list[4]
            self.package_delivery_deadline = package_info_list[5]
            self.package_mass = package_info_list[6]
            self.package_notes = package_info_list[7]
            self.delivery_status = DeliveryStatus.HUB
            self.time_delivered = None

    # This method to Override the builtin dunder str method for objects of this type
    # This allows me to get a string representation of any package quickly and easily
    # O(1)
    def __str__(self):
        self.package_info_list.append(self.delivery_status.value)
        return str(self.package_info_list)

    # method to package up the destination out of it's components stored in the object as a string
    # O(1)
    def get_full_destination(self):
        return self.package_address + "(" + self.package_zip + ")"


# simple enum to track location of any package
class DeliveryStatus(Enum):
    HUB = "At Hub"
    SENT = "In Transit"
    ARRIVE = "Delivered to Location"
