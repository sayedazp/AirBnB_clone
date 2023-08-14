#!/usr/bin/python3
"""Defines unittests for models/review.py.

Unittest classes:
    TestReview_instantiation
    TestReview_save
    TestReview_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.review import Review


class TestReview_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the Review class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(Review().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_reviewmodel = Review()
        self.assertIn("id", my_reviewmodel.to_dict())
        self.assertIn("created_at", my_reviewmodel.to_dict())
        self.assertIn("updated_at", my_reviewmodel.to_dict())
        self.assertIn("__class__", my_reviewmodel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_reviewmodel = Review()
        my_reviewmodel.middle_name = "Holberton"
        my_reviewmodel.my_number = 98
        self.assertEqual("Holberton", my_reviewmodel.middle_name)
        self.assertIn("my_number", my_reviewmodel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_reviewmodel = Review()
        rv_dict = my_reviewmodel.to_dict()
        self.assertEqual(str, type(rv_dict["id"]))
        self.assertEqual(str, type(rv_dict["created_at"]))
        self.assertEqual(str, type(rv_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_reviewmodel = Review()
        my_reviewmodel.id = "123456"
        my_reviewmodel.created_at = my_reviewmodel.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'Review',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(my_reviewmodel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_reviewmodel = Review()
        self.assertNotEqual(my_reviewmodel.to_dict(), my_reviewmodel.__dict__)

    def test_to_dict_with_arg(self):
        my_reviewmodel = Review()
        with self.assertRaises(TypeError):
            my_reviewmodel.to_dict(None)

class TestReview_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the Review class."""

    def test_no_args_instantiates(self):
        self.assertEqual(Review, type(Review()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(Review(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(Review().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(Review().updated_at))

    def test_place_id_is_public_class_attribute(self):
        my_reviewmodel = Review()
        self.assertEqual(str, type(Review.place_id))
        self.assertIn("place_id", dir(my_reviewmodel))
        self.assertNotIn("place_id", my_reviewmodel.__dict__)

    def test_user_id_is_public_class_attribute(self):
        my_reviewmodel = Review()
        self.assertEqual(str, type(Review.user_id))
        self.assertIn("user_id", dir(my_reviewmodel))
        self.assertNotIn("user_id", my_reviewmodel.__dict__)

    def test_text_is_public_class_attribute(self):
        my_reviewmodel = Review()
        self.assertEqual(str, type(Review.text))
        self.assertIn("text", dir(my_reviewmodel))
        self.assertNotIn("text", my_reviewmodel.__dict__)

    def test_two_reviews_unique_ids(self):
        rv1 = Review()
        rv2 = Review()
        self.assertNotEqual(rv1.id, rv2.id)

    def test_two_reviews_different_created_at(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.created_at, rv2.created_at)

    def test_two_reviews_different_updated_at(self):
        rv1 = Review()
        sleep(0.05)
        rv2 = Review()
        self.assertLess(rv1.updated_at, rv2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_reviewmodel = Review()
        my_reviewmodel.id = "123456"
        my_reviewmodel.created_at = my_reviewmodel.updated_at = dt
        rvstr = my_reviewmodel.__str__()
        self.assertIn("[Review] (123456)", rvstr)
        self.assertIn("'id': '123456'", rvstr)
        self.assertIn("'created_at': " + dt_repr, rvstr)
        self.assertIn("'updated_at': " + dt_repr, rvstr)

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_reviewmodel = Review(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_reviewmodel.id, "345")
        self.assertEqual(my_reviewmodel.created_at, dt)
        self.assertEqual(my_reviewmodel.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            Review(id=None, created_at=None, updated_at=None)


class TestReview_save(unittest.TestCase):
    """Unittests for testing save method of the Review class."""

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
        my_reviewmodel = Review()
        sleep(0.05)
        first_updated_at = my_reviewmodel.updated_at
        my_reviewmodel.save()
        self.assertLess(first_updated_at, my_reviewmodel.updated_at)

    def test_two_saves(self):
        my_reviewmodel = Review()
        sleep(0.05)
        first_updated_at = my_reviewmodel.updated_at
        my_reviewmodel.save()
        second_updated_at = my_reviewmodel.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_reviewmodel.save()
        self.assertLess(second_updated_at, my_reviewmodel.updated_at)

    def test_save_with_arg(self):
        my_reviewmodel = Review()
        with self.assertRaises(TypeError):
            my_reviewmodel.save(None)

    def test_save_updates_file(self):
        my_reviewmodel = Review()
        my_reviewmodel.save()
        rvid = "Review." + my_reviewmodel.id
        with open("file.json", "r") as f:
            self.assertIn(rvid, f.read())


if __name__ == "__main__":
    unittest.main()
