import datetime
import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


class TestDBCreateUser(unittest.TestCase):

    def setUp(self):
        self.db = next(get_db())
        # reset db
        reset_db(bind=self.db.get_bind())
        self.test_user_dict = {
            "username": "old",
            "email": "old@gmail.com",
            "password": "123",
            "role": constants.UserRole.CLIENT,
            "created_at": datetime.datetime.now().astimezone().isoformat(),
            "updated_at": datetime.datetime.now().astimezone().isoformat(),
        }

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        invalid_args = ["lksdjfd", None, 4.8]
        user_create = schemas.UserCreate.model_validate(self.test_user_dict)

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
        user_create = schemas.UserCreate.model_validate(self.test_user_dict)
        # dummy
        existing_user, _ = crud.create_user(self.db, user_create)
        if existing_user is None:
            self.skipTest("dummy user not created")
        # test
        user_create.email = "new@gmail.com"
        result_user, status_code = crud.create_user(self.db, user_create)
        self.assertIsNone(result_user)
        self.assertEqual(status_code, constants.StatusCode.UNAME_ALREADY_EXIST)

    def test_existing_email(self):
        user_create = schemas.UserCreate.model_validate(self.test_user_dict)
        # dummy
        existing_user, _ = crud.create_user(self.db, user_create)
        if existing_user is None:
            self.skipTest("dummy user not created")
        # test
        user_create.username = "new"
        result_user, status_code = crud.create_user(self.db, user_create)
        self.assertIsNone(result_user)
        self.assertEqual(status_code, constants.StatusCode.EMAIL_ALREADY_EXIST)

    def test_with_dates(self):
        user_create = schemas.UserCreate.model_validate(self.test_user_dict)
        result_user, _ = crud.create_user(self.db, user_create)
        if not result_user:
            self.fail("valid user with dates not created")
        result_user_dict = result_user.as_dict()

        self.assertEqual(result_user_dict["username"], self.test_user_dict["username"])
        self.assertEqual(result_user_dict["email"], self.test_user_dict["email"])
        self.assertEqual(result_user_dict["role"], self.test_user_dict["role"])
        self.assertEqual(
            result_user_dict["created_at"], self.test_user_dict["created_at"]
        )
        self.assertEqual(
            result_user_dict["updated_at"], self.test_user_dict["updated_at"]
        )

    def test_without_dates(self):
        test_user_dict = self.test_user_dict.copy()
        del test_user_dict["created_at"]
        del test_user_dict["updated_at"]
        user_create = schemas.UserCreate.model_validate(test_user_dict)
        result_user, _ = crud.create_user(self.db, user_create)
        if not result_user:
            self.fail("valid user without dates not created")
        result_user_dict = result_user.as_dict()

        self.assertEqual(result_user_dict["username"], self.test_user_dict["username"])
        self.assertEqual(result_user_dict["email"], self.test_user_dict["email"])
        self.assertEqual(result_user_dict["role"], self.test_user_dict["role"])

    def test_missing_required_field_on_user_create_basemodel(self):
        # uname
        test_user_dict = self.test_user_dict.copy()
        del test_user_dict["username"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # email
        test_user_dict = self.test_user_dict.copy()
        del test_user_dict["email"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # pass
        test_user_dict = self.test_user_dict.copy()
        del test_user_dict["password"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # role
        test_user_dict = self.test_user_dict.copy()
        del test_user_dict["role"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)

    def test_invalid_value_on_user_create_basemodel(self):
        # uname
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["username"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # email
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["email"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # pass
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["password"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # role
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["role"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)

    def test_none_in_required_field_on_user_create_basemodel(self):
        # uname
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["username"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # email
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["email"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # pass
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["password"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)
        # role
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["role"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserCreate.model_validate(test_user_dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
