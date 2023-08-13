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

    def default(self, arg):
        """defines what should happen when input in different form"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.count,
            "update": self.do_update
        }
        dotted = re.search(r"\.", arg)
        if dotted is not None:
            parsed = [arg[:dotted.span()[0]], arg[dotted.span()[1]:]]
            parenth = re.search(r"\((.*?)\)", parsed[1])
            if dotted is not None:
                args = [parsed[1][:parenth.span()[0]], parenth.group()[1:-1]]
                if args[0] in argdict.keys():
                    call = "{} {}".format(parsed[0], args[1])
                    return argdict[args[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def count(self, arg):
        """internal counting logic to count instances of certain class"""
        arg = arg.strip(", ")
        count = 0
        for instance in storage.all().values():
            if arg == instance.__class__.__name__:
                count += 1
        return count

    @staticmethod
    def parser(line):  # pre command processing
        """Parser to parse the input to out the input vars"""
        return [i.strip(",") for i in split(line)]

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

    def do_update(self, line):
        """Usage:$ update BaseModel 1234-1234-1234 email "aibnb@mail.com"
        Updates an instance based on the class name and id by \
        adding or updating attribute"""
        args = self.parser(line)

        if len(args) == 0:
            print("** class name missing **")
            return False
        if args[0] not in storage.classes.keys():
            print("** class doesn't exist **")
            return False
        if len(args) == 1:
            print("** instance id missing **")
            return False
        dicObjRepre = storage.all()
        if "{}.{}".format(args[0], args[1]) not in dicObjRepre.keys():
            print("** no instance found **")
            return False
        if len(args) == 2:
            print("** attribute name missing **")
            return False
        if len(args) == 3:
            try:
                type(eval(args[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(args) == 4:
            obj = dicObjRepre["{}.{}".format(args[0], args[1])]
            if args[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[args[2]])
                obj.__dict__[args[2]] = valtype(args[3])
            else:
                obj.__dict__[args[2]] = args[3]
        storage.save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
