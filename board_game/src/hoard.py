# organization is project/package/module/submodule
from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import csv
import json
import board_game as bg


class Treasure():
    def __init__(self, level, value, ability, desc):
        self.level = level
        self.value = value
        self.ability = ability
        self.desc = desc
        
    def __str__(self):
        fmt = "L%d %s(%s) %5dgp"
        return fmt % (self.level, self.desc, self.ability, self.value)
    
    def __mul__(self, n):
        return [self for _ in range(n)]
    
    def json_encode(self):
        return {"__type__": "Treasure",
                "level":    self.level,
                "value":    self.value,
                "ability":  self.ability,
                "desc":     self.desc}
                
    # Note: this is a class function, suitable to use for json load object_hook
    def json_decode(json_dict):
        local_dict = (json_dict["Treasure"] if "Treasure" in json_dict else
                      json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Treasure")) else
                      None)
        if local_dict != None:
            level       = local_dict["level"]
            value       = local_dict["value"]
            ability     = local_dict["ability"]
            desc        = local_dict["desc"]
            return Treasure(int(level), int(value), ability, desc)
        return json_dict
    

class Hoard():
    def __init__(self, csv_path=None, json_path=None, name=None, treasures=None):
        self.name = name if name != None else ""
        self.treasures = treasures if treasures != None else []
        if csv_path != None:
            self.load_from_csv_path(csv_path)
        elif json_path != None:
            self.load_from_json_path(json_path)

    def add(self, treasure):
        self.treasures.append(treasure)

    @property
    def value(self):
        return sum([treasure.value for treasure in self.treasures])
        
    def load_from_csv_path(self, csv_path):
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) != 5:
                    print("SkipTreasure(#)", len(row), row)
                    count = 0
                else:
                    level, count, value, ability, desc = row
                    try:
                        level = int(level)
                        count = int(count)
                        value = int(value)
                        ability = ability.strip()
                        desc = desc.strip()
                    except:
                        #print("SkipTreasure(int)", len(row), row)
                        count = 0
                for _ in range(count):
                    treasure = Treasure(level, value, ability, desc)
                    self.treasures.append(treasure)

    def from_csv_path(csv_path):
        return Hoard(csv_path)

    def __str__(self):
        form = "Hoard: size={}"
        return form.format(len(self))
    
    def __len__(self):
        return len(self.treasures)
    
    def __iter__(self):
        for treasure in self.treasures:
            yield treasure

    def json_encode(self):
        return {"__type__": "Hoard",
                "name":       self.name,
                "treasures":  self.treasures}
                
    # Note: this is a class function, suitable to use for json load object_hook
    def json_decode(json_dict):
        local_dict = (json_dict["Hoard"] if "Hoard" in json_dict else
                      json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Hoard")) else
                      None)
        if local_dict != None:
            name      = local_dict["name"]
            treasures = local_dict["treasures"]
            return Hoard(name=name, treasures=treasures)
        return json_dict
    
    def save_to_json_path(self, json_path=None):
        jsoninator = bg.Jsoninator({"Hoard": Hoard, "Treasure": Treasure})
        with open(json_path, 'w') as json_file:
            json.dump(self, json_file, indent=2, sort_keys=False,
                      default=jsoninator.default, ensure_ascii=True)
    
    def load_from_json_path(self, json_path):
        jsoninator = bg.Jsoninator({"Hoard": bg.Hoard, "Treasure": bg.Treasure})
        with open(json_path, newline='') as json_file:
            json_data = json.load(json_file, object_hook=jsoninator.object_hook)
            self.name = json_data.name
            self.treasures = json_data.treasures

    def from_json_path(json_path):
        return Hoard(json_path=json_path)
