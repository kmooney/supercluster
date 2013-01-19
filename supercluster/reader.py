import yaml
from adapters import AWSAdapter
from model import Cluster


class Reader(object):

    def __init__(self, *args, **kwargs):
        adapter = kwargs.pop('adapter', AWSAdapter)
        self.adapter = adapter()
        self.cluster = None

    def get_cluster(self):
        return self.cluster

    def make_cluster(self, data):
        """
        Given a dictionary, this uses the cluster adapter to create
        cluster objects.
        """

        elements = data.pop('elements', list())
        self.cluster = Cluster(
            data=data,
            elements=[self.adapter.translate_element(x) for x in elements]
        )


class YamlReader(Reader):

    def __init__(self, document):
        """
        Expects an arg called 'document' that contains
        yaml-formatted string data.
        """
        super(YamlReader, self).__init__(document, **dict())
        self.make_cluster(yaml.load(document))
