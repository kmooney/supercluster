from supercluster.reader import YamlReader

yaml_path = "configs/cluster_definitions/enterprise-tier.yaml"
yr = YamlReader(open(yaml_path).read())
print yr.get_cluster()
print yr.get_cluster().elements
