""" Script to download all photos from Schoology """

import json
import logging
import os
import random
import string
import time
from pathlib import Path

import requests
from dotenv import load_dotenv, find_dotenv

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv(find_dotenv(usecwd=True))
CONSUMER_KEY = os.environ.get("SCHOOLOGY_API_CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("SCHOOLOGY_API_CONSUMER_SECRET")

def load_config(config_file: Path = Path('.config.json')) -> dict:
    """ Load config from file """
    if config_file.exists():
        logging.info("Loading config from %s", config_file)
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        logging.info("Config file not found, initializing default config")
        config = {'users': []}
        save_config(config)
        return config

def save_config(config: dict, config_file: Path = Path('.config.json')) -> None:
    """ Save config to file """
    logging.info("Saving config file to %s", config_file)
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)


def generate_nonce(length=8) -> str:
    """Generate a random string of given length."""
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

def get_oauth_headers() -> dict:
    """ Generate OAuth headers for Schoology API """
    timestamp = str(int(time.time()))
    nonce = generate_nonce()
    headers = {
        'Authorization': f'OAuth realm="Schoology%20API",oauth_consumer_key="{CONSUMER_KEY}",oauth_signature_method="PLAINTEXT",oauth_timestamp="{timestamp}",oauth_nonce="{nonce}",oauth_version="1.0",oauth_signature="{CONSUMER_SECRET}&"'
    }
    return headers

def get_current_user_uid() -> str:
    """ Get current user UID """
    url = "https://api.schoology.com/v1/app-user-info"
    logging.info("Fetching user UID from: %s", url)
    response = requests.get(url, headers=get_oauth_headers(), timeout=5)
    return response.json()["api_uid"]

def get_user_name(user_id: str) -> str:
    """ Get current user name """
    url = f"https://api.schoology.com/v1/users/{user_id}"
    logging.info("Fetching user name from: %s", url)
    response = requests.get(url, headers=get_oauth_headers(), timeout=5)
    return response.json()["name_display"]

def get_children_uids(user_id: str) -> list[str]:
    """ Get current user children """
    url = f"https://api.schoology.com/v1/users/{user_id}"
    logging.info("Fetching user children from: %s", url)
    response = requests.get(url, headers=get_oauth_headers(), timeout=5)
    return response.json()["child_uids"].split(',')

def get_sections(user_id: str) -> list[dict]:
    """ Get current user sections """
    url = f"https://api.schoology.com/v1/users/{user_id}/sections"
    logging.info("Fetching user sections from: %s", url)
    response = requests.get(url, headers=get_oauth_headers(), timeout=5)
    return response.json()["section"]

def get_albums(section_id: str) -> list:
    """ Get current user albums """
    url = f"https://api.schoology.com/v1/sections/{section_id}/albums"
    logging.info("Fetching user albums from: %s", url)
    response = requests.get(url, headers=get_oauth_headers(), timeout=5)
    return response.json()["album"]

def get_album_contents(section_id: str, album_id: str) -> dict:
    """ Get current user album photos """
    url = f"https://api.schoology.com/v1/sections/{section_id}/albums/{album_id}?withcontent=1"
    logging.info("Fetching user album contents from: %s", url)
    response = requests.get(url, headers=get_oauth_headers(), timeout=5)
    return response.json()

def download_file(url: str, filename: str, download_to_path: Path) -> None:
    """ Download photo from URL """
    logging.info("Downloading photo from %s to %s", url, download_to_path/filename)
    response = requests.get(url, headers=get_oauth_headers(), timeout=5)
    with open(download_to_path/filename, 'wb') as f:
        f.write(response.content)


def main():
    """ Main function """
    config = load_config()

    user_id = get_current_user_uid()

    # Find user config
    user_info = next((user for user in config["users"] if user["id"] == user_id), None)

    if user_info is None:
        # If not found, create new config
        user_name = get_user_name(user_id)
        logging.info("User name: %s", user_name)
        user_info = {
            "id": user_id,
            "name": user_name,
            "downloaded_albums": [],
            "children": []
        }
        config["users"].append(user_info)

    children_info = user_info["children"]

    # Get children user IDs
    children_uids = get_children_uids(user_id)

    # Iterate over children
    for child_uid in children_uids:
        child_name = get_user_name(child_uid)
        logging.info("Child name: %s", child_name)
        child_info = {'id': child_uid, 'name': child_name, 'courses': []}

        # Get course sections for each child
        sections = get_sections(child_uid)

        # Iterate over sections
        for section in sections:
            course_title = section["course_title"]
            child_info["courses"].append({
                "id": section["id"],
                "title": course_title,
            })

            # Get albums for each course section
            albums = get_albums(section["id"])

            if len(albums) == 0:
                logging.warning("No albums found for child: %s in section %s", child_name, course_title)
                break

            # Iterate over albums
            for album in albums:
                # Check if album is already downloaded
                if album["id"] in [x["id"] for x in user_info["downloaded_albums"]]:
                    logging.info("Album %s already downloaded, skipping", album["title"])
                    continue

                # Create the local path for download
                local_path = Path("photos")/user_name/child_name/course_title/album["title"]
                local_path.mkdir(parents=True, exist_ok=True)

                # Iterate over the album contents and download the attachments
                album_contents = get_album_contents(section["id"], album["id"])
                for content in album_contents["content"]:
                    if content["type"] == "image" or content["type"] == "video":
                        for content_file in content["attachments"]["files"]["file"]:
                            download_file(content_file["download_path"], content_file["filename"], local_path)

                # Add album to downloaded albums in config
                user_info["downloaded_albums"].append({
                    "id": album["id"],
                    "course_id": section["id"],
                    "title": album["title"],
                    "downloaded_at": int(time.time()),
                })

        # Update children info
        children_info.append(child_info)

    user_info["children"] = children_info
    user_info["last_updated"] = int(time.time())

    save_config(config)

if __name__ == "__main__":
    main()
