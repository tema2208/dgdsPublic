from .metadata_template import template
from path import Path
import requests
import os
import json
from .defense import *


def upload_file_to_ipfs_from_django(file):
    # with Path(file).open("rb") as fp:
    file_binary = file.read()
    ipfs_url = "http://127.0.0.1:5001"
    endpoint = "/api/v0/add"
    response = requests.post(ipfs_url + endpoint, files={"file": file_binary})
    ipfs_hash = response.json()["Hash"]
    filename = str(file)
    file_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
    print(file_uri)
    return file_uri


def convert_game_file_to_metadata(file):
    game_file_uri = upload_file_to_ipfs_from_django(file)
    cipher = AESCipher("")
    encrypted_message = cipher.encrypt(game_file_uri)
    key = cipher.key
    return game_file_uri, encrypted_message, key


def upload_array_to_ipfs(array):
    uri_array = []
    for file in array:
        uri_array.append(upload_file_to_ipfs_from_django(file))
    return uri_array


def upload_json_to_ipfs(metadata_template):
    metadata_json = json.dumps(metadata_template)
    api_url = "http://127.0.0.1:5001/api/v0"
    files = {"file": ("metadata.json", metadata_json)}
    response = requests.post(f"{api_url}/add", files=files)
    ipfs_hash = response.json()["Hash"]
    return f"https://ipfs.io/ipfs/{ipfs_hash}?filename=metadata.json"


def create_metadata_json(poster, images):
    return upload_file_to_ipfs_from_django(poster), json.dumps(upload_array_to_ipfs(images))
