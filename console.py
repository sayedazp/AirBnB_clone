#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    @staticmethod
    def parser(line):  # pre command processing
        return [i.strip(",") for i in split(line)]

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, line):
        """Usage:$ create BaseModel.
        Creates a new instance of BaseModel,\
        saves it (to the JSON file) and prints the id"""
        args = self.parser(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in storage.classes.keys():
            print("** class doesn't exist **")
        else:
            print(storage.classes[args[0]]().id)
            storage.save()

    def do_show(self, line):
        """Usage:$ show BaseModel 1234-1234-1234.
        Prints the string representation of an instance \
        based on the class name and id.
        """
        args = self.parser(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in storage.classes.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            dicObjRepre = storage.all()
            if "{}.{}".format(args[0], args[1]) not in dicObjRepre:
                print("** no instance found **")
            else:
                print(dicObjRepre["{}.{}".format(args[0], args[1])])

    def do_destroy(self, line):
        """Usage:$ destroy BaseModel 1234-1234-1234.
        Deletes an instance based on the class name and \
        id (save the change into the JSON file)."""
        args = self.parser(line)
        if len(args) == 0:
            print("** class name missing **")
        elif args[0] not in storage.classes.keys():
            print("** class doesn't exist **")
        elif len(args) == 1:
            print("** instance id missing **")
        else:
            dicObjRepre = storage.all()
            if "{}.{}".format(args[0], args[1]) not in dicObjRepre:
                print("** no instance found **")
            else:
                storage.delete(*args)
                storage.save()

    def do_all(self, line):
        """Usage:$ all BaseModel or $ all
        Prints all string representation of all instances \
        based or not on the class name"""
        args = self.parser(line)
        if len(args) > 0 and args[0] not in storage.classes.keys():
            print("** class doesn't exist **")
        else:
            objects = []
            for obj in storage.all().values():
                if len(args) > 0 and args[0] == obj.__class__.__name__:
                    objects.append(obj.__str__())
                elif len(args) == 0:
                    objects.append(obj.__str__())
            print(objects)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, line):
        """Usage:$ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        Updates an instance based on the class name and id by \
        adding or updating attribute"""
        args = self.parser(line)

        if len(args) == 0:
            print("** class name missing **")
            return
        if args[0] not in storage.classes.keys():
            print("** class doesn't exist **")
            return
        if len(args) == 1:
            print("** instance id missing **")
            return
        dicObjRepre = storage.all()
        if "{}.{}".format(args[0], args[1]) not in dicObjRepre.keys():
            print("** no instance found **")
            return
        if len(args) == 2:
            print("** attribute name missing **")
            return
        if len(args) == 3 and not isinstance(eval(args[2]), dict):
            print("** value missing **")
            return
        if len(args) == 4:
            obj = dicObjRepre["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = valtype(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
