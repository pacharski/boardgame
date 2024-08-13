# organization is package/module/submodule
import setup

from copy import deepcopy

class Point():
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    @property
    def xy(self):
        return (self.x, self.y)
    
    def deep_copy(self):
        return deepcopy(self)
    
    def __str__(self):
        form = "Point: ({x}, {y})"
        return form.format(x=self.x, y=self.y)
    
    def __eq__(self, point):
        return ((point != None)
            and (self.x == point.x) 
            and (self.y == point.y))
    
    def json_encode(self):
        return {"__type__": "Point",
                "xy":       self.xy }
    
    def json_decode(json_dict):
        if "Point" in json_dict:
            xy = json_dict["Point"]
            return Point(x=int(xy[0]), y=int(xy[1]))
        if ("__type__" in json_dict) and (json_dict["__type__"] == "Point"):
            xy = json_dict["xy"]
            return Point(x=int(xy[0]), y=int(xy[1]))
        return json_dict
                         

import json        
if __name__ == "__main__":
    p1 = Point()
    p2 = Point(x=5)
    p3 = Point(y=4)
    p4 = Point(x=6, y=8)
    p5 = p4.deep_copy()
    p5.y = 12

    points = [p1, p2, p3, p4, p5]
    
    print(p1)
    print(p2)
    print(p3)
    print(p4)
    print(p5)
    print()
        