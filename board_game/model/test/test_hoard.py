import unittest
import json
import os

from model.jsoninator import Jsoninator
from model.hoard import Hoard, Treasure

class TreasureTestCase(unittest.TestCase):
    def test_treasure_construct(self):
        t1 = Treasure(level=4, value=200, ability=None, desc="Treasure1")
        self.assertEqual((t1.level, t1.value, t1.ability, t1.desc),
                         (4, 200, None, "Treasure1"),
                         "Treasure construct match all fields")   
        
    def test_treasure_json(self):
        t1 = Treasure(level=4, value=100, ability=None,   desc="Treasure1")
        t2 = Treasure(level=5, value=200, ability="Scry", desc="Viewer2")
        t3 = Treasure(level=6, value=300, ability=None,   desc="Treasure3")
        treasures = [t1, t2, t3]

        self.assertEqual((t1.level, t1.value, t1.ability, t1.desc),
                         (4, 100, None, "Treasure1"),
                         "Treasure1 construct match all fields")   
        self.assertEqual((t2.level, t2.value, t2.ability, t2.desc),
                         (5, 200, "Scry", "Viewer2"),
                         "Treasure2 construct match all fields")   
        self.assertEqual((t3.level, t3.value, t3.ability, t3.desc),
                         (6, 300, None, "Treasure3"),
                         "Treasure3 construct match all fields")   
        
        jsoninator = Jsoninator({"Treasure": Treasure})
        temp_str = json.dumps(treasures, default=jsoninator.default)
        treasures_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)
        
        self.assertEqual(len(treasures), 3,
                         "Length of list of treasures is 3")
        self.assertEqual(len(treasures), len(treasures_copy),
                         "Length of list of treasures match after json dumps/loads")
        
        for treasure, treasure_copy in zip(treasures, treasures_copy):
            self.assertEqual(treasure.level, treasure_copy.level,
                             "Treasure level match after json dumps/loads")
            self.assertEqual(treasure.value, treasure_copy.value,
                             "Treasure value match after json dumps/loads")
            self.assertEqual(treasure.ability, treasure_copy.ability,
                             "Treasure ability match after json dumps/loads")
            self.assertEqual(treasure.desc, treasure_copy.desc,
                             "Treasure desc match after json dumps/loads")

class HoardTestCase(unittest.TestCase):
    def setUp(self):
        here = os.path.abspath(__file__)
        self.csv_path = os.path.join(os.path.dirname(here), "../../../data/treasures.csv")
        self.json_path = os.path.join(os.path.dirname(here), "../../../data/treasures.json")
        
    def test_hoard_csv(self):
        hoard1 = Hoard(self.csv_path)
        self.assertEqual(len(hoard1), 80,
                         "Hoard1 (csv_path) has 80 treasures")
        hoard2 = Hoard()
        self.assertEqual(len(hoard2), 0,
                         "Hoard2 (default) has 0 treasures")
        hoard3 = Hoard.from_csv_path(self.csv_path)
        self.assertEqual(len(hoard3), 80,
                         "Hoard3 from_csv_path has 80 treasures")
        
    def test_hoard_json(self):
        hoard1 = Hoard(self.csv_path)
        hoard2 = Hoard()
        hoard3 = Hoard.from_csv_path(self.csv_path)
        hoards = (hoard1, hoard2, hoard3)

        jsoninator = Jsoninator({"Hoard": Hoard, "Treasure": Treasure})
        temp_str = json.dumps(hoards, default=jsoninator.default)
        hoards_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        # Write a json file
        # with open(self.json_path, 'w') as json_file:
        #     json.dump(hoard1, json_file, indent=2, sort_keys=True,
        #               default=jsoninator.default, ensure_ascii=True)
        
        self.assertEqual(len(hoards), len(hoards_copy),
                         "Length of list of hoards match after json dumps/loads")
        
        for hoard, hoard_copy in zip(hoards, hoards_copy):
            self.assertEqual(len(hoard), len(hoard_copy),
                             "Length of hoard match after json dumps/loads")
            for treasure, treasure_copy in zip(hoard, hoard_copy):
                self.assertEqual(treasure.level, treasure_copy.level,
                                 "Treasure level match after json dumps/loads")
                self.assertEqual(treasure.value, treasure_copy.value,
                                 "Treasure value match after json dumps/loads")
                self.assertEqual(treasure.ability, treasure_copy.ability,
                                 "Treasure ability match after json dumps/loads")
                self.assertEqual(treasure.desc, treasure_copy.desc,
                                 "Treasure desc match after json dumps/loads")
                