class User:

    #Class initializer
    def __init__(self, id, first_name, last_name, email, password, bio = "", username = "", profile_image_url = "", active = True, created_on = ""):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.bio = bio
        self.username = username
        self.profile_image_url = profile_image_url
        self.active = active
        self.created_on = created_on