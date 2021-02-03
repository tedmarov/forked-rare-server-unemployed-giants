# PURPOSE: This module defines the blueprint for the Post Tag class

# Class initializer. It has 3 custom parameters, with the
# special `self` parameter that every method on a class
# needs as the first parameter.

class PostTag: 

    def __init__(self, id, post_id, tag_id):
        self.id = id
        self.post_id = post_id
        self.tag_id = tag_id
