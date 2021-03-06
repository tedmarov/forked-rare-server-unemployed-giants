# PURPOSE: This module defines the blueprint for the Tag class

class Tag():

    # Class initializer. It has 2 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, label):
        self.id = id
        self.label = label