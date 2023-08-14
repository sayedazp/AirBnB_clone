#!/usr/bin/python3
"""Defines unittests for models/city.py.

Unittest classes:
    TestCity_instantiation
    TestCity_save
    TestCity_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.city import City


class TestCity_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the City class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(City().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_citymodel = City()
        self.assertIn("id", my_citymodel.to_dict())
        self.assertIn("created_at", my_citymodel.to_dict())
        self.assertIn("updated_at", my_citymodel.to_dict())
        self.assertIn("__class__", my_citymodel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_citymodel = City()
        my_citymodel.middle_name = "ahmed"
        my_citymodel.my_number = 96
        self.assertEqual("ahmed", my_citymodel.middle_name)
        self.assertIn("my_number", my_citymodel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_citymodel = City()
        cy_dict = my_citymodel.to_dict()
        self.assertEqual(str, type(cy_dict["id"]))
        self.assertEqual(str, type(cy_dict["created_at"]))
        self.assertEqual(str, type(cy_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_citymodel = City()
        my_citymodel.id = "123456"
        my_citymodel.created_at = my_citymodel.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'City',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(my_citymodel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_citymodel = City()
        self.assertNotEqual(my_citymodel.to_dict(), my_citymodel.__dict__)

    def test_to_dict_with_arg(self):
        my_citymodel = City()
        with self.assertRaises(TypeError):
            my_citymodel.to_dict(None)

class TestCity_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the City class."""

    def test_no_args_instantiates(self):
        self.assertEqual(City, type(City()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(City(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(City().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(City().updated_at))

    def test_state_id_is_public_class_attribute(self):
        my_citymodel = City()
        self.assertEqual(str, type(City.state_id))
        self.assertIn("state_id", dir(my_citymodel))
        self.assertNotIn("state_id", my_citymodel.__dict__)

    def test_name_is_public_class_attribute(self):
        my_citymodel = City()
        self.assertEqual(str, type(City.name))
        self.assertIn("name", dir(my_citymodel))
        self.assertNotIn("name", my_citymodel.__dict__)

    def test_two_cities_unique_ids(self):
        cy1 = City()
        cy2 = City()
        self.assertNotEqual(cy1.id, cy2.id)

    def test_two_cities_different_created_at(self):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.created_at, cy2.created_at)

    def test_two_cities_different_updated_at(self):
        cy1 = City()
        sleep(0.05)
        cy2 = City()
        self.assertLess(cy1.updated_at, cy2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_citymodel = City()
        my_citymodel.id = "123456"
        my_citymodel.created_at = my_citymodel.updated_at = dt
        cystr = my_citymodel.__str__()
        self.assertIn("[City] (123456)", cystr)
        self.assertIn("'id': '123456'", cystr)
        self.assertIn("'created_at': " + dt_repr, cystr)
        self.assertIn("'updated_at': " + dt_repr, cystr)

    # def test_args_unused(self):
    #     my_citymodel = City(None)
    #     self.assertNotIn(None, my_citymodel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_citymodel = City(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_citymodel.id, "345")
        self.assertEqual(my_citymodel.created_at, dt)
        self.assertEqual(my_citymodel.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            City(id=None, created_at=None, updated_at=None)


class TestCity_save(unittest.TestCase):
    """Unittests for testing save method of the City class."""

    @classmethod
    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_one_save(self):
        my_citymodel = City()
        sleep(0.05)
        first_updated_at = my_citymodel.updated_at
        my_citymodel.save()
        self.assertLess(first_updated_at, my_citymodel.updated_at)

    def test_two_saves(self):
        my_citymodel = City()
        sleep(0.05)
        first_updated_at = my_citymodel.updated_at
        my_citymodel.save()
        second_updated_at = my_citymodel.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_citymodel.save()
        self.assertLess(second_updated_at, my_citymodel.updated_at)

    def test_save_with_arg(self):
        my_citymodel = City()
        with self.assertRaises(TypeError):
            my_citymodel.save(None)

    def test_save_updates_file(self):
        my_citymodel = City()
        my_citymodel.save()
        cyid = "City." + my_citymodel.id
        with open("file.json", "r") as f:
            self.assertIn(cyid, f.read())



if __name__ == "__main__":
    unittest.main()

