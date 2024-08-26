from pathlib import Path
print('Running' if __name__ == '__main__' else
      'Importing', Path(__file__).resolve())

import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(here)))

import board_game as bg


class Card(bg.Card):
    def __init__(self, name, value, shortcut):
        super().__init__(name, value)
        self.shortcut = shortcut

    def __mul__(self, n):
        return [self for _ in range(n)]

    def __str__(self):
        form = "{} Shortcut={}"
        return form.format(super().__str__(), self.shortcut) 
                           
    def json_encode(self):
        return {**super().json_encode(),
                "shortcut": self.shortcut}

    # Note: this is a class function
    def json_decode(json_dict):
        card_dict = (json_dict if (("__type__" in json_dict) and (json_dict["__type__"] == "Card")) else
                     None)
        if card_dict != None:
            name      = card_dict["name"]
            value     = card_dict["value"]
            shortcut  = card_dict["shortcut"]
            return Card(name, value, shortcut=int(shortcut))
        return json_dict


if __name__ == "__main__":
    print(Card("Ogre", 3, 5))