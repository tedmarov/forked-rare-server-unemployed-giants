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

        # Initializes posts as an empy dict instead of a list
        posts = {}

        dataset = db_cursor.fetchall()
        for row in dataset:
            #Checks to see if the key coresponding to that row's id is in the dictionary already.
            if row['id'] in posts:
                #If it is, takes the tag_id and label responses from that query and appends them to the tags list that is a nested dictionary within the bigger posts dictionary
                tag = Tag(row['tag_id'], row['label'])
                posts[row['id']].tags.append(tag.__dict__)


            else:
                #If a key doesn't exist corresponding with the post's id, it makes a new key/value pair in the dict
                post = Post(row['id'],row['user_id'], row['category_id'], row['title'],
                row['publication_date'], row['content'],row['approved'], row['image_url'])

                #This becomes the key, and the post is the value.
                posts[row['id']] = post


                tag = Tag(row['tag_id'], row['label'])
                
                #Creates and then appends the tag key as a key/value pair nested in the bigger posts dictionary
                posts[row['id']].tags = []
                posts[row['id']].tags.append(tag.__dict__)


        #Makes a list, then loops through the values of posts (ignoring the keys) and puts every value into dict_posts as a dictionary, so we have a list of dictionaries like normal to send to the server
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
        """, (new_post['user_id'], new_post['category_id'], new_post['title'],
              new_post['publication_date'], new_post['image_url'],
              new_post['content'], new_post['approved'], ))

        id = db_cursor.lastrowid
        new_post['id'] = id
    return json.dumps(new_post)


def delete_post(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Posts
        WHERE id = ?
        """, (id, ))


def get_post_by_id(id):
    with sqlite3.connect("./rare.db") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

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
        """, (id, ))

        data = db_cursor.fetchone()

        post = Post(data['id'], data['user_id'], data['category_id'], data['title'],
                    data['publication_date'], data['content'], data['approved'], data['image_url'])

        post = post.__dict__

        #sets two properties acquired from the join that are not automatically on the Post model
        post['author'] = data['username']
        post['category'] = data['label']


        #Queries for all instances of tag/post many to many relationships and gets the appriopriate tag information
        db_cursor.execute("""
        SELECT
            p.id,
            p.post_id,
            p.tag_id,
            t.id,
            t.label
        FROM PostTags p
        LEFT JOIN Tags t ON p.tag_id = t.id
        WHERE p.post_id = ?
        """, ( post['id'], ))

        dataset = db_cursor.fetchall()

        tags = []

        #Loops through and creates appropriate tags for each tag/post relationship
        for row in dataset:
            tag = Tag(row['tag_id'], row['label'])
            tags.append(tag.__dict__)

        #Assigns all tags associated with a post as a list that is the value of the 'tags' key
        post['tags'] = tags

        return json.dumps(post)


def get_user_posts(user_id):
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
            p.approved
        FROM Posts p
        Where p.user_id = ?
        """, (user_id,))

        posts = []
        dataset = db_cursor.fetchall()
        for row in dataset:

            post = Post(row['id'], row['user_id'], row['category_id'], row['title'],
                        row['publication_date'], row['image_url'], row['content'], row['approved'])

            posts.append(post.__dict__)
    return json.dumps(posts)
