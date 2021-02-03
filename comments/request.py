import sqlite3
import json
from models import Comment
## import datetime from datetime so we don't get everything in datetime package.
## if just import datetime, you'll get everything. Now we only get datetime
## datetime is a function in the datetime package
from datetime import datetime


def get_all_comments():
    # Open a connection to the database
    with sqlite3.connect("./rare.db") as conn:

        # Just use these. It's a Black Box.
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # Write the SQL query to get the information you want
        db_cursor.execute("""
        SELECT
        a.id,
        a.post_id,
        a.author_id,
        a.content,
        a.time
        FROM Comments a
        """)

        # Initialize an empty list to hold all animal representations
        comments = []

        # Convert rows of data into a Python list
        dataset = db_cursor.fetchall()

        # Iterate list of data returned from database
        for row in dataset:

            comment = Comment(row["id"], row["post_id"], row["author_id"], row["content"], row["time"])
            # Add the dictionary representation of the animal to the list
            comments.append(comment.__dict__)

    # Use `json` package to properly serialize list as JSON
    return json.dumps(comments)

def create_comment(new_comment):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()
        conn.row_factory = sqlite3.Row


        db_cursor.execute("""
        INSERT INTO Comments
            ( post_id, author_id, content, time )
        VALUES
            ( ?, ?, ?, ? );
        """, (new_comment['post_id'], new_comment['author_id'],
              new_comment['content'], datetime.now() ))
              ## .now gets date and time right now


        id = db_cursor.lastrowid

        # Add the `id` property to the comment dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_comment['id'] = id

        return json.dumps(new_comment)

def delete_comment(id):
    with sqlite3.connect("./rare.db") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Comments
        WHERE id = ?
        """, (id, ))