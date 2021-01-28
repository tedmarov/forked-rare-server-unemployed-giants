# AUTHOR: Travis Stevenson
# PURPOSE: This module defines the blueprint for the
# Category class.

class Category():

    # Class initializer. It has 2 custom parameters, with the
    # special `self` parameter that every method on a class
    # needs as the first parameter.
    def __init__(self, id, label):
        self.id = id
        self.label = label
