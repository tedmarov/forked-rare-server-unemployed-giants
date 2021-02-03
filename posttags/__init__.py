# PURPOSE: This module is responsible for turning the post tags directory
# into a Python package so that we can use the functions within it elsewhere
# in the project.

from .request import get_all_post_tags, create_post_tag