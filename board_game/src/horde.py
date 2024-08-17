import os
import sys
import json
import csv

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import board_game as bg


class Creature():
    def __init__(self, level, defenses, ability, desc):
        self.level = level
        self.defenses = defenses
        self.ability = ability
        self.desc = desc
        
    def __str__(self):
        fmt = "L%d %s(%s) L%s F%s W%s S%s H%s E%s"
        return fmt % (self.level, self.desc, self.ability, 
                      str( self.defenses[0] ).ljust(2),
                      str( self.defenses[1] ).ljust(2),
                      str( self.defenses[2] ).ljust(2),
                      str( self.defenses[3] ).ljust(2),
                      str( self.defenses[4] ).ljust(2),
                      str( self.defenses[5] ).ljust(2))
    
    def __mul__(self, n):
        return [self for _ in range(n)]
    
    def json_encode(self):
        return {"__type__": "Creature",
                "level":    self.level,
                "defenses": self.defenses,
                "ability":  self.ability,
                "desc":     self.desc}
                
    # Note: this is a class function, suitable to use for json load object_hook
    def json_decode(json_dict):
        local_dict = (json_dict["Creature"] if "Creature" in json_dict else
                      json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Creature")) else
                      None)
        if local_dict != None:
            level       = local_dict["level"]
            defenses    = tuple(local_dict["defenses"])
            ability     = local_dict["ability"]
            desc        = local_dict["desc"]
            return Creature(level, defenses, ability, desc)
        return json_dict

    
class Horde():
    # the default value is used for ALL instances, so default creatures to None and
    #  assign to empty list inside __init__ if None
    def __init__(self, csv_path=None, name=None, creatures=None):
        self.name = name if name != None else ""
        self.creatures = creatures if creatures != None else []
        if csv_path != None:
            self.load_from_csv_path(csv_path)

    def load_from_csv_path(self, csv_path):
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
            for row in reader:
                if len(row) != 10:
                    print("SkipCreature(#)", len(row), row)
                    count = 0
                level, count, h, f, w, s, h, e, ability, desc = row
                try:
                    level = int(level)
                    count = int(count)
                    defenses = (h.strip(), f.strip(), w.strip(),
                                s.strip(), h.strip(), e.strip())
                    ability = ability.strip()
                    desc = desc.strip()
                except:
                    # print("SkipCreature(value)", len(row), row)
                    count = 0
                for _ in range(count):
                    creature = Creature(level, defenses, ability, desc)
                    self.creatures.append(creature)

    def from_csv_path(csv_path):
        return Horde(csv_path)

    def __str__(self):
        form = "Horde: {} size={}"
        return form.format(self.name, len(self))
    
    def __len__(self):
        return len(self.creatures)
    
    def __iter__(self):
        for creature in self.creatures:
            yield creature

    def json_encode(self):
        return {"__type__": "Horde",
                "name":       self.name,
                "creatures":  self.creatures}
                
    # Note: this is a class function, suitable to use for json load object_hook
    def json_decode(json_dict):
        local_dict = (json_dict["Horde"] if "Horde" in json_dict else
                      json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Horde")) else
                      None)
        if local_dict != None:
            name      = local_dict["name"]
            creatures = local_dict["creatures"]
            return Horde(name=name, creatures=creatures)
        return json_dict 