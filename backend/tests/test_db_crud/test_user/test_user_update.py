import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


class TestDBUpdateUser(unittest.TestCase):

    def setUp(self):
        self.db = next(get_db())
        # reset db
        reset_db(bind=self.db.get_bind())
        self.test_user_dict = {
            "username": "new",
            "email": "new@gmail.com",
            "password": "123",
            "role": constants.UserRole.SUPPORT,
        }
        self.existing_user_dict = {
            "username": "old",
            "email": "old@gmail.com",
            "password": "123",
            "role": constants.UserRole.CLIENT,
        }
        self.existing_user, _ = crud.create_user(
            self.db, schemas.UserCreate.model_validate(self.existing_user_dict)
        )

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        if self.existing_user is None:
            self.skipTest("existing user was not created")
        invalid_args = ["lksdjfd", None, 4.8]
        user_id = self.existing_user.id
        user_update = schemas.UserUpdate.model_validate(self.test_user_dict)

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
        if self.existing_user is None:
            self.skipTest("existing user was not created")
        user_id = self.existing_user.id
        user_update = schemas.UserUpdate.model_validate(self.test_user_dict)
        user_update.username = "old"

        result_user, status_code = crud.update_user(self.db, user_id, user_update)
        self.assertIsNone(result_user, "user w/ existing username was created")
        self.assertEqual(status_code, constants.StatusCode.UNAME_ALREADY_EXIST)

    def test_existing_email(self):
        if self.existing_user is None:
            self.skipTest("existing user was not created")
        user_id = self.existing_user.id
        user_update = schemas.UserUpdate.model_validate(self.test_user_dict)
        user_update.email = "old@gmail.com"

        result_user, status_code = crud.update_user(self.db, user_id, user_update)
        self.assertIsNone(result_user, "user w/ existing email was created")
        self.assertEqual(status_code, constants.StatusCode.EMAIL_ALREADY_EXIST)

    def test_optional_field_on_user_update_basemodel(self):
        if self.existing_user is None:
            self.skipTest("existing user was not created")

        # uname
        user_update = schemas.UserUpdate.model_validate({"username": "new"})
        self.assertIsInstance(user_update, schemas.UserUpdate)
        # email
        user_update = schemas.UserUpdate.model_validate({"email": "new@gmail.com"})
        self.assertIsInstance(user_update, schemas.UserUpdate)
        # pass
        user_update = schemas.UserUpdate.model_validate({"password": "123"})
        self.assertIsInstance(user_update, schemas.UserUpdate)
        # role
        user_update = schemas.UserUpdate.model_validate(
            {"role": constants.UserRole.SUPPORT}
        )
        self.assertIsInstance(user_update, schemas.UserUpdate)

    def test_invalid_value_on_user_update_basemodel(self):
        # uname
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["username"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserUpdate.model_validate(test_user_dict)
        # email
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["email"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserUpdate.model_validate(test_user_dict)
        # pass
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["password"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserUpdate.model_validate(test_user_dict)
        # role
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["role"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.UserUpdate.model_validate(test_user_dict)

    def test_none_in_optional_field_on_user_update_basemodel(self):
        # uname
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["username"] = None
        user_update = schemas.UserUpdate.model_validate(test_user_dict)
        self.assertIsInstance(user_update, schemas.UserUpdate)
        # email
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["email"] = None
        user_update = schemas.UserUpdate.model_validate(test_user_dict)
        self.assertIsInstance(user_update, schemas.UserUpdate)
        # pass
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["password"] = None
        user_update = schemas.UserUpdate.model_validate(test_user_dict)
        self.assertIsInstance(user_update, schemas.UserUpdate)
        # role
        test_user_dict = self.test_user_dict.copy()
        test_user_dict["role"] = None
        user_update = schemas.UserUpdate.model_validate(test_user_dict)
        self.assertIsInstance(user_update, schemas.UserUpdate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
