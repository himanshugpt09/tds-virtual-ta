from load_discourse import load_all_posts
from load_course import load_course_pages

def load_all_docs():
    discourse_docs = load_all_posts('discourse_json')
    course_docs = load_course_pages('tds_pages_md', 'metadata.json')
    return discourse_docs + course_docs
