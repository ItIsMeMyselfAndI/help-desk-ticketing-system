import datetime
import json
import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


class TestDBCreateTicket(unittest.TestCase):

    def setUp(self):
        self.db = next(get_db())
        # reset db
        reset_db(bind=self.db.get_bind())
        # json datasets
        with open("app/datasets.json", "r") as file:
            self.sample_users = json.load(file)["users"]

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        invalid_args = ["lksdjfd", None, 4.8]
        user_create = schemas.UserCreate(
            username="old",
            email="old@gmail.com",
            password="123",
            role=constants.UserRole.CLIENT,
        )
        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, user_create=user_create):
                with self.assertRaises(pydantic.ValidationError):
                    crud.create_user(arg, user_create)
            # user basemodel
            with self.subTest(arg=arg, user_create=user_create):
                with self.assertRaises(pydantic.ValidationError):
                    crud.create_user(self.db, arg)

    def test_existing_username(self):
        user_create = schemas.UserCreate(
            username="old",
            email="old@gmail.com",
            password="123",
            role=constants.UserRole.CLIENT,
        )
        # dummy
        result_1 = crud.create_user(self.db, user_create)
        if result_1[1] != constants.StatusCode.SUCCESS:
            self.skipTest("dummy user not created")
        # test
        user_create.email = "new@gmail.com"
        result_2 = crud.create_user(self.db, user_create)
        self.assertEqual(result_2[1], constants.StatusCode.UNAME_ALREADY_EXIST)

    def test_existing_email(self):
        user_create = schemas.UserCreate(
            username="old",
            email="old@gmail.com",
            password="123",
            role=constants.UserRole.CLIENT,
        )
        # dummy
        result_1 = crud.create_user(self.db, user_create)
        if result_1[1] != constants.StatusCode.SUCCESS:
            self.skipTest("dummy user not created")
        # test
        user_create.username = "new"
        result_2 = crud.create_user(self.db, user_create)
        self.assertEqual(result_2[1], constants.StatusCode.EMAIL_ALREADY_EXIST)

    def test_with_dates(self):
        user_dict = {
            "username": "name",
            "email": "name@gmail.com",
            "password": "123",
            "role": constants.UserRole.SUPPORT,
            "created_at": datetime.datetime.now().astimezone().isoformat(),
            "updated_at": datetime.datetime.now().astimezone().isoformat(),
        }
        user_create = schemas.UserCreate(**user_dict)
        result = crud.create_user(self.db, user_create)
        if not result[0]:
            self.fail("valid user with dates not created")
        del user_dict["password"]  # no password in models.User.as_dict()
        for key in user_dict.keys():  # stop sub test if not eq
            self.assertEqual(result[0].as_dict()[key], user_dict[key])

    def test_without_dates(self):
        user_dict = {
            "username": "name",
            "email": "name@gmail.com",
            "password": "123",
            "role": constants.UserRole.SUPPORT,
        }
        user_create = schemas.UserCreate(**user_dict)
        result = crud.create_user(self.db, user_create)
        if not result[0]:
            self.fail("valid user with dates not created")
        del user_dict["password"]  # no password in models.User.as_dict()
        for key in user_dict.keys():  # stop sub test if not eq
            self.assertEqual(result[0].as_dict()[key], user_dict[key])

    def test_missing_field_on_user_create_basemodel(self):
        user_dict = {
            "username": "name",
            "email": f"name@gmail.com",
            "role": constants.UserRole.SUPPORT,
            "password": "123",
        }
        for key in user_dict.keys():
            with self.subTest(key=key, user_dict=user_dict):
                user_dict_copy = user_dict.copy()
                del user_dict_copy[key]
                with self.assertRaises(pydantic.ValidationError):
                    schemas.UserCreate.model_validate(user_dict_copy)

    def test_invalid_value_on_user_create_basemodel(self):
        invalid_value = [1, 2, 3]
        user_dict = {
            "username": "name",
            "email": f"name@gmail.com",
            "role": constants.UserRole.SUPPORT,
            "password": "123",
            "created_at": datetime.datetime.now().astimezone().isoformat(),
        }
        for key in user_dict.keys():
            with self.subTest(
                key=key, user_dict=user_dict, invalid_value=invalid_value
            ):
                user_dict_copy = user_dict.copy()
                user_dict_copy.update({key: invalid_value})
                with self.assertRaises(pydantic.ValidationError):
                    schemas.UserCreate.model_validate(user_dict_copy)

    def test_none_in_required_field_on_user_create_basemodel(self):
        user_dict = {
            "username": "name",
            "email": f"name@gmail.com",
            "role": constants.UserRole.SUPPORT,
            "password": "123",
        }
        for key in user_dict.keys():
            with self.subTest(key=key, user_dict=user_dict):
                user_dict_copy = user_dict.copy()
                user_dict_copy.update({key: None})
                with self.assertRaises(pydantic.ValidationError):
                    schemas.UserCreate.model_validate(user_dict_copy)


if __name__ == "__main__":
    unittest.main(verbosity=2)
