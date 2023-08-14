#!/usr/bin/python3
"""Defines unittests for models/place.py.

Unittest classes:
    TestPlace_to_dict
    TestPlace_instantiation
    TestPlace_save
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.place import Place


class TestPlace_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Place class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Place().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_placemodel = Place()
        self.assertIn("id", my_placemodel.to_dict())
        self.assertIn("created_at", my_placemodel.to_dict())
        self.assertIn("updated_at", my_placemodel.to_dict())
        self.assertIn("__class__", my_placemodel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_placemodel = Place()
        my_placemodel.middle_name = "ahmed"
        my_placemodel.my_number = 88
        self.assertEqual("ahmed", my_placemodel.middle_name)
        self.assertIn("my_number", my_placemodel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_placemodel = Place()
        pl_dict = my_placemodel.to_dict()
        self.assertEqual(str, type(pl_dict["id"]))
        self.assertEqual(str, type(pl_dict["created_at"]))
        self.assertEqual(str, type(pl_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_placemodel = Place()
        my_placemodel.id = "123456"
        my_placemodel.created_at = my_placemodel.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Place',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(my_placemodel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_placemodel = Place()
        self.assertNotEqual(my_placemodel.to_dict(), my_placemodel.__dict__)

    def test_to_dict_with_arg(self):
        my_placemodel = Place()
        with self.assertRaises(TypeError):
            my_placemodel.to_dict(None)

class TestPlace_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Place class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Place, type(Place()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Place(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Place().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Place().updated_at))

    def test_city_id_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(str, type(Place.city_id))
        self.assertIn("city_id", dir(my_placemodel))
        self.assertNotIn("city_id", my_placemodel.__dict__)

    def test_user_id_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(str, type(Place.user_id))
        self.assertIn("user_id", dir(my_placemodel))
        self.assertNotIn("user_id", my_placemodel.__dict__)

    def test_name_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(str, type(Place.name))
        self.assertIn("name", dir(my_placemodel))
        self.assertNotIn("name", my_placemodel.__dict__)

    def test_description_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(str, type(Place.description))
        self.assertIn("description", dir(my_placemodel))
        self.assertNotIn("desctiption", my_placemodel.__dict__)

    def test_number_rooms_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(int, type(Place.number_rooms))
        self.assertIn("number_rooms", dir(my_placemodel))
        self.assertNotIn("number_rooms", my_placemodel.__dict__)

    def test_number_bathrooms_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(int, type(Place.number_bathrooms))
        self.assertIn("number_bathrooms", dir(my_placemodel))
        self.assertNotIn("number_bathrooms", my_placemodel.__dict__)

    def test_max_guest_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(int, type(Place.max_guest))
        self.assertIn("max_guest", dir(my_placemodel))
        self.assertNotIn("max_guest", my_placemodel.__dict__)

    def test_price_by_night_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(int, type(Place.price_by_night))
        self.assertIn("price_by_night", dir(my_placemodel))
        self.assertNotIn("price_by_night", my_placemodel.__dict__)

    def test_latitude_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(float, type(Place.latitude))
        self.assertIn("latitude", dir(my_placemodel))
        self.assertNotIn("latitude", my_placemodel.__dict__)

    def test_longitude_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(float, type(Place.longitude))
        self.assertIn("longitude", dir(my_placemodel))
        self.assertNotIn("longitude", my_placemodel.__dict__)

    def test_amenity_ids_is_public_class_attribute(self):
        my_placemodel = Place()
        self.assertEqual(list, type(Place.amenity_ids))
        self.assertIn("amenity_ids", dir(my_placemodel))
        self.assertNotIn("amenity_ids", my_placemodel.__dict__)

    def test_two_places_unique_ids(self):
        pl1 = Place()
        pl2 = Place()
        self.assertNotEqual(pl1.id, pl2.id)

    def test_two_places_different_created_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.created_at, pl2.created_at)

    def test_two_places_different_updated_at(self):
        pl1 = Place()
        sleep(0.05)
        pl2 = Place()
        self.assertLess(pl1.updated_at, pl2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_placemodel = Place()
        my_placemodel.id = "123456"
        my_placemodel.created_at = my_placemodel.updated_at = dt
        plstr = my_placemodel.__str__()
        self.assertIn("[Place] (123456)", plstr)
        self.assertIn("'id': '123456'", plstr)
        self.assertIn("'created_at': " + dt_repr, plstr)
        self.assertIn("'updated_at': " + dt_repr, plstr)

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_placemodel = Place(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_placemodel.id, "345")
        self.assertEqual(my_placemodel.created_at, dt)
        self.assertEqual(my_placemodel.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Place(id=None, created_at=None, updated_at=None)


class TestPlace_save(unittest.TestCase):
    """Unittests for testing save method of the Place class."""

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
        my_placemodel = Place()
        sleep(0.05)
        first_updated_at = my_placemodel.updated_at
        my_placemodel.save()
        self.assertLess(first_updated_at, my_placemodel.updated_at)

    def test_two_saves(self):
        my_placemodel = Place()
        sleep(0.05)
        first_updated_at = my_placemodel.updated_at
        my_placemodel.save()
        second_updated_at = my_placemodel.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_placemodel.save()
        self.assertLess(second_updated_at, my_placemodel.updated_at)

    def test_save_with_arg(self):
        my_placemodel = Place()
        with self.assertRaises(TypeError):
            my_placemodel.save(None)

    def test_save_updates_file(self):
        my_placemodel = Place()
        my_placemodel.save()
        plid = "Place." + my_placemodel.id
        with open("file.json", "r") as f:
            self.assertIn(plid, f.read())


if __name__ == "__main__":
    unittest.main()
