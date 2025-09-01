import datetime
import json
import unittest

import pydantic
from sqlalchemy import select
from app import crud, models, schemas, constants
from app.db import get_db, reset_db


class TestDBUpdateTicket(unittest.TestCase):

    def setUp(self):
        self.db = next(get_db())
        # reset db
        reset_db(bind=self.db.get_bind(), datasets_path="app/datasets.json", limit=1)
        # json datasets
        with open("app/datasets.json", "r") as file:
            self.sample_users = json.load(file)["users"]

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        user_id = self.db.execute(select(models.User.id).limit(1)).scalars().first()
        if not user_id:
            self.skipTest("empty users table")
        invalid_args = ["lksdjfd", None, 4.8]
        user_update = schemas.UserUpdate(
            username="old",
            email="old@gmail.com",
            password="123",
            role=constants.UserRole.CLIENT,
        )
        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, user_id=user_id, user_update=user_update):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_user(arg, user_id, user_update)
            # user id
            with self.subTest(arg=arg, user_id=user_id, user_update=user_update):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_user(self.db, arg, user_update)
            # user basemodel
            with self.subTest(arg=arg, user_id=user_id, user_update=user_update):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_user(self.db, user_id, arg)

    def test_existing_username(self):
        user_id = self.db.execute(select(models.User.id).limit(1)).scalars().first()
        if not user_id:
            self.skipTest("empty users table")
        user_update = schemas.UserUpdate(
            username="old",
            email="old@gmail.com",
            password="123",
            role=constants.UserRole.CLIENT,
        )
        # dummy
        result_1 = crud.update_user(self.db, user_id, user_update)
        if result_1[1] != constants.StatusCode.SUCCESS:
            self.skipTest("dummy user not updated")
        # test
        user_update.email = "new@gmail.com"
        result_2 = crud.update_user(self.db, user_id, user_update)
        self.assertEqual(result_2[1], constants.StatusCode.UNAME_ALREADY_EXIST)

    def test_existing_email(self):
        user_id = self.db.execute(select(models.User.id).limit(1)).scalars().first()
        if not user_id:
            self.skipTest("empty users table")
        user_update = schemas.UserUpdate(
            username="old",
            email="old@gmail.com",
            password="123",
            role=constants.UserRole.CLIENT,
        )
        # dummy
        result_1 = crud.update_user(self.db, user_id, user_update)
        if result_1[1] != constants.StatusCode.SUCCESS:
            self.skipTest("dummy user not updated")
        # test
        user_update.username = "new"
        result_2 = crud.update_user(self.db, user_id, user_update)
        self.assertEqual(result_2[1], constants.StatusCode.EMAIL_ALREADY_EXIST)

    def test_without_dates(self):
        user_id = self.db.execute(select(models.User.id).limit(1)).scalars().first()
        if not user_id:
            self.skipTest("empty users table")
        user_dict = {
            "username": "name",
            "email": "name@gmail.com",
            "password": "123",
            "role": constants.UserRole.SUPPORT,
        }
        user_update = schemas.UserUpdate(**user_dict)
        result = crud.update_user(self.db, user_id, user_update)
        if not result[0]:
            self.fail("valid user with dates not updated")
        del user_dict["password"]  # no password in models.User.as_dict()
        for key in user_dict.keys():  # stop sub test if not eq
            with self.subTest(key=key, result=result):
                self.assertEqual(result[0].as_dict()[key], user_dict[key])

    def test_optional_field_on_user_update_basemodel(self):
        user_id = self.db.execute(select(models.User.id).limit(1)).scalars().first()
        if not user_id:
            self.skipTest("empty users table")
        optional_fields = [
            {"username": "name"},
            {"email": f"name@gmail.com"},
            {"role": constants.UserRole.SUPPORT},
            {"password": "123"},
        ]
        for field in optional_fields:
            with self.subTest(field=field):
                user_update = schemas.UserUpdate.model_validate(field)
                self.assertIsInstance(user_update, schemas.UserUpdate)

    def test_invalid_value_on_user_update_basemodel(self):
        user_id = self.db.execute(select(models.User.id).limit(1)).scalars().first()
        if not user_id:
            self.skipTest("empty users table")
        invalid_value = [1, 2, 3]
        keys = [
            "username",
            "email",
            "role",
            "password",
        ]
        for key in keys:
            with self.subTest(key=key):
                with self.assertRaises(pydantic.ValidationError):
                    schemas.UserUpdate.model_validate({key: invalid_value})

    def test_none_in_optional_field_on_user_update_basemodel(self):
        user_id = self.db.execute(select(models.User.id).limit(1)).scalars().first()
        if not user_id:
            self.skipTest("empty users table")
        keys = [
            "username",
            "email",
            "role",
            "password",
        ]
        for key in keys:
            with self.subTest(key=key):
                user_update = schemas.UserUpdate.model_validate({key: None})
                self.assertIsInstance(user_update, schemas.UserUpdate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
