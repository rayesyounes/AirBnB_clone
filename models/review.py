#!/usr/bin/python3
""" Doc Here """
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Class Review that inherits from BaseModel
    """
    place_id = ""
    user_id = ""
    text = ""
