import hashlib
import json
import os
import time

import requests
from celery import shared_task

from .models import Character

MARVEL_API_BASE_URL = "https://gateway.marvel.com/v1/public"
MARVEL_API_PUBLIC_KEY = "230cd895321c59f504f1bb0737bcdd8d"
MARVEL_API_PRIVATE_KEY = "5818b6fece09beca7fbaac7dc54eee919a85b7f5"
CHARACTER_NAME = "spectrum"

def generate_marvel_auth_params():
    timestamp = str(int(time.time()))
    hash_str = f"{timestamp}{MARVEL_API_PRIVATE_KEY}{MARVEL_API_PUBLIC_KEY}"
    hash_md5 = hashlib.md5(hash_str.encode('utf-8')).hexdigest()

    return {
        "apikey": MARVEL_API_PUBLIC_KEY,
        "ts": timestamp,
        "hash": hash_md5,
    }


def get_marvel_character(name):
    params = generate_marvel_auth_params()
    query_params = {"name": name}
    params.update(query_params)

    url = f"{MARVEL_API_BASE_URL}/characters"
    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"get_marvel_character API returned a non-200 status code: {response.status_code}")

    json_response = response.json()["data"]["results"]

    data = json_response[0]

    return {
        "id": data["id"],
        "name": data["name"],
        "description": data["description"],
        "thumbnail": f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}",
    }


def get_marvel_character_by_id(character_id):
    params = generate_marvel_auth_params()

    url = f"{MARVEL_API_BASE_URL}/characters/{character_id}"

    response = requests.get(url, params=params)

    if response.status_code != 200:
        raise Exception(f"get_marvel_character_by_id API returned a non-200 status code: {response.status_code}")

    json_response = response.json()["data"]["results"]

    data = json_response[0]

    return {
        "id": data["id"],
        "name": data["name"],
        "description": data["description"],
        "thumbnail": f"{data['thumbnail']['path']}.{data['thumbnail']['extension']}",
    }


def get_marvel_characters_from_comics(character_id):

    params = generate_marvel_auth_params()
    url = f"{MARVEL_API_BASE_URL}/characters/{character_id}/comics"
    response = requests.get(url, params=params)

    json_response = response.json()["data"]["results"]

    data = json_response
    character_ids = set()

    for comic in data:
        for character in comic["characters"]["items"]:
            character_id = character["resourceURI"].split("/")[-1]
            character_ids.add(int(character_id))

    return character_ids


@shared_task
def create_spectrum_in_database():
    spectrum = get_marvel_character(CHARACTER_NAME)
    Character.objects.create(
        marvel_id=spectrum["id"],
        name=spectrum["name"],
        description=spectrum["description"],
        thumbnail=spectrum["thumbnail"],
    )
    return spectrum["id"]


@shared_task
def create_related_characters_in_database(spectrum_id):
    character_ids = get_marvel_characters_from_comics(spectrum_id)
    character_ids.remove(spectrum_id)

    for character_id in character_ids:
        character = get_marvel_character_by_id(character_id)
        Character.objects.create(
            marvel_id=character["id"],
            name=character["name"],
            description=character["description"],
            thumbnail=character["thumbnail"],
        )
