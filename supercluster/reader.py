import yaml
from adapters import AWSAdapter
from model import SuperCluster, Cluster


class Reader(object):

    def __init__(self, *args, **kwargs):
        adapter = kwargs.pop('adapter', AWSAdapter)
        self.adapter = adapter()
        self.supercluster = None
        self.configs = dict()

    def get_supercluster(self):
        return self.supercluster

    def load_config(self, data):
        """
        Loads the cluster config from python dictionary
        """

        elements = data.pop('elements', None)
        data['elements'] = [
            self.adapter.translate_element(x) for x in elements
        ]
        cluster = Cluster(**data)
        self.configs[cluster.slug] = cluster

    def make_supercluster(self, data):
        """
        Given a dictionary, this uses the cluster adapter to create
        cluster objects.
        """

        elements = data.pop('clusters', list())
        elements = [
            self.configs[cluster['type']].reify(cluster['slug'])
            for cluster in elements
        ]
        self.supercluster = SuperCluster(
            clusters=elements,
            name=data.get('name', 'Unknown'),
            description=data.get('name', 'Unknown')
        )


class YamlReader(Reader):

    def __init__(self):
        """
        Expects an arg called 'document' that contains
        yaml-formatted string data.
        """
        super(YamlReader, self).__init__()

    def make_supercluster(self, data):
        data = yaml.load(data)
        super(YamlReader, self).make_supercluster(data)

    def load_config(self, data):
        """
        Given a yaml document, loads a cluster config
        """
        data = yaml.load(data)
        super(YamlReader, self).load_config(data)
