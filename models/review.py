#!/usr/bin/python3
from models.base_model_update import BaseModel

class Review(BaseModel):
	"""
	Class Review that inherits from BaseModel
	"""
	place_id = ""
	user_id = ""
	text = ""

