class Cluster(object):
    """
       Holds info about the cluster.
    """
    def __init__(self, *args, **kwargs):
        self.mydict = kwargs.pop('data', dict())
        self.elements = kwargs.pop('elements', list())


class ClusterElement(object):

    def __init__(self, *args, **kwargs):
        pass

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
