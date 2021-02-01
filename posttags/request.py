import sqlite3
import json
from models import PostTag

def get_all_post_tags():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
            SELECT
                t.id,
                t.post_id,
                t.tag_id
            FROM PostTags t
        """)

        # Initialize an empty list to hold all tag representations
        post_tags = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            # Create an tag instance from the current row.
            # Note that the database fields are specified in
            # exact order of the parameters defined in the
            # tag class above.
            post_tag = PostTag(row['id'], row['post_id'], row['tag_id'])

            post_tags.append(post_tag.__dict__)

    # Use `json` package to properly serialize list as JSON
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

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the category dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_post_tag['id'] = id

    return json.dumps(new_post_tag)    