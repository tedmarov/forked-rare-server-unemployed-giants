class Comment:
    def __init__(self, id, post_id, author_id, content):
        self.id = id
        self.content = content
        self.post_id = post_id
        self.author_id = author_id
        