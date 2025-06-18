import os
import json
from bs4 import BeautifulSoup

def load_all_posts(folder='discourse_json'):
    posts = []
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
                topic = json.load(f)
                topic_id = topic.get('id', 'unknown')
                for post in topic['post_stream']['posts']:
                    post_number = post['post_number']
                    cooked = post.get('cooked', '')
                    clean_text = BeautifulSoup(cooked, 'html.parser').get_text()
                    url = f"https://discourse.onlinedegree.iitm.ac.in/t/{topic_id}/{post_number}"
                    posts.append({"text": clean_text.strip(), "url": url})
    return posts
