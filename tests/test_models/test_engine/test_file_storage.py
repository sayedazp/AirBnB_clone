#!/usr/bin/python3
"""Defines unittests for models/engine/file_storage.py.

Unittest classes:
    TestFileStorage_instantiation
    TestFileStorage_methods
"""
import os
import json
import models
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class TestFileStorage_methods(unittest.TestCase):
    """Unittests for testing methods of the FileStorage class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    @classmethod
    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}

    def test_all(self):
        self.assertEqual(dict, type(models.storage.all()))

    def test_all_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.all(None)

    def test_new(self):
        my_basemodel = BaseModel()
        my_usermodel = User()
        my_statemodel = State()
        my_placemodel = Place()
        my_citymodel = City()
        my_amenitymodel = Amenity()
        my_reviewmodel = Review()
        models.storage.new(my_basemodel)
        models.storage.new(my_usermodel)
        models.storage.new(my_statemodel)
        models.storage.new(my_placemodel)
        models.storage.new(my_citymodel)
        models.storage.new(my_amenitymodel)
        models.storage.new(my_reviewmodel)
        self.assertIn("BaseModel." + my_basemodel.id, models.storage.all().keys())
        self.assertIn(my_basemodel, models.storage.all().values())
        self.assertIn("User." + my_usermodel.id, models.storage.all().keys())
        self.assertIn(my_usermodel, models.storage.all().values())
        self.assertIn("State." + my_statemodel.id, models.storage.all().keys())
        self.assertIn(my_statemodel, models.storage.all().values())
        self.assertIn("Place." + my_placemodel.id, models.storage.all().keys())
        self.assertIn(my_placemodel, models.storage.all().values())
        self.assertIn("City." + my_citymodel.id, models.storage.all().keys())
        self.assertIn(my_citymodel, models.storage.all().values())
        self.assertIn("Amenity." + my_amenitymodel.id, models.storage.all().keys())
        self.assertIn(my_amenitymodel, models.storage.all().values())
        self.assertIn("Review." + my_reviewmodel.id, models.storage.all().keys())
        self.assertIn(my_reviewmodel, models.storage.all().values())

    def test_new_with_args(self):
        with self.assertRaises(TypeError):
            models.storage.new(BaseModel(), 1)

    def test_save(self):
        my_basemodel = BaseModel()
        my_usermodel = User()
        my_statemodel = State()
        my_placemodel = Place()
        my_citymodel = City()
        my_amenitymodel = Amenity()
        my_reviewmodel = Review()
        models.storage.new(my_basemodel)
        models.storage.new(my_usermodel)
        models.storage.new(my_statemodel)
        models.storage.new(my_placemodel)
        models.storage.new(my_citymodel)
        models.storage.new(my_amenitymodel)
        models.storage.new(my_reviewmodel)
        models.storage.save()
        save_text = ""
        with open("file.json", "r") as f:
            save_text = f.read()
            self.assertIn("BaseModel." + my_basemodel.id, save_text)
            self.assertIn("User." + my_usermodel.id, save_text)
            self.assertIn("State." + my_statemodel.id, save_text)
            self.assertIn("Place." + my_placemodel.id, save_text)
            self.assertIn("City." + my_citymodel.id, save_text)
            self.assertIn("Amenity." + my_amenitymodel.id, save_text)
            self.assertIn("Review." + my_reviewmodel.id, save_text)

    def temy_statemodel_save_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.save(None)

    def test_reload(self):
        my_basemodel = BaseModel()
        my_usermodel = User()
        my_statemodel = State()
        my_placemodel = Place()
        my_citymodel = City()
        my_amenitymodel = Amenity()
        my_reviewmodel = Review()
        models.storage.new(my_basemodel)
        models.storage.new(my_usermodel)
        models.storage.new(my_statemodel)
        models.storage.new(my_placemodel)
        models.storage.new(my_citymodel)
        models.storage.new(my_amenitymodel)
        models.storage.new(my_reviewmodel)
        models.storage.save()
        models.storage.reload()
        objs = FileStorage._FileStorage__objects
        self.assertIn("BaseModel." + my_basemodel.id, objs)
        self.assertIn("User." + my_usermodel.id, objs)
        self.assertIn("State." + my_statemodel.id, objs)
        self.assertIn("Place." + my_placemodel.id, objs)
        self.assertIn("City." + my_citymodel.id, objs)
        self.assertIn("Amenity." + my_amenitymodel.id, objs)
        self.assertIn("Review." + my_reviewmodel.id, objs)

    def test_reload_with_arg(self):
        with self.assertRaises(TypeError):
            models.storage.reload(None)

class TestFileStorage_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the FileStorage class."""

    def test_FileStorage_instantiation_no_args(self):
        self.assertEqual(type(FileStorage()), FileStorage)

    def test_FileStorage_instantiation_with_arg(self):
        with self.assertRaises(TypeError):
            FileStorage(None)

    def test_FileStorage_file_path_is_private_str(self):
        self.assertEqual(str, type(FileStorage._FileStorage__file_path))

    def testFileStorage_objects_is_private_dict(self):
        self.assertEqual(dict, type(FileStorage._FileStorage__objects))

    def test_storage_initializes(self):
        self.assertEqual(type(models.storage), FileStorage)

if __name__ == "__main__":
    unittest.main()

