import csv


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
    

class Horde():
    def __init__(self, csv_path=None):
        self.creatures = []
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
        form = "Horde: size={}"
        return form.format(len(self))
    
    def __len__(self):
        return len(self.creatures)
    
    def __iter__(self):
        for creature in self.creatures:
            yield creature


if __name__ == '__main__':
    import os
    
    here = os.path.abspath(__file__)
    csv_path = os.path.join(os.path.dirname(here), "../../data/creatures.csv")
    horde1 = Horde(csv_path)
    horde2 = Horde.from_csv_path(csv_path)
    assert len(horde1) == len(horde2)
    assert len(horde1) == 61

    # for creature in horde1:
    #     print(creature)