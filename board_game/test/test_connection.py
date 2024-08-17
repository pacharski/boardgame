import unittest

import os
import sys
import json

here = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(here, "../.."))
import board_game as bg


class ConnectionTestCase(unittest.TestCase):
    def setUp(self):
        c1 = bg.Connection()
        c1.name = "conneciton1"
        c1.origin=11
        c1.terminus=71
        c1.forward = c1.backward = bg.Connection.Type.cSecretDoor
        c2 = bg.Connection(name="connection2", origin=13, terminus=23)
        c2.forward = bg.Connection.Type.cDoor
        c3 = bg.Connection(name="connection3", origin=13, terminus=23)
        c3.backward = bg.Connection.Type.cImpasse
        self.connections = [c1, c2, c3]

    def test_connection_construct_default(self):
        c = bg.Connection()
        self.assertEqual((c.name, c.origin, c.terminus, c.forward, c.backward),
                         ("", None, None, bg.Connection.Type.cClear, bg.Connection.Type.cClear),
                        "Connectioin default constructor match")
        
    def test_connection_construct(self):
        c = bg.Connection("Stage Left", 13, 26, 
                          forward=bg.Connection.Type.cSecretDoor)
        self.assertEqual((c.name, c.origin, c.terminus, c.forward, c.backward),
                         ("Stage Left", 13, 26, 
                          bg.Connection.Type.cSecretDoor, 
                          bg.Connection.Type.cSecretDoor),
                         "Connection constructor match")
        
    def test_connection_json(self):
        jsoninator = bg.Jsoninator({"Connection": bg.Connection})
        temp_str = json.dumps(self.connections, default=jsoninator.default)
        connections_copy = json.loads(temp_str, object_hook=jsoninator.object_hook)

        self.assertEqual(len(self.connections), len(connections_copy),
                         "Number of connections match after json dumps/loads")
        for connection, connection_copy in zip(self.connections, connections_copy):
            self.assertEqual((connection.name, connection.origin, connection.terminus),
                             (connection_copy.name, connection_copy.origin, 
                              connection_copy.terminus),
                             "Connection name/origin/terminus match after json dumps/loads")
            self.assertEqual(connection.forward,
                             connection_copy.forward,
                             "Connection forward match after json dumps/loads")
            self.assertEqual(connection.backward,
                             connection_copy.backward,
                             "Connection backward match after json dumps/loads")