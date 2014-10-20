import copy
import importlib
import os
import unittest

from geoalchemy2.shape import from_shape
from geoalchemy2.types import Geometry
from shapely.geometry import Point
from sqlalchemy import create_engine, Column, Integer, MetaData, String, Table
from sqlalchemy.engine import Engine
from sqlalchemy.exc import OperationalError
from clusterit.app import app
from clusterit.sql import get_connection, get_features


class SqlTestCase(unittest.TestCase):
    def setUp(self):
        settings_module = os.environ.get('CLUSTERIT_SETTINGS_MODULE', 'tests.settings')
        self.config_id = list(importlib.import_module(settings_module).SERVICES.items())[0][0]
        self.config = list(importlib.import_module(settings_module).SERVICES.items())[0][1]

        features = []
        for x in range(-3, 4):
            for y in range(-3, 4):
                features.append({
                    'geometry': Point([x, y]),
                    'properties': {
                        'ident': '%+d - %+d' % (x, y)
                    }
                })

        engine = self._get_postgis()
        table = Table(self.config['table'], MetaData(engine),
                      Column('id', Integer, primary_key=True),
                      Column(self.config['geometryName'], Geometry('POINT', srid=4326)),
                      Column('ident', String))
        table.drop(checkfirst=True)
        table.create()

        # Insert features
        connection = engine.connect()
        for feature in features:
            values = copy.copy(feature['properties'])
            values[self.config['geometryName']] = from_shape(feature['geometry'], srid=4326)
            connection.execute(table.insert().values(values))


    def _get_postgis(self):
        user = ''
        if self.config.get('user'):
            user = self.config['user']
        if self.config.get('password'):
            user += ':' + self.config['password']
        if len(user) > 0:
            user += '@'

        connection_string = 'postgresql+psycopg2://%(user)s%(host)s/%(database)s' % {
            'user': user,
            'host': self.config['host'] if self.config['host'] else '',
            'database': self.config['database']
        }

        engine = create_engine(connection_string, echo=True)

        return engine


    def tearDown(self):
        drop = (
            True if os.environ.get('CLUSTERIT_TESTS_DONT_DROP', False) == '1'
            else False)
        if not drop:
            return

        engine = self._get_postgis()
        table = Table(
            self.config['table'],
            MetaData(engine),
            autoload=True)
        connection = engine.connect()
        table.drop()


    def test_connection(self):
        with app.test_request_context():
            connection = get_connection(self.config_id, self.config)
            assert isinstance(connection['engine'], Engine)
            assert isinstance(connection['metadata'], MetaData)
            assert isinstance(connection['table'], Table)

    def test_connection_exception(self):
        false_config = copy.deepcopy(self.config)
        false_config['host'] = 'this_host_does_not_exist_hopefully'
        with app.test_request_context():
            self.assertRaises(OperationalError,  get_connection, self.config_id, false_config)

    def test_multiple_connections(self):
        with app.test_request_context():
            connection_1 = get_connection(self.config_id, self.config)

            config_id_2 = 'written_in_a_train'
            config_2 = copy.deepcopy(self.config)
            connection_2 = get_connection(config_id_2, config_2)

            assert app.extensions['clusterit']['sql'][self.config_id] == connection_1
            assert app.extensions['clusterit']['sql'][config_id_2] == connection_2
            assert connection_1 != connection_2

    def test_get_features(self):
        with app.test_request_context():
            bbox = [-1.5, -1.5, 1.5, 1.5]
            features = get_features(self.config_id, self.config, bbox)
            assert len(features) == 9
