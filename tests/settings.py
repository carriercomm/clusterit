import os

TRAVIS = True if os.environ.get('TRAVIS') == 'true' else False

DEBUG = True

SERVICES = {
    'test': {
        'type':                 'sql',
        'host':                  None,
        'user':                 'postgres' if TRAVIS else None,
        'database':             'test_clusterit',
        'table':                'test_points',
        'geometryName':         'geom',
        #'columns':              ['id'],

        #'srs':                   4326,
        #'threshold':             1,
        #'use_centroid':          True,

        #'include_features':      True,
        #'aggregation':          'scalerank',
        #'aggregation_split':     None,
        #'aggregation_backref':  'id',
    }
}

