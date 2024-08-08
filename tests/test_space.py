import json 
from copy import deepcopy

from model import Space, Point


if __name__ == "__main__":
    class SpaceEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Space):
                return o.json_encode()
            return json.JSONEncoder.default(self, o)
        
    class SpaceDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if 'Space' in dct:
                return Space.json_decode(dct)
            return dct

    s1 = Space()
    s2 = Space(id=2, name="Crypt", center=Point(5, 6), level=4)
    s3 = Space(id=3, name="Queen's Crypt", center=Point(5, 6), level=4)
    s3.vertices = [Point(0, 0), Point(0, 5), Point(4, 5), Point(4, 0)]
    s4 = Space(name="Queen's Crypt", center=Point(5, 6), level=4,
               vertices = [Point(0, 0), Point(0, 5), Point(4, 5), Point(4, 0)])
    s4.add_vertex(Point(7,8))
    s5 = s4.deep_copy()
    s5.add_vertex(Point(11,12))
    
    print(s1)
    print(s2)
    print(s3)
    print(s4)
    print(s5)
    print()

    spaces = [s1, s2, s3, s4, s5]
    
    filename = "temp/space.json"
    with open(filename, 'w') as jsonfile:
        json.dump(spaces, jsonfile, cls=SpaceEncoder)
    with open(filename, 'r') as jsonfile:
        spaces_copy = json.load(jsonfile, cls=SpaceDecoder)
    assert len(spaces) == len(spaces_copy)
    for idx in range(len(spaces)):
        print("{} == {}".format(spaces[idx], spaces_copy[idx]))
        assert spaces[idx].name  == spaces_copy[idx].name
        assert spaces[idx].level == spaces_copy[idx].level

    print()
    for _ in range(10):
        s4.remove_last_vertex()
        print(s4)
