import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


# read
class TestDBDeleteTicket(unittest.TestCase):

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

    def test_invalid_id(self):
        if self.existing_user is None:
            self.skipTest("existing user was not created")
        user_id = self.existing_user.id

        invalid_args = ["lksdjfd", None, 4.8]
        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, user_id=user_id):
                if not user_id:
                    self.skipTest("empty users table")
                with self.assertRaises(pydantic.ValidationError):
                    crud.delete_user(arg, user_id)
            # user id
            with self.subTest(arg=arg):
                with self.assertRaises(pydantic.ValidationError):
                    crud.delete_user(self.db, arg)

    def test_left_out_of_bound_id(self):
        if self.existing_user is None:
            self.skipTest("existing user was not created")
        user_id = self.existing_user.id

        result_user, status_code = crud.delete_user(self.db, user_id - 100)
        self.assertIsNone(result_user)
        self.assertEqual(status_code, constants.StatusCode.USER_NOT_FOUND)

    def test_right_out_of_bound_id(self):
        if self.existing_user is None:
            self.skipTest("existing user was not created")
        user_id = self.existing_user.id

        result_user, status_code = crud.delete_user(self.db, user_id + 100)
        self.assertIsNone(result_user)
        self.assertEqual(status_code, constants.StatusCode.USER_NOT_FOUND)

    def test_correct_id(self):
        if self.existing_user is None:
            self.skipTest("existing user was not created")
        user_id = self.existing_user.id

        result_user, _ = crud.delete_user(self.db, user_id)
        if result_user is None:
            self.fail("delete user failed")
        result_user_dict = result_user.as_dict()

        self.assertEqual(
            result_user_dict["username"], self.existing_user_dict["username"]
        )
        self.assertEqual(result_user_dict["email"], self.existing_user_dict["email"])
        self.assertEqual(result_user_dict["role"], self.existing_user_dict["role"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
