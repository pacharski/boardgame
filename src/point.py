class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def xy(self):
        return (self.x, self.y)
    
    def deep_copy(self):
        return Point(self.x, self.y)
    
    def __str__(self):
        form = "Point: ({x}, {y})"
        return form.format(x=self.x, y=self.y)
    
    def json_encode(self):
        return { "Point": self.xy }
    
    def json_decode(json_dict):
        if "Point" in json_dict:
            xy = json_dict["Point"]
            return Point(x=int(xy[0]), y=int(xy[1]))
                         

import json        
if __name__ == "__main__":
    class PointEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, Point):
                return o.json_encode()
            return json.JSONEncoder.default(self, o)
        
    class PointDecoder(json.JSONDecoder):
        def __init__(self, *args, **kwargs):
            json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        def object_hook(self, dct):
            if 'Point' in dct:
                return Point.json_decode(dct)
            return dct

    p1 = Point()
    p2 = Point(x=5)
    p3 = Point(y=4)
    p4 = Point(x=6, y=8)
    p5 = p4.deep_copy()

    points = [p1, p2, p3, p4, p5]
    
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    print(p5)
    print()

    filename = "temp/point.json"
    with open(filename, 'w') as jsonfile:
        json.dump(points, jsonfile, cls=PointEncoder)
    with open(filename, 'r') as jsonfile:
        points_copy = json.load(jsonfile, cls=PointDecoder)
    assert len(points) == len(points_copy)
    for idx in range(len(points)):
        print("{} == {}".format(points[idx], points_copy[idx]))
        assert points[idx].x == points_copy[idx].x
        assert points[idx].y == points_copy[idx].y
        