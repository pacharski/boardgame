import os
import sys

import csv


class Treasure():
    def __init__(self, level, value, ability, desc):
        self.level = level
        self.value = value
        self.ability = ability
        self.desc = desc
        
    def __str__(self):
        fmt = "L%d %s(%s) %5dgp"
        return fmt % (self.level, self.desc, self.ability, self.value)
    

class Hoard():
    def __init__(self, filename):
        self.treasures = []
        with open(filename, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if len(row) != 5:
                    print("SkipTreasure(#)", len(row), row)
                    count = 0
                level, count, value, ability, desc = row
                try:
                    level = int(level)
                    count = int(count)
                    value = int(value)
                    ability = ability.strip()
                    desc = desc.strip()
                except:
                    print("SkipTreasure(int)", len(row), row)
                    count = 0
                for _ in range(count):
                    treasure = Treasure(level, value, ability, desc)
                    self.treasures.append(treasure)

    def show(self):
        for treasure in self.treasures:
            print(treasure)
        print("Total", len(self.treasures))



if __name__ == '__main__':
    here = os.path.abspath(__file__)
    treasures = os.path.join(os.path.dirname(here), "../data/treasures.csv")
 
    hoard = Hoard(treasures)
    hoard.show()