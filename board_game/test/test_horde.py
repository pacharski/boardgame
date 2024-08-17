import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import board_game as bg


class CreatureTestCase(unittest.TestCase):
    def test_creature_construct(self):
        c1 = bg.Creature(level=4, defenses=(5, 6, 7, 8, 9, 10), ability=None, desc="Creature1")
        self.assertEqual((c1.level, c1.defenses, c1.ability, c1.desc),
                         (4, (5,6,7,8,9,10), None, "Creature1"),
                         "Creature construct match all fields")   
        
    def test_creature_json(self):
        c1 = bg.Creature(level=4, defenses=(5, 6, 7, 8, 9, 10), ability=None, desc="Creature1")
        c2 = bg.Creature(level=5, defenses=(4, 6, 5, 7, 8, 11), ability="Trap!", desc="Trap2")
        c3 = bg.Creature(level=6, defenses=(5, 6, 6, 6, 9, 10), ability=None, desc="Creature3")
        creatures = [c1, c2, c3]

        self.assertEqual((c1.level, c1.defenses, c1.ability, c1.desc),
                         (4, (5, 6, 7, 8, 9, 10), None, "Creature1"),
                         "Creature1 construct match all fields")   
        self.assertEqual((c2.level, c2.defenses, c2.ability, c2.desc),
                         (5, (4, 6, 5, 7, 8, 11), "Trap!", "Trap2"),
                         "Creature2 construct match all fields")   
        self.assertEqual((c3.level, c3.defenses, c3.ability, c3.desc),
                         (6, (5, 6, 6, 6, 9, 10), None, "Creature3"),
                         "Creature3 construct match all fields")   
        
        jsoninator = bg.Jsoninator({"Creature": bg.Creature})
        temp_str = json.dumps(creatures, default=jsoninator.default)
        creatures_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)
        
        self.assertEqual(len(creatures), 3,
                         "Length of list of creatures is 3")
        self.assertEqual(len(creatures), len(creatures_copy),
                         "Length of list of creatures match after json dumps/loads")
        
        for creature, creature_copy in zip(creatures, creatures_copy):
            self.assertEqual(creature.level, creature_copy.level,
                                "Creature level match after json dumps/loads")
            self.assertEqual(creature.defenses, creature_copy.defenses,
                                "Creature defenses match after json dumps/loads")
            self.assertEqual(creature.ability, creature_copy.ability,
                                "Creature ability match after json dumps/loads")
            self.assertEqual(creature.desc, creature_copy.desc,
                                "Creature desc match after json dumps/loads")

class HordeTestCase(unittest.TestCase):
    def setUp(self):
        here = os.path.dirname(os.path.abspath(__file__))
        self.csv_path = os.path.join(os.path.dirname(here), "../data/creatures.csv")
        
    def test_horde_csv(self):
        horde1 = bg.Horde(self.csv_path)
        self.assertEqual(len(horde1), 61,
                         "Horde1 (csv_path) has 61 creatures")
        horde2 = bg.Horde()
        self.assertEqual(len(horde2), 0,
                         "Horde2 (default) has 0 creatures")
        horde3 = bg.Horde.from_csv_path(self.csv_path)
        self.assertEqual(len(horde3), 61,
                         "Horde3 from_csv_path has 61 creatures")
        
    def test_horde_json(self):
        horde1 = bg.Horde(self.csv_path)
        horde2 = bg.Horde()
        horde3 = bg.Horde.from_csv_path(self.csv_path)
        hordes = (horde1, horde2, horde3)

        jsoninator = bg.Jsoninator({"Horde": bg.Horde, "Creature": bg.Creature})
        temp_str = json.dumps(hordes, default=jsoninator.default)
        hordes_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)
        
        self.assertEqual(len(hordes), len(hordes_copy),
                         "Length of list of hordes match after json dumps/loads")
        
        for horde, horde_copy in zip(hordes, hordes_copy):
            self.assertEqual(len(horde), len(horde_copy),
                             "Length of horde match after json dumps/loads")
            for creature, creature_copy in zip(horde, horde_copy):
                self.assertEqual(creature.level, creature_copy.level,
                                 "Creature level match after json dumps/loads")
                self.assertEqual(creature.defenses, creature_copy.defenses,
                                 "Creature defenses match after json dumps/loads")
                self.assertEqual(creature.ability, creature_copy.ability,
                                 "Creature ability match after json dumps/loads")
                self.assertEqual(creature.desc, creature_copy.desc,
                                 "Creature desc match after json dumps/loads")
                
