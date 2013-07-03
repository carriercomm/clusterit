from json import loads

from geojson import GeoJSONEncoder
from shapely.geometry import Point

from clusterit.feature import Feature


def test_init():
    f = Feature(Point(0.0, 0.0), {})
    assert isinstance(f, Feature)


def test_geosjon():
    geometry = Point(0.0, 0.0)
    properties = {
        'a': 3
    }
    f = Feature(geometry, properties)

    json = f.geoJSON()

    gencoder = GeoJSONEncoder()

    assert loads(gencoder.encode(geometry)) == json['geometry']
    assert properties == json['properties']
