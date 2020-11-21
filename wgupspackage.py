from enum import Enum


class WGUPSPackage:
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

    def __str__(self):
        self.package_info_list.append(self.delivery_status.value)
        return str(self.package_info_list)

    def get_full_destination(self):
        return self.package_address + "(" + self.package_zip + ")"


class DeliveryStatus(Enum):
    HUB = "At Hub"
    SENT = "In Transit"
    ARRIVE = "Delivered to Location"
