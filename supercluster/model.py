from copy import deepcopy


class ImproperlyConfigured(Exception):
    pass


class Cluster(object):
    """
       Holds info about the cluster.
    """
    def __init__(self, *args, **kwargs):
        self.slug = kwargs.pop('slug')
        self.description = kwargs.pop('description')
        self.elements = kwargs.pop('elements', list())

    def reify(self, slug):
        """
            This will return a cluster with elements
            bound to the supercluster config,
            so client-specific clusters.
        """
        element_copy = deepcopy(self.elements)
        for el in element_copy:
            el.slug = "{client_slug}-{element_slug}".format(
                client_slug=slug,
                element_slug=el.slug
            )

        return Cluster(
            slug="{client_slug}-{cluster_slug}".format(
                client_slug=slug,
                cluster_slug=self.slug
            ),
            description=self.description,
            elements=element_copy
        )

    def __unicode__(self):
        elements_unicode = u""
        for element in self.elements:
            elements_unicode += element.__unicode__()
        return u"""
            Cluster: {name}
            Elements:
                {elements}
        """.format(name=self.slug, elements=elements_unicode)


class SuperCluster(object):
    """
        Contains all clusters and metainfo
    """

    def __init__(self, clusters, name, description):
        self.name = name
        self.description = description
        self.clusters = clusters

    def append(self, cluster):
        if not type(cluster) == Cluster:
            raise TypeError("superclusters contain clusters.")
        self.clusters.append(cluster)

    def __unicode__(self):
        subclusters = u""
        for cluster in self.clusters:
            subclusters += cluster.__unicode__()

        return u"""
            Supercluster: {name}
            {count} subclusters
                {subclusters}
        """.format(
            name=self.name,
            count=len(self.clusters),
            subclusters=subclusters
        )


class ClusterElement(object):

    def __init__(self, *args, **kwargs):
        self.slug = kwargs.pop('slug', None)
        if self.slug is None:
            raise ImproperlyConfigured("ClusterElement must have slug")

    def am_i(self):
        """
        This answers the question: Does this object exist in the cloud?
        """
        raise NotImplementedError("am_i must be implemented by subclasses!")

    def make_me(self):
        """
        This creates the clusterobject in the cloud.
        """
        raise NotImplementedError("make_me must be implemetned by subclasses!")

    def __unicode__(self):
        return u"""
                {type}: {slug}""".format(
            type=type(self).__name__,
            slug=self.slug)


class AWSClusterElement(ClusterElement):
    """
    Represents an AWS Cluster Element.  Should be extended with concrete
    element types.
    """

    def __init__(self, *args, **kwargs):
        super(AWSClusterElement, self).__init__(*args, **kwargs)


class AWSLoadBalancer(AWSClusterElement):
    """
    Represents and EC2 Load Balancer
    """

    def __init__(self, *args, **kwargs):
        super(AWSLoadBalancer, self).__init__(*args, **kwargs)


class AWSInstance(AWSClusterElement):
    """
    Represents an EC2 Instance
    """

    def am_i(self):
        pass

    def __init__(self, *args, **kwargs):
        super(AWSInstance, self).__init__(*args, **kwargs)


class AWSEBS(AWSClusterElement):
    """
    Represents an EBS Volume
    """

    def __init__(self, *args, **kwargs):
        super(AWSEBS, self).__init__(*args, **kwargs)


class AWSSecurityGroup(AWSClusterElement):
    """
    Represents a Security Group
    """

    def __init__(self, *args, **kwargs):
        super(AWSSecurityGroup, self).__init__(*args, **kwargs)


class AWSRDS(AWSClusterElement):
    """
    Represents an RDS
    """

    def __init__(self, *args, **kwargs):
        super(AWSRDS, self).__init__(*args, **kwargs)
