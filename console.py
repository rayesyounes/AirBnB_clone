#!/usr/bin/python3
""" Command line interpreter """
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """The console class"""

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
        """Exit the program on End Of File"""
        print()
        return True

    def handle_empty_line(self, arg):
        """Handles empty lines by doing nothing"""
        pass

    def do_create(self, arg):
        """Create a new instance of BaseModel, save it, and print the ID"""
        args = arg.split()
        if not arg:
            print("** class name missing **")
            return
        if args[0] not in self.class_name:
            print("** class doesn't exist **")
            return
        new_instance = self.class_name[args[0]]()
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
        if instance_id[0] == instance_id[-1] == '"':
            instance_id = instance_id[1:-1]
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
        if instance_id[0] == instance_id[-1] == '"':
            instance_id = instance_id[1:-1]
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
            filtered_objects = [str(obj) for key, obj in storage.all().items()
                                if key.startswith(class_name + ".")]
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

        if instance_id[0] == instance_id[-1] == '"':
            instance_id = instance_id[1:-1]
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

    def do_count(self, arg):
        """
        Counts the number of instances of a specific class
        """
        class_name = arg.strip()
        if class_name not in self.class_name:
            print("** class doesn't exist **")
            return

        count = 0
        for obj in storage.all().values():
            if class_name == obj.__class__.__name__:
                count += 1
        print(count)

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        commands = {
            "all": self.do_all,
            "count": self.do_count,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "update": self.do_update
        }
        args = re.search(r"\.", arg)
        if args is None:
            print("*** Invalid command: {} ***".format(arg))
            return False
        else:
            com = [arg[:args.start()], arg[args.end():]]
            args = re.search(r"\((.*?)\)", com[1])
            if args is not None:
                command = [com[1][:args.start()], args.group(1)]
                if command[0] in commands.keys():
                    res = "{} {}".format(com[0], command[1])
                    return commands[command[0]](res)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
