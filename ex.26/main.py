import json
class ToDictMixin(object):
    def to_dict(self):
        return self._traverse_dict(self.__dict__)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, ToDictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value

class BinaryTree(ToDictMixin):
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

def test_BinaryTree():
    tree = BinaryTree(10,
                      left=BinaryTree(7, right=BinaryTree(9)),
                      right=BinaryTree(13, left=BinaryTree(11)))
    print(tree.to_dict())

class JsonMixin(object):
    @classmethod
    def from_json(cls, data):
        kwargs = json.loads(data)
        return cls(**kwargs)

    def to_json(self):
        return json.dumps(self.to_dict())

class DatacenterRack(ToDictMixin, JsonMixin):
    def __init__(self, switch=None, machines=None):
        self.switch = Switch(**switch)
        self.machines = [Machine(**kwargs) for kwargs in machines]

class Switch(ToDictMixin, JsonMixin):
    def __init__(self, ports, speed):
        self.ports = ports
        self.speed = speed

class Machine(ToDictMixin, JsonMixin):
    def __init__(self, cores, ram, disk):
        self.cores = cores
        self.ram = ram
        self.disk = disk

def test_DatacenterRack():
    serialized = """{
        "switch":{"ports":5, "speed":1e9},
        "machines":[
            {"cores":8, "ram":32e9, "disk":5e12},
            {"cores":4, "ram":16e9, "disk":1e12},
            {"cores":2, "ram":4e9, "disk":500e9}
        ]
    }"""
    deserialized = DatacenterRack.from_json(serialized)
    roundtrip = deserialized.to_json()
    assert json.loads(serialized)==json.loads(roundtrip)
    print(roundtrip)

if __name__=='__main__':
    test_DatacenterRack()
