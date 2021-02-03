# PURPOSE: This module defines the blueprint for the Comment class

# Class initializer. It has 5 custom parameters, with the
# special `self` parameter that every method on a class
# needs as the first parameter.

class Comment:
    def __init__(self, id, post_id, author_id, content, time):
        self.id = id
        self.content = content
        self.post_id = post_id
        self.author_id = author_id
        self.time = time
        