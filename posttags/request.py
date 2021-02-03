import sqlite3
import json
from models import PostTag

def get_all_post_tags():
    with sqlite3.connect("./rare.db") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
            SELECT
                t.id,
                t.post_id,
                t.tag_id
            FROM PostTags t
        """)

        post_tags = []

        dataset = db_cursor.fetchall()

        for row in dataset:

            post_tag = PostTag(row['id'], row['post_id'], row['tag_id'])
            post_tags.append(post_tag.__dict__)

    return json.dumps(post_tags)

def create_post_tag(new_post_tag):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        Insert Into PostTags
            ( post_id, tag_id )
        Values
            ( ?, ? );
        """, (new_post_tag['post_id'], new_post_tag['tag_id']))

    
        id = db_cursor.lastrowid

     
        new_post_tag['id'] = id

    return json.dumps(new_post_tag)    