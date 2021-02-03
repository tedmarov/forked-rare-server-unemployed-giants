# PURPOSE: This module defines the blueprint for the Post class

# Class initializer. It has 8 custom parameters, with the
# special `self` parameter that every method on a class
# needs as the first parameter.

class Post():

    def __init__(self, id, user_id, category_id, title, publication_date, 
         content, approved, image_url = "" ):
        self.id = id
        self.userId = user_id
        self.categoryId = category_id
        self.title = title
        self.publicationDate = publication_date
        self.imageUrl = image_url
        self.content = content
        self.approved = approved