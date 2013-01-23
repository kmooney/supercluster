import os
import yaml
SECRETS_PATH = os.environ.get("SECRETS_PATH", '..')
path = os.path.join(SECRETS_PATH, "secrets.yaml")
secrets = yaml.load(open(path).read())
MYSQL_PASSWORD = secrets['mysql-password']
