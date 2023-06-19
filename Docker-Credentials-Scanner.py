#!/usr/bin/python3

import docker
import re
import base64
import json

# Define a regular expression to search for credential patterns
cred_regex = re.compile(r'(user|username|password|pass|\S+:\S+)\s*=\s*[\'"](\S+)[\'"]')

# Define a function to recursively search for credentials in a JSON or dictionary object
def search_for_credentials(obj):
    credentials = []
    if isinstance(obj, dict):
        for key, value in obj.items():
            if isinstance(value, (str, bytes)):
                matches = cred_regex.findall(str(value))
                for match in matches:
                    credentials.append((key, match[0], match[1]))
            elif isinstance(value, (list, tuple, dict)):
                credentials.extend(search_for_credentials(value))
    elif isinstance(obj, (list, tuple)):
        for value in obj:
            if isinstance(value, (str, bytes)):
                matches = cred_regex.findall(str(value))
                for match in matches:
                    credentials.append((None, match[0], match[1]))
            elif isinstance(value, (list, tuple, dict)):
                credentials.extend(search_for_credentials(value))
    return credentials

# Connect to the local Docker daemon
client = docker.from_env()

# Iterate over all images in the local Docker daemon
for image in client.images.list():
    # Get the image's configuration
    config = client.api.inspect_image(image.id)

    # Check for hardcoded credentials in the image's environment variables
    for env_var in config['Config']['Env']:
        matches = cred_regex.findall(env_var)
        for match in matches:
            key = match[0]
            credential = match[1]
            if credential.startswith('base64:'):
                credential = base64.b64decode(credential[len('base64:'):]).decode('utf-8')
                try:
                    credential_obj = json.loads(credential)
                    credentials = search_for_credentials(credential_obj)
                    for cred_key, cred_name, cred_value in credentials:
                        print(f"Found hardcoded credentials in image {image.id}: {cred_key} {cred_name}={cred_value}")
                except:
                    print(f"Error decoding JSON for image {image.id}")
    # Check for hardcoded credentials in the image's build args
    if 'Config' in config and 'Labels' in config['Config']:
        if 'build_args' in config['Config']['Labels']:
            build_args = json.loads(config['Config']['Labels']['build_args'])
            credentials = search_for_credentials(build_args)
            for cred_key, cred_name, cred_value in credentials:
                print(f"Found hardcoded credentials in image {image.id}: {cred_key} {cred_name}={cred_value}")

    # Check for hardcoded credentials in the image's command
    if 'Cmd' in config['Config']:
        cmd = ' '.join(config['Config']['Cmd'])
        matches = cred_regex.findall(cmd)
        for match in matches:
            key = match[0]
            credential = match[1]
            if credential.startswith('base64:'):
                credential = base64.b64decode(credential[len('base64:'):]).decode('utf-8')
                try:
                    credential_obj = json.loads(credential)
                    credentials = search_for_credentials(credential_obj)
                    for cred_key, cred_name, cred_value in credentials:
                        print(f"Found hardcoded credentials in image {image.id}: {cred_key} {cred_name}={cred_value}")
                except:
                    print(f"Error decoding JSON for image {image.id}")

    # Check for hardcoded credentials in the image's entrypoint
    if 'Entrypoint' in config['Config']:
            entrypoint = ' '.join(config['Config']['Entrypoint'])
            matches = cred_regex.findall(entrypoint)
            for match in matches:
                key = match[0]
                credential = match[1]
                if credential.startswith('base64:'):
                    credential = base64.b64decode(credential[len('base64:'):]).decode('utf-8')
                    try:
                        credential_obj = json.loads(credential)
                        credentials = search_for_credentials(credential_obj)
                        for cred_key, cred_name, cred_value in credentials:
                            print(f"Found hardcoded credentials in image {image.id}: {cred_key} {cred_name}={cred_value}")
                    except:
                        print(f"Error decoding JSON for image {image.id}")
