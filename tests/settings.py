DEBUG = True

SERVICES = {
    'cities_sql': {
        'type':                 'sql',
        'host':                  None,
        'user':                  None,
        'database':             'clusterit',
        'table':                'pop_places',
        'geometryName':         'geom',
        'columns':              ['name'],

        'srs':                   4326,
        'threshold':             1,
        'use_centroid':          True,

        'include_features':      True,
        'aggregation':          'scalerank',
        'aggregation_split':     None,
        'aggregation_backref':  'id',
    }
}
