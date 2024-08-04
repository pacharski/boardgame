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
    

class Hoard():
    def __init__(self, filename):
        self.creatures = []
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
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
                    print("SkipCreature(value)", len(row), row)
                    count = 0
                for _ in range(count):
                    creature = Creature(level, defenses, ability, desc)
                    self.creatures.append(creature)

    def show(self):
        for creature in self.creatures:
            print(creature)
        print("Total", len(self.creatures))



if __name__ == '__main__':
    import os
    import csv

    here = os.path.abspath(__file__)
    creatures = os.path.join(os.path.dirname(here), "../data/creatures.csv")
    
    hoard = Hoard(creatures)
    hoard.show()