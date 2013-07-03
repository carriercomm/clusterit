import decimal

from flask import current_app
from geoalchemy2 import Geometry
from geoalchemy2.elements import WKTElement
from geoalchemy2.shape import to_shape
from shapely.geometry import box
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql.expression import func, select

from feature import Feature


def get_connection(id, config):
    connection = getattr(current_app.extensions['clusterit']['sql'], id, None)
    if not connection:
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

        current_app.logger.info('SQL connection: %s' % connection_string)

        engine = create_engine(connection_string, echo=current_app.config['DEBUG'])
        metadata = MetaData(engine)
        table = Table(config['table'], metadata, autoload=True)

        connection = {
            'engine': engine,
            'metadata': metadata,
            'table': table
        }

        current_app.extensions['clusterit']['sql'][id] = connection

    return connection


def get_features(id, config, bbox):
    connection = get_connection(id, config)

    srs = config.get('srs', 4326)
    bbox = WKTElement(box(*bbox).wkt, srs)

    column_names = config.get('columns', [])
    for c in ['aggregation', 'aggregation_backref']:
        if config.get(c) and config[c] not in column_names:
            column_names.append(config[c])
    columns = [getattr(connection['table'].c, c) for c in column_names]

    the_geom = getattr(connection['table'].c, config['geometryName'])
    if the_geom.type.srid != srs:
        the_geom = func.ST_Transform(the_geom, srs).label(the_geom.name)
    columns.append(the_geom)

    query = select(columns).where(func.ST_Centroid(the_geom).contained(bbox))

    features = []
    for row in connection['engine'].connect().execute(query):
        properties = {}
        for column in columns:
            k = column.name
            v = row[k]

            if k == config['geometryName']:
                geometry = to_shape(v)
                break
            elif isinstance(v, decimal.Decimal):
                v = float(v)

            properties[k] = v
        features.append(Feature(geometry, properties))

    return features
