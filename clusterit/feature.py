from json import loads

from geojson.codec import dumps


class Feature(object):
    def __init__(self, geometry, properties={}):
        self.geometry = geometry
        self.properties = properties

    def geoJSON(self):

        return {
            'type': 'Feature',
            'geometry': loads(dumps(self.geometry)),
            'properties': self.properties
        }
