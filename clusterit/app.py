import json
import os

from flask import abort, request, Flask

from cluster import get_clusters


app = Flask(__name__)

app.config.from_object(os.environ.get('CLUSTERIT_SETTINGS_MODULE'))

app.extensions['clusterit'] = {
    'sql': {}
}


@app.route('/<string:id>')
def proxy(id):
    try:
        config = app.config['SERVICES'][id]
    except KeyError:
        abort(404)

    bbox = [float(p) for p in request.args.get(
        'bbox', '-180,-90,180,90').split(',')]
    resolution = float(request.args.get('resolution'))

    clusters = get_clusters(id, config, bbox, resolution)

    return (json.dumps({
        'type': 'FeatureCollection',
        'features': [c.geoJSON() for c in clusters]
    }), 200, {
        'Content-Type': 'application/json'
    })
