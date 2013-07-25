from json import loads
import unittest

from geojson import GeoJSONEncoder
from shapely.geometry import Point

from clusterit.feature import Feature


class FeatureTestCase(unittest.TestCase):
    def test_init(self):
        f = Feature(Point(0.0, 0.0), {})
        assert isinstance(f, Feature)


    def test_geosjon(self):
        geometry = Point(0.0, 0.0)
        properties = {
            'a': 3
        }
        f = Feature(geometry, properties)

        json = f.geoJSON()

        gencoder = GeoJSONEncoder()

        assert loads(gencoder.encode(geometry)) == json['geometry']
        assert properties == json['properties']

