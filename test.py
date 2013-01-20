from supercluster.reader import YamlReader

print "== Testing Constellation Definition  =="
yaml_path = "configs/cluster_config.yaml"
yr = YamlReader()
yr.load_config(open('configs/cluster_definitions/mid-tier.yaml').read())
yr.load_config(open('configs/cluster_definitions/small-tier.yaml').read())
yr.load_config(open('configs/cluster_definitions/enterprise-tier.yaml').read())
yr.make_supercluster(open(yaml_path).read())
print u"%s" % yr.supercluster
