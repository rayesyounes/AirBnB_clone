#!/usr/bin/python3

import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "
    class_name = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """Exit the program on EOF (Ctrl+D)"""
        print()
        return True

    def handle_empty_line(self, arg):
        """Eliminates empty lines"""
        return False

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it, and print the ID"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        if args[0] not in self.class_name:
            print("** class doesn't exist **")
            return
        new_instance = self.class_name[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """Print the string representation of an instance"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if args[0] not in self.class_name:
            print("** class doesn't exist **")
            return
        class_name = args[0]
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        obj = storage.all()
        if key in obj:
            print(obj[key])
        else:
            print("** no instance found **")

    def do_destroy(self, arg):
        """Delete an instance based on the class name and ID"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if args[0] not in self.class_name:
            print("** class doesn't exist **")
            return
        class_name = args[0]
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        obj = storage.all()
        if key in obj:
            del obj[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """Print all instances or instances of a specific class"""
        if not arg:
            objects = [str(obj) for obj in storage.all().values()]
            print(objects)
        else:
            args = arg.split()
            if args[0] not in self.class_name:
                print("** class doesn't exist **")
                return
            class_name = args[0]
            filtered_objects = [
                str(obj) for key, obj in storage.all().items()
                if key.startswith(class_name + ".")
            ]
            print(filtered_objects)

    def do_update(self, arg):
        """Update an instance based on the class name and ID"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return
        class_name = args[0]
        instance_id = args[1]
        key = "{}.{}".format(class_name, instance_id)
        obj = storage.all()
        if key not in obj:
            print("** no instance found **")
            return
        attribute_name = args[2]
        attribute_value = args[3]
        if attribute_value[0] == attribute_value[-1] == '"':
            attribute_value = attribute_value[1:-1]
        try:
            attribute_value = int(attribute_value)
        except ValueError:
            try:
                attribute_value = float(attribute_value)
            except ValueError:
                pass
        setattr(obj[key], attribute_name, attribute_value)
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()