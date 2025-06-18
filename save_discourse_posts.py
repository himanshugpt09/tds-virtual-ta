import os
import json
from bs4 import BeautifulSoup

def load_all_posts(folder='discourse_json'):
    posts = []
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            with open(os.path.join(folder, filename), 'r', encoding='utf-8') as f:
                topic = json.load(f)
                topic_id = topic.get("id", "unknown")
                topic_title = topic.get("title", "")
                for post in topic['post_stream']['posts']:
                    cooked = post.get('cooked', '')
                    clean_text = BeautifulSoup(cooked, 'html.parser').get_text()
                    posts.append({
                        "topic_id": topic_id,
                        "topic_title": topic_title,
                        "post_number": post['post_number'],
                        "reply_to_post_number": post.get('reply_to_post_number'),
                        "content": clean_text.strip()
                    })
    return posts

if __name__ == "__main__":
    all_posts = load_all_posts()
    with open("discourse_posts.json", "w", encoding="utf-8") as f:
        json.dump(all_posts, f, indent=2)
    print(f"✅ Saved {len(all_posts)} posts to discourse_posts.json")
