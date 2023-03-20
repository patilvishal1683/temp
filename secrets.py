import yaml
import sys

yaml_to_dict = None
file_name = "./values.yaml"
with open(file_name, 'r') as file:
    # AWS File Converted into Dict
    yaml_to_dict = yaml.safe_load(file)

all_keycloak_secrets = []
keycloak_keys = yaml_to_dict.get('keycloak')
if keycloak_keys:
    for key in keycloak_keys:
        if type(keycloak_keys[key]) == dict:
            secret = keycloak_keys.get(key).get('clientSecret')
            if secret:
                all_keycloak_secrets.append(keycloak_keys.get(key).get('clientSecret'))

print(all_keycloak_secrets)
