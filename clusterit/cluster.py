class Cluster(object):
    def __init__(self, feature, threshold):
        self.features = [feature]
        self.threshold = threshold

    def add(self, feature):
        if self.features[0].geometry.distance(feature.geometry) <= self.threshold:
            self.features.append(feature)
            return True
        return False


def cluster_features(features, threshold):
    clusters = []
    for feature in features:
        clustered = False
        for cluster in reversed(clusters):
            if cluster.add(feature):
                clustered = True
                break
        if not clustered:
            clusters.append(Cluster(feature, threshold))

    return clusters
