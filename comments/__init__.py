# PURPOSE: This module is responsible for turning the comments directory
# into a Python package so that we can use the functions within it elsewhere
# in the project.

from .request import create_comment, delete_comment, get_all_comments