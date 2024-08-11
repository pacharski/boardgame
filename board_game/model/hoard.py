# organization is package/module/submodule
import setup

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
    
    def __mul__(self, n):
        return [self for _ in range(n)]
    

class Hoard():
    def __init__(self, csv_path):
        self.treasures = []
        if csv_path != None:
            self.load_from_csv_path(csv_path)

    def load_from_csv_path(self, csv_path):
        with open(csv_path, newline='') as csv_file:
            reader = csv.reader(csv_file)
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


if __name__ == '__main__':
    import os
    
    here = os.path.abspath(__file__)
    csv_path = os.path.join(os.path.dirname(here), "../../data/treasures.csv")
    hoard1 = Hoard(csv_path)
    hoard2 = Hoard.from_csv_path(csv_path)
    assert len(hoard1) == len(hoard2)
    assert len(hoard1) == 80
    
    for treasure in hoard1:
        print(treasure)