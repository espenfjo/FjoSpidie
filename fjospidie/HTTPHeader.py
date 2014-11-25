from pymongo.son_manipulator import SONManipulator

class HTTPHeader(object):
    def __init__(self, header):
        self.name = header.name
        self.value = header.value


class Transform(SONManipulator):
    """
    Transform the Report object into Mongo eatable dicts, and back
    """
    def transform_incoming(self, son, collection):
        """
        Convert a Report object into a Mongo/JSON object
        """
        if isinstance(son, dict):
            for (key, value) in son.items():
                print type(value)
                
                if isinstance(value, list):
                    for idx, foo in enumerate(value):
                        if isinstance(value, HTTPHeader):
                            print "OHAIFDS"
                            son[key] = value.__dict__
        return son
