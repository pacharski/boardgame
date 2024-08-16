# organization is project/package/module/submodule
# dimport setup

from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

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
    

if __name__ == "__main__":
    print(Point())