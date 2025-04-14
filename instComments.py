from instagrapi import Client
import json
import os
import time
from datetime import datetime


def fetch_comments(cl, media_id):
    """
    Fetches comments for the given media_id (post).
    
    :param cl: instagrapi client object
    :param media_id: media (post) identifier
    :return: list of comment dictionaries
    """
    comments = cl.media_comments(media_id)
    return [comment.dict() for comment in comments]

def format_data(media, comment):
    """
    Formats a comment for saving to JSON.
    
    :param media: dictionary with post data
    :param comment: dictionary with comment data
    :return: dictionary with formatted data
    """
    return {
        "Nickname": comment['user']['username'],
        "Date": comment['created_at_utc'].isoformat(),
        "Likes": comment['like_count'],
        "Comment": comment['text'],
        "Source": media['link']
    }

def append_to_json(data, file_name):
    """
    Appends new data to a JSON file. Creates the file if it doesn't exist.
    
    :param data: list of new entries
    :param file_name: file name to save data into
    """
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {"inst": []}
        existing_data["inst"].extend(data)
    else:
        existing_data = {"inst": data}

    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, ensure_ascii=False, indent=4)
    print(f"Data updated in {file_name}")

def save_state(last_key, state_file="state.json"):
    """
    Saves the state of the last successfully processed post.
    
    :param last_key: key (post number)
    :param state_file: path to state file
    """
    with open(state_file, "w", encoding="utf-8") as file:
        json.dump({"last_key": last_key}, file)

def load_state(state_file="state.json"):
    """
    Loads state from file (last processed post number).
    
    :param state_file: path to state file
    :return: last_key or None if file doesn't exist
    """
    if os.path.exists(state_file):
        with open(state_file, "r", encoding="utf-8") as file:
            return json.load(file).get("last_key")
    return None


media_file_name = "whoINST.json"
comments_file_name = "whoComments.json"
state_file = "state.json"

cl = Client()
cl.login("login","password")

try:
    if os.path.exists(media_file_name):
        with open(media_file_name, "r", encoding="utf-8") as file:
            media_data = json.load(file)
        
        last_key = load_state(state_file)
        start_processing = False if last_key else True

        for post_num, media in media_data.items():
            if post_num == last_key:
                start_processing = True
                continue
            if not start_processing:
                continue

            media_id = media['id']
            try:
                comments = fetch_comments(cl, media_id)
                formatted_comments = [format_data(media, comment) for comment in comments]
                append_to_json(formatted_comments, comments_file_name)
                save_state(post_num, state_file)
            except Exception as e:
                print(f"Error while processing comments for post {media_id}: {e}. Waiting 5 minutes before retrying...")
                time.sleep(300)
                continue
except Exception as e:
    print(f"An error occurred: {e}")