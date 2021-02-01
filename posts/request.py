import sqlite3
import json
from models import Post, Tag

def get_all_posts():
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            p.id,
            p.user_id,
            p.category_id,
            p.title,
            p.publication_date,
            p.image_url,
            p.content,
            p.approved,
            b.post_id,
            b.tag_id,
            t.label
        FROM Posts p
        LEFT JOIN PostTags b
        on p.id == b.post_id
        LEFT JOIN Tags t
        on t.id == b.tag_id
        """)

        posts = {}
        dataset = db_cursor.fetchall()
        for row in dataset:
            if row['id'] in posts:
                tag = Tag(row['tag_id'], row['label'])
                posts[row['id']].tags.append(tag.__dict__)

                posts.append(tag.__dict__)

            else:
                post = Post(row['id'],row['user_id'], row['category_id'], row['title'],
                row['publication_date'], row['content'],row['approved'], row['image_url'])

                posts[row['id']] = post

                tag = Tag(row['tag_id'], row['label'])
                posts[row['id']].tags = []
                posts[row['id']].tags.append(tag.__dict__)


        dict_posts = []
        for post in posts.values():
            dict_posts.append(post.__dict__)

    return json.dumps(dict_posts)


def create_post(new_post):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Posts
            (user_id, category_id, title, publication_date, image_url, content, approved)
        VALUES
            (?,?,?,?,?,?,?)
        """,(new_post['userId'], new_post['categoryId'], new_post['title'],
            new_post['publicationDate'], new_post['imageUrl'], 
            new_post['content'],new_post['approved'], ))
        
        id = db_cursor.lastrowid
        new_post['id'] = id
    return json.dumps(new_post)

def get_post_by_id(id):
     with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        #Set values passed in from form
        db_cursor.execute("""
        SELECT
            u.id,
            u.user_id,
            u.category_id,
            u.title,
            u.publication_date,
            u.image_url,
            u.content,
            u.approved,
            b.username,
            c.label
        FROM posts u
        LEFT JOIN users b ON u.user_id = b.id
        LEFT JOIN categories c on u.category_id = c.id
        WHERE u.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'], data['publication_date']
        , data['content'], data['approved'], data['image_url'])

        post=post.__dict__

        post['author'] = data['username']
        post['category'] = data['label']

        return json.dumps(post)
