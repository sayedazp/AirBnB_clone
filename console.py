#!/usr/bin/python3
"""define console class and entry point of the project"""
import cmd
from shlex import split
from models import storage
from models.user import User
import re


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = '(hbnb)'
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

    def do_quit(self, line):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, line):
        """End of file ctrl+d signal"""
        print("")
        return True

    def emptyline(self):
        """overriding the original emptyline function"""
        pass

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

    def do_all(self, arg):  # edited
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl = self.parser(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = self.parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
