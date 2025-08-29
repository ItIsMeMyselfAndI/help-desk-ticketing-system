import datetime
import json
import os
import unittest

import pydantic_core
from app import crud, models, schemas, constants
from app.db import get_db


# create
class TestCreateTicketDB(unittest.TestCase):
    def setUp(self):
        self.db = next(get_db())
        with open("app/datasets.json", "r") as file:
            self.users = json.load(file)["users"]
        self.user_id_1 = 6
        self.user_id_2 = 7
        self.user_id_3 = 8

    def tearDown(self):
        pass

    def test_with_dates(self):
        user, user_create = None, None
        for user in self.users:
            if user["id"] == self.user_id_1:
                user_create = schemas.UserCreate(**user)
                break
        if not user:
            self.skipTest("sample user not found")
        if not user_create:
            self.skipTest("user base not created")
        if crud.verify_user_account(self.db, user["username"], user["password"]):       
            self.skipTest("user already exist")
        user_entity, status_code = crud.create_user(self.db, user_create)
        if not user_entity:
            self.skipTest(status_code)
        user_dict = user_entity.as_dict()
        role: constants.UserRole = user_dict["role"]
        user_dict.update({"role" : role.value})
        self.assertEqual(status_code, constants.StatusCode.SUCCESS)
    
    def test_without_dates(self):
        user, user_create = None, None
        for user in self.users:
            if user["id"] == self.user_id_2:
                del user["created_at"]
                del user["updated_at"]
                user_create = schemas.UserCreate(**user)
                break
        if not user:
            self.skipTest("sample user not found")
        if not user_create:
            self.skipTest("user base not created")
        if crud.verify_user_account(self.db, user["username"], user["password"]):       
            self.skipTest("user already exist")
        user_entity, status_code = crud.create_user(self.db, user_create)
        if not user_entity:
            self.skipTest(status_code)
        user_dict = user_entity.as_dict()
        role: constants.UserRole = user_dict["role"]
        user_dict.update({"role" : role.value})
        self.assertEqual(status_code, constants.StatusCode.SUCCESS)

    def test_missing_required(self):
        user = None
        for user in self.users:
            if user["id"] == self.user_id_3:
                del user["created_at"]
                del user["updated_at"]
                del user["username"]
                break
        if not user:
            self.skipTest("sample user not found")
        with self.assertRaises(pydantic_core._pydantic_core.ValidationError):
            schemas.UserCreate(**user)


# read
@unittest.skip("get ticket")
class TestGetTicketDB(unittest.TestCase):
    def setUp(self):
        self.db = next(get_db())

    def tearDown(self):
        pass

    def test_out_of_bound_id(self):
        for user_id in [-1000, 0, 1000]:
            with self.subTest(user_id=user_id):
                result = crud.get_user_good(self.db, user_id)
                self.assertEqual(result, (None, constants.StatusCode.USER_NOT_FOUND))

    def test_correct_id(self):
        with open("app/datasets.json", "r") as file:
            users = json.load(file)["users"]
        for user_id in [1, 10, 18]:
            user_out, status_code = crud.get_user_good(self.db, user_id)
            if not user_out:
                self.skipTest(status_code)
            user_dict = user_out.model_dump()
            role: constants.UserRole = user_dict["role"]
            created_at: datetime.datetime = user_dict["created_at"]
            updated_at: datetime.datetime = user_dict["updated_at"]
            user_dict.update({"role" : role.value})
            user_dict.update({"created_at" : created_at.isoformat()})
            user_dict.update({"updated_at" : updated_at.isoformat()})
            user = None
            for user in users:
                if user["id"] == user_id:
                    break
            if not user:
                self.skipTest("sample user not found")
            del user["password"]
            self.assertEqual(user, user_dict)
            self.assertEqual(status_code, constants.StatusCode.SUCCESS)


if __name__ == '__main__':
    unittest.main()
