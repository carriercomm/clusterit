import copy
import importlib
import os

from geoalchemy2.shape import from_shape
from geoalchemy2.types import Geometry
from shapely.geometry import Point
from sqlalchemy import create_engine, Column, Integer, MetaData, String, Table


__features__ = []
settings_module = os.environ.get('CLUSTERIT_SETTINGS_MODULE', 'tests.settings')
config = importlib.import_module(settings_module).SERVICES.items()[0][1]


def setup():
    for x in range(-3, 4):
        for y in range(-3, 4):
            __features__.append({
                'geometry': Point([x, y]),
                'properties': {
                    'ident': '%+d - %+d' % (x, y)
                }
            })

    _save_postgis()


def teardown():
    _destroy_postgis()


def _get_postgis():
    user = ''
    if config.get('user'):
        user = config['user']
    if config.get('password'):
        user += ':' + config['password']
    if len(user) > 0:
        user += '@'

    connection_string = 'postgresql+psycopg2://%(user)s%(host)s/%(database)s' % {
        'user': user,
        'host': config['host'] if config['host'] else '',
        'database': config['database']
    }

    engine = create_engine(connection_string, echo=True)

    return engine


def _save_postgis():
    # Create Table
    engine = _get_postgis()
    table = Table(config['table'], MetaData(engine),
                  Column('id', Integer, primary_key=True),
                  Column(config['geometryName'], Geometry('POINT', srid=4326)),
                  Column('ident', String))
    table.create()

    # Insert features
    connection = engine.connect()
    for feature in __features__:
        values = copy.copy(feature['properties'])
        values[config['geometryName']] = from_shape(feature['geometry'], srid=4326)
        connection.execute(table.insert().values(values))


def _destroy_postgis():
    engine = _get_postgis()
    table = Table(
        config['table'],
        MetaData(engine),
        autoload=True)
    connection = engine.connect()
    table.drop()

