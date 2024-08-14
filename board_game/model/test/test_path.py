import unittest
import json

from model.jsoninator import Jsoninator
from model.path import Path

class PathTestCase(unittest.TestCase):
    def setUp(self):
        p1 = Path()
        p1.name = "path1"
        p1.origin=11
        p1.terminus=71
        p1.forward = p1.backward = Path.Type.cSecretDoor
        p2 = Path(name="path2", origin=13, terminus=23)
        p2.forward = Path.Type.cDoor
        p3 = Path(name="path3", origin=13, terminus=23)
        p3.backward = Path.Type.cImpasse
        self.paths = [p1, p2, p3]

    def test_path_construct_default(self):
        p = Path()
        self.assertEqual((p.name, p.origin, p.terminus, p.forward, p.backward),
                         ("", None, None, Path.Type.cClear, Path.Type.cClear),
                         "Path default constructor match")
        
    def test_path_construct(self):
        p = Path("Stage Left", 13, 26, forward=Path.Type.cSecretDoor)
        self.assertEqual((p.name, p.origin, p.terminus, p.forward, p.backward),
                         ("Stage Left", 13, 26, Path.Type.cSecretDoor, Path.Type.cSecretDoor),
                         "Path constructor match")
        
    def test_path_json(self):
        jsoninator = Jsoninator({"Path": Path})
        temp_str = json.dumps(self.paths, default=jsoninator.default)
        paths_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        self.assertEqual(len(self.paths), len(paths_copy),
                         "Number of paths match after json dumps/loads")
        for path, path_copy in zip(self.paths, paths_copy):
            self.assertEqual((path.name, path.origin, path.terminus),
                             (path_copy.name, path_copy.origin, path_copy.terminus),
                             "Path name/origin/terminus match after json dumps/loads")
            self.assertEqual(path.forward,
                             path_copy.forward,
                             "Path forward match after json dumps/loads")
            self.assertEqual(path.backward,
                             path_copy.backward,
                             "Path backward match after json dumps/loads")