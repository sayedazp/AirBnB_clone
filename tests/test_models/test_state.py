#!/usr/bin/python3
"""Defines unittests for models/state.py.

Unittest classes:
    TestState_instantiation
    TestState_save
    TestState_to_dict
"""
import os
import models
import unittest
from datetime import datetime
from time import sleep
from models.state import State


class TestState_to_dict(unittest.TestCase):
    """Unittests for testing to_dict method of the State class."""

    def test_to_dict_type(self):
        self.assertTrue(dict, type(State().to_dict()))

    def test_to_dict_contains_correct_keys(self):
        my_statemodel = State()
        self.assertIn("id", my_statemodel.to_dict())
        self.assertIn("created_at", my_statemodel.to_dict())
        self.assertIn("updated_at", my_statemodel.to_dict())
        self.assertIn("__class__", my_statemodel.to_dict())

    def test_to_dict_contains_added_attributes(self):
        my_statemodel = State()
        my_statemodel.middle_name = "Holberton"
        my_statemodel.my_number = 98
        self.assertEqual("Holberton", my_statemodel.middle_name)
        self.assertIn("my_number", my_statemodel.to_dict())

    def test_to_dict_datetime_attributes_are_strs(self):
        my_statemodel = State()
        st_dict = my_statemodel.to_dict()
        self.assertEqual(str, type(st_dict["id"]))
        self.assertEqual(str, type(st_dict["created_at"]))
        self.assertEqual(str, type(st_dict["updated_at"]))

    def test_to_dict_output(self):
        dt = datetime.today()
        my_statemodel = State()
        my_statemodel.id = "123456"
        my_statemodel.created_at = my_statemodel.updated_at = dt
        tdict = {
            'id': '123456',
            '__class__': 'State',
            'created_at': dt.isoformat(),
            'updated_at': dt.isoformat(),
        }
        self.assertDictEqual(my_statemodel.to_dict(), tdict)

    def test_contrast_to_dict_dunder_dict(self):
        my_statemodel = State()
        self.assertNotEqual(my_statemodel.to_dict(), my_statemodel.__dict__)

    def test_to_dict_with_arg(self):
        my_statemodel = State()
        with self.assertRaises(TypeError):
            my_statemodel.to_dict(None)

class TestState_instantiation(unittest.TestCase):
    """Unittests for testing instantiation of the State class."""

    def test_no_args_instantiates(self):
        self.assertEqual(State, type(State()))

    def test_new_instance_stored_in_objects(self):
        self.assertIn(State(), models.storage.all().values())

    def test_id_is_public_str(self):
        self.assertEqual(str, type(State().id))

    def test_created_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().created_at))

    def test_updated_at_is_public_datetime(self):
        self.assertEqual(datetime, type(State().updated_at))

    def test_name_is_public_class_attribute(self):
        my_statemodel = State()
        self.assertEqual(str, type(State.name))
        self.assertIn("name", dir(my_statemodel))
        self.assertNotIn("name", my_statemodel.__dict__)

    def test_two_states_unique_ids(self):
        st1 = State()
        st2 = State()
        self.assertNotEqual(st1.id, st2.id)

    def test_two_states_different_created_at(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.created_at, st2.created_at)

    def test_two_states_different_updated_at(self):
        st1 = State()
        sleep(0.05)
        st2 = State()
        self.assertLess(st1.updated_at, st2.updated_at)

    def test_str_representation(self):
        dt = datetime.today()
        dt_repr = repr(dt)
        my_statemodel = State()
        my_statemodel.id = "123456"
        my_statemodel.created_at = my_statemodel.updated_at = dt
        ststr = my_statemodel.__str__()
        self.assertIn("[State] (123456)", ststr)
        self.assertIn("'id': '123456'", ststr)
        self.assertIn("'created_at': " + dt_repr, ststr)
        self.assertIn("'updated_at': " + dt_repr, ststr)

    # def test_args_unused(self):
    #     my_statemodel = State(None)
    #     self.assertNotIn(None, my_statemodel.__dict__.values())

    def test_instantiation_with_kwargs(self):
        dt = datetime.today()
        dt_iso = dt.isoformat()
        my_statemodel = State(id="345", created_at=dt_iso, updated_at=dt_iso)
        self.assertEqual(my_statemodel.id, "345")
        self.assertEqual(my_statemodel.created_at, dt)
        self.assertEqual(my_statemodel.updated_at, dt)

    def test_instantiation_with_None_kwargs(self):
        with self.assertRaises(TypeError):
            State(id=None, created_at=None, updated_at=None)


class TestState_save(unittest.TestCase):
    """Unittests for testing save method of the State class."""

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
        my_statemodel = State()
        sleep(0.05)
        first_updated_at = my_statemodel.updated_at
        my_statemodel.save()
        self.assertLess(first_updated_at, my_statemodel.updated_at)

    def test_two_saves(self):
        my_statemodel = State()
        sleep(0.05)
        first_updated_at = my_statemodel.updated_at
        my_statemodel.save()
        second_updated_at = my_statemodel.updated_at
        self.assertLess(first_updated_at, second_updated_at)
        sleep(0.05)
        my_statemodel.save()
        self.assertLess(second_updated_at, my_statemodel.updated_at)

    def test_save_with_arg(self):
        my_statemodel = State()
        with self.assertRaises(TypeError):
            my_statemodel.save(None)

    def test_save_updates_file(self):
        my_statemodel = State()
        my_statemodel.save()
        stid = "State." + my_statemodel.id
        with open("file.json", "r") as f:
            self.assertIn(stid, f.read())


if __name__ == "__main__":
    unittest.main()
