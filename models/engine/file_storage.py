#!/usr/bin/python3
import json
import os

class FileStorage:
	"""
	Serializes and instances to a JSON file
	and deserializes JSON file to instances
	"""
	__file_path = "file.json"
	__objects = {}

	def all(self):
		"""
		Returns the dictionary __objects
		"""
		return FileStorage.__objects

	def new(self, obj):
		"""
		Sets in __objects the obj with key <obj class name>.id
		"""
		key = f"{obj.__class__.__name__}.{obj.id}"
		self.__class__.__objects[key] = obj

	def save(self):
		"""
		Serializes __objects to the JSON file
		"""
		data = {}
		for key, value in self.__class__.__objects.items():
			data[key] = value.to_dict()
		with open(self.__file_path, "w") as write_file:
			json.dump(data, write_file)

	def reload(self):
		"""
		Deserializes the JSON file to __objects if it exists
		"""
		from models.base_model import BaseModel
		from models.user import User
		class_mapping = {
			"BaseModel": BaseModel,
			"User": User,
                        "State": State,
                        "City": City,
                        "Amenity": Amenity,
                        "Place": Place,
                        "Review": Review
		}
		if os.path.exists(FileStorage.__file_path):
			with open(FileStorage.__file_path) as read_file:
				data = json.load(read_file)
				FileStorage.__objects = {}
				for key, value in data.items():
					class_name, obj_id = key.split(".")
					if class_name in class_mapping:
						cls = class_mapping[class_name]
						obj = cls(**value)
						FileStorage.__objects[key] = obj
