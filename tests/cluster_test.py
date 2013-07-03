from shapely.geometry import Point

from clusterit.cluster import cluster_features, Cluster
from clusterit.feature import Feature


def test_cluster():
    a = Feature(Point(0, 0))
    b = Feature(Point(1, 0))
    c = Feature(Point(2, 0))

    features = [a, b, c]

    clusters = cluster_features(features, 1.0)

    assert len(clusters) == 2
    assert len(clusters[0].features) == 2
    assert len(clusters[1].features) == 1
    for cluster in clusters:
        assert isinstance(cluster, Cluster)
