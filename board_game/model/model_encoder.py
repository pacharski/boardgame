# organization is package/module/submodule
import setup

import sys
import json
from json_encoder import CompactJSONEncoder


cModelEncodables = ("Point", "Path", "Exit", "Space", "Board",
                    "Card", "Deck", "Marker", "Player")

class ModelJSONEncoder(CompactJSONEncoder):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.encodables = cModelEncodables

    def default(self, o):
        if hasattr(o, "json_encode"):
            #if isinstance(o, ModelJSONEncoder.cEncodables):  
            return o.json_encode()
        return CompactJSONEncoder.default(self, o)
    
class ModelJSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)
        self.decodables = cModelEncodables
    
    def str_to_class(self, class_name):
        stuff = [mod for mod in globals() if "model" in mod]
        print(stuff)
        print()
        print(globals())   
        if ((class_name in globals())
        and isinstance(globals()[class_name], types.ClassType)):
            return globals()[class_name]
        return None
        # stuff = [mod for mod in sys.modules if "model" in mod]
        # print(stuff)   
        # for module in stuff: 
        #     # module_attr = sys.modules[__name__]
        #     if hasattr(module, class_name):
        #         class_type = getattr(module, class_name)
        #         return class_type
        # return None

    def import_string(dotted_path):
        """
        Import a dotted module path and return the attribute/class designated by the
        last name in the path. Raise ImportError if the import failed.
        """
        try:
            module_path, class_name = dotted_path.rsplit('.', 1)
        except ValueError:
            msg = "%s doesn't look like a module path" % dotted_path
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

        module = import_module(module_path)

        try:
            return getattr(module, class_name)
        except AttributeError:
            msg = 'Module "%s" does not define a "%s" attribute/class' % (
                module_path, class_name)
            six.reraise(ImportError, ImportError(msg), sys.exc_info()[2])

    def object_hook(self, json_dict):
        for class_name in self.decodables:
            if class_name in json_dict:
                class_type = self.str_to_class(class_name)
                if class_type != None:
                    return class_type.json_decode(json_dict)
        return json_dict