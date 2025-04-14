from instagrapi import Client
import json
import os
import time
from datetime import datetime

# Proxy settings
proxy = "proxy"

def contains_keyword(caption, keywords):
    """
    Check if caption contains any of the specified keywords.
    """
    return any(keyword in (caption or "").lower() for keyword in keywords)

def fetch_user_medias(cl, username, start, end, keywords):
    """
    Fetch user media and filter by keywords in captions.
    
    :param cl: Instagrapi client
    :param username: Instagram username
    :param start: start index
    :param end: end index
    :param keywords: list of keywords to search in captions
    :return: list of media matching keywords
    """
    user_id = cl.user_id_from_username(username)
    all_medias = []
    end_cursor = None
    while True:
        try:
            medias, end_cursor = cl.user_medias_paginated(user_id, amount=50, end_cursor=end_cursor)
        except Exception as e:
            print(e)
            time.sleep(300)
            continue
        if not medias:
            break
        all_medias.extend(medias)
        if len(all_medias) >= end:
            break
    return [media for i, media in enumerate(all_medias) if contains_keyword(media.caption_text, keywords)]

def save_to_json(data, file_name):
    """
    Save data to a JSON file, merging with existing data if file exists.
    """
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            existing_data = json.load(file)
        existing_data.update(data)
        data = existing_data
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data saved to {file_name}")

# Main logic
file_name = "instData.json"
cl = Client()

# Proxy connection test (optional)
before_ip = cl._send_public_request("api")
cl.set_proxy("proxy")
after_ip = cl._send_public_request("api")

# Login credentials (replace with real credentials)
cl.login("login", "password")

# Keywords to search for in captions
keywords = ['вакцина', 'вакцин', 'вакцинация', 'вакцинациясы', 'вакцинациядан', 'тарту', 'иммунизациясы', 'екпе', 'прививка', 'прививки', 'вакцины', 'иммунизация']

# Set post range for parsing
start_post = int(input("Enter start post number: "))
end_post = int(input("Enter end post number: "))

try:
    medias = fetch_user_medias(cl, "kazsouzrod", start_post, end_post, keywords)
    media_dicts = {
        f"kazsouzrod{i + start_post}": {
            'id': media.id,
            'link': f"https://www.instagram.com/p/{media.code}/"
        }
        for i, media in enumerate(medias)
    }
    print(media_dicts)
    save_to_json(media_dicts, file_name)
except Exception as e:
    print(f"An error occurred: {e}")
