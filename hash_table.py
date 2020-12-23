# this contains the class definitions for a custom Hash Map
class HashMap:
    # we will initialize an empty hash with an optional parameter to adjust the map size if needed
    # O(1)
    def __init__(self, map_size=40):
        self.map = []
        for i in range(map_size):
            self.map.append([])

    # this private method is only used to find what map container any key passed in should exist at
    # O(1)
    def _create_hash(self, key):
        map_container = int(key) % len(self.map)
        return map_container

    # this method will associate a key-value pair and place them at the correct location in the map
    # O(1)
    def insert_item(self, key, value):
        hash_value = self._create_hash(key)
        self.map[hash_value] = [key, value]

    # this method will find a key  value in the map and replace any member there with an empty space
    # O(1)
    def delete_item(self, key):
        hash_value = self._create_hash(key)
        self.map[hash_value] = []

    # This method takes in a variable number of args consisting of keys in the map
    # it will return a list of values associated with those keys
    # O(N)
    def get_value(self, *args):
        return_list = []
        for key in args:
            hash_value = self._create_hash(key)
            if self.map[hash_value] is None:
                return_list.append(None)
            else:
                return_list.append(self.map[hash_value][1])
        return return_list

    # this method will return a list consisting of all values for each possible map location.
    # O(N)
    def get_all_values(self):
        return [item[1] for item in self.map]

    # this method will return a list of all keys found in each possible location of the map
    # O(N)
    def get_keys(self):
        return [item[0] for item in self.map]

    # this method is a simple output helper for showing a maps contents in a human readable form.
    # O(1)
    def __str__(self):
        string_representation = ''
        for i in self.map:
            string_representation += str(i[0])
            string_representation += " : "
            string_representation += str(i[1])
            string_representation += "\n"
        return string_representation
