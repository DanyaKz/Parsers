from facebook_page_scraper import Facebook_scraper
import re
import json
from datetime import datetime

# Page/group settings and keywords
keywords = ['вакцина', 'gathering','ағайын' , 'вакцин', 'вакцинация', 'вакцинациясы', 'вакцинациядан', 'тарту', 'иммунизациясы', 'екпе', 'прививка', 'прививки', 'вакцины', 'иммунизация']
page_or_group_name = "id"
posts_count = 20
browser = "firefox"
timeout = 200 
headless = True
credentials = ("email", "password")
# Indicates if the Facebook target is a group or a page
isGroup = True

# Create scraper object
data = Facebook_scraper(
    page_or_group_name, 
    posts_count, 
    browser,  
    timeout=timeout, 
    headless=headless, 
    isGroup=isGroup
)

# Get all posts
try:
    posts = data.scrap_to_json()
    all_posts = [post for post in posts]
except Exception as e:
    print(f"An error occurred while retrieving posts: {e}")
    all_posts = []

# Filter posts by keywords in the content
filtered_posts = []
for post in all_posts:
    for keyword in keywords:
        if re.search(keyword, post['content'], re.IGNORECASE):
            filtered_posts.append(post)
            break

print(f"Found {len(filtered_posts)} posts matching keywords.")

# Collect comments from the filtered posts
comments_data = {"facebook": []}

for post in filtered_posts:
    post_id = post['post_id']
    try:
        comments = scraper.get_comments(post_id=post_id)
        for comment in comments:
            comment_data = {
                "Nickname": comment['username'],
                "Date": datetime.strptime(comment['created_time'], '%Y-%m-%d %H:%M:%S').isoformat() + "+00:00",
                "Likes": comment['like_count'],
                "Comment": comment['text'],
                "Source": post['post_url']
            }
            comments_data["facebook"].append(comment_data)
    except Exception as e:
        print(f"An error occurred while retrieving comments for post {post_id}: {e}")

# Save comments to a JSON file
with open("comments.json", "w", encoding="utf-8") as f:
    json.dump(comments_data, f, ensure_ascii=False, indent=4)

print("Comments saved to comments.json")
