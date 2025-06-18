import os
import json

def load_course_pages(folder='tds_pages_md', metadata_file='metadata.json'):
    with open(metadata_file, 'r', encoding='utf-8') as f:
        metadata = json.load(f)

    docs = []
    for item in metadata:
        filepath = os.path.join(folder, item['filename'])
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                docs.append({
                    "text": content.strip(),
                    "url": item['original_url']
                })
    return docs
