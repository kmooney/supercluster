from model import AWSLoadBalancer, AWSEBS
from model import AWSRDS, AWSInstance, AWSSecurityGroup


class Adapter(object):

    def __init__(self, *args, **kwargs):
        pass

    def translate_element(self, element):
        raise NotImplementedError(
            "translate_element must be implemented by children"
        )


class AWSAdapter(Adapter):

    def __init__(self, *args, **kwargs):
        super(AWSAdapter, self).__init__(*args, **kwargs)
        self.mapping = dict()
        self._register_elements()

    def _register_elements(self):
        self.mapping['elb'] = AWSLoadBalancer
        self.mapping['security_group'] = AWSEBS
        self.mapping['instance'] = AWSInstance
        self.mapping['ebs'] = AWSSecurityGroup
        self.mapping['db'] = AWSRDS

    def translate_element(self, element):
        element_type = element.pop('type')
        # stick the aws parameters from the yaml
        # into the class.
        return self.mapping[element_type](**element)
