import datetime

import hubsorter


def _run_to_time(end_time):
    time_part = datetime.time(8, 0, 0)
    date_part = datetime.date.today()
    time_now = datetime.datetime.combine(date_part, time_part)
    global truck1
    while len(truck1.ordered_cargo) > 0:
        time_now = truck1.drop_off_next_package(time_now)
        if time_now <= end_time:
            truck1.set_package_delivered(time_now)
        else:
            break
    truck1.drop_off_next_package(time_now)
    time_part = datetime.time(8, 0, 0)
    date_part = datetime.date.today()
    time_now = datetime.datetime.combine(date_part, time_part)
    while len(truck2.ordered_cargo) > 0:
        time_now = truck2.drop_off_next_package(time_now)
        if time_now <= end_time:
            truck2.set_package_delivered(time_now)
        else:
            break
    truck2.drop_off_next_package(time_now)
    while len(truck3.ordered_cargo) > 0:
        time_now = truck3.drop_off_next_package(time_now)
        if time_now <= end_time:
            truck3.set_package_delivered(time_now)
        else:
            break
    truck3.drop_off_next_package(time_now)


def all_truck_statuses(current_time):
    print(f"Current Time is: {current_time} ")
    print("\n*************\nStill To Be Delivered: ")
    print("*********\n|TRUCK 1|\n*********")
    for package in truck1.ordered_cargo:
        print(f"  {package.package_id}, ", end='')
    print("*********\n|TRUCK 2|\n*********")
    for package in truck2.ordered_cargo:
        print(f"  {package.package_id}, ", end='')
    print("*********\n|TRUCK 3|\n*********")
    for package in truck3.ordered_cargo:
        print(f"  {package.package_id}, ", end='')
    print("\n\n*************\nPreviously Delivered: ")
    print("*********\n|TRUCK 1|\n*********")
    for package in truck1.delivered_cargo:
        print(f"  {package.package_id} - Delivered at {package.time_delivered}")
    print(f"\nTotal distance Traveled: {truck1.total_distance_traveled}\n")
    print("*********\n|TRUCK 2|\n*********")
    for package in truck2.delivered_cargo:
        print(f"  {package.package_id} - Delivered at {package.time_delivered}")
    print(f"\nTotal distance Traveled: {truck2.total_distance_traveled}\n")
    print("*********\n|TRUCK 3|\n*********")
    for package in truck3.delivered_cargo:
        print(f"  {package.package_id} - Delivered at {package.time_delivered}")
    print(f"\nTotal distance Traveled: {truck3.total_distance_traveled}\n")

    print(f"************TOTAL DISTANCE ALL TRUCKS: "
          f"{truck1.total_distance_traveled + truck2.total_distance_traveled + truck3.total_distance_traveled}"
          f"************\n\n")


if __name__ == '__main__':
    truck1, truck2, truck3 = hubsorter.separate_packages()
    option = ''
    while option != "quit":
        option = (input("What would you like to do? Run [all] or check status at a certain [time] or [quit]?")
                  .lower()
                  .strip())
        if option == "all":
            time_part = datetime.time(23, 59, 0)
            date_part = datetime.date.today()
            time_to_check = datetime.datetime.combine(date_part, time_part)
            _run_to_time(time_to_check)
            all_truck_statuses(time_to_check)

        if option == "time":
            time_input = input("What time would you like to check? FORMAT HH:MM - 24Hour")
            hour = int(time_input.split(":")[0])
            minute = int(time_input.split(":")[1])
            time_part = datetime.time(hour, minute, 0)
            date_part = datetime.date.today()
            time_to_check = datetime.datetime.combine(date_part, time_part)
            _run_to_time(time_to_check)
            all_truck_statuses(time_to_check)






