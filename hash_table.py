class HashMap:
    def __init__(self, map_size=40):
        self.map = []
        for i in range(map_size):
            self.map.append([])

    def _create_hash(self, key):
        map_container = int(key) % len(self.map)
        return map_container

    def insert_item(self, key, value):
        hash_value = self._create_hash(key)
        self.map[hash_value] = [key, value]

    def delete_item(self, key):
        hash_value = self._create_hash(key)
        self.map[hash_value] = []

    def get_value(self, *args):
        return_list = []
        for key in args:
            hash_value = self._create_hash(key)
            if self.map[hash_value] is None:
                return_list.append(None)
            else:
                return_list.append(self.map[hash_value][1])
        return return_list

    def get_all_values(self):
        return [item[1] for item in self.map]

    def get_keys(self):
        return [item[0] for item in self.map]

    def __str__(self):
        string_representation = ''
        for i in self.map:
            string_representation += str(i[0])
            string_representation += " : "
            string_representation += str(i[1])
            string_representation += "\n"
        return string_representation
