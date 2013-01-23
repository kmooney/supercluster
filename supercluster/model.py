from copy import deepcopy
import boto
from exceptions import LoadBalanceException, InstanceException, RDSException
from . import MYSQL_PASSWORD


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
                element_slug=el.slug,
                cluster=self
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
        self.type = kwargs.pop('type', None)
        self.slug = kwargs.pop('slug', None)
        self.cluster = kwargs.pop('cluster', None)
        self.attributes = kwargs
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
    Represents and EC2 Load Balancer.
    """

    def am_i(self):
        """
            Looks for a load balancer that has the following kvps:
                1) cluster = self.cluster.name
                2) slug = self.slug
            If it can be found, returns True
            Otherwise false.
        """
        lbs = self.connection.get_all_load_balancers([self.slug])
        if len(lbs) > 1:
            raise LoadBalanceException(
                "Too many ELBs with slug: {slug}".format(slug=self.slug)
            )
        else:
            return len(lbs) == 1

    def make_me(self):
        if self.am_i() is False:
            # TODO Needs security groups
            self.connection.create_load_balancer(
                self.slug,
                self.zones,
                self.listeners
            )
        # TODO - Create & Register Instances

    def __init__(self, *args, **kwargs):
        self.zones = kwargs.pop('zones', list())
        # TODO - Process listeners
        self.listeners = kwargs.pop(
            'listeners',
            [(80, 8000, "HTTP", ), ]
        )
        if len(self.zones) == 0:
            raise LoadBalanceException("Load Balancer must have zones!")
        self.connection = boto.connect_elb()
        super(AWSLoadBalancer, self).__init__(*args, **kwargs)


class AWSInstance(AWSClusterElement):
    """
    Represents an EC2 Instance
    """

    def am_i(self):
        filters = dict(('tag:slug', self.slug))
        instances = self.connection.get_all_instances(filters=filters)
        if len(instances) > 1:
            raise InstanceException(
                "Too many instances with slug {slug}".format(slug=self.slug)
            )
        else:
            return len(instances) == 1

    def make_me(self):
        if not self.am_i():
            # TODO Need security groups!
            # TODO Need ssh key for cluster
            reservation = self.connection.run_instances(self.ami)
            instance = reservation[0]
            self.connection.create_tags(
                instance.id,
                dict(('slug', self.slug, ))
            )

    def __init__(self, *args, **kwargs):
        self.connection = boto.connect_ec2()
        self.ami = kwargs.pop('ami', None)
        self.size = kwargs.pop('size', None)
        if self.size is None:
            raise InstanceException("Instance requires size")
        if self.ami is None:
            raise InstanceException("Instance requires AMI")
        super(AWSInstance, self).__init__(*args, **kwargs)


class AWSRDS(AWSClusterElement):
    """
    Represents an EBS Volume
    """

    def am_i(self):
        instances = self.connection.get_all_dbinstances(instance_id=self.slug)
        if len(instances) > 1:
            raise RDSException("Too many RDSs with this slug!")
        else:
            return len(instances) == 1

    def make_me(self):
        if not self.am_i():
            self.connection.create_dbinstance(
                self.slug,
                self.storage,
                self.size,
                self.username,
                self.password,
            )
        pass

    def __init__(self, *args, **kwargs):
        self.connection = boto.rds.RDSConnection()
        self.storage = kwargs.get('storage', None)
        if self.storage is None:
            raise RDSException("storage must be set")
        self.size = kwargs.get('size', None)
        if self.size is None:
            raise RDSException("size must be set")
        self.username = kwargs.get('username', 'mysql')
        #TODO - Figure out how to make the db password
        #       work per cluster or maybe per rds per
        #       cluster.  Do not force it into the
        #       cluster definition file!
        self.password = kwargs.get('password', MYSQL_PASSWORD)
        super(AWSRDS, self).__init__(*args, **kwargs)


class AWSSecurityGroup(AWSClusterElement):
    """
    Represents a Security Group
    """

    def __init__(self, *args, **kwargs):
        super(AWSSecurityGroup, self).__init__(*args, **kwargs)
