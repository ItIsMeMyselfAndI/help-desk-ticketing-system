import json
import re
import unittest

import pydantic
from sqlalchemy import func, select
from app import crud, models, schemas, constants
from app import db
from app.db import get_db, reset_db


# read
class TestDBDeleteTicket(unittest.TestCase):

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

    def test_invalid_id(self):
        invalid_args = ["lksdjfd", None, 4.8]
        user_id = self.db.execute(select(models.User.id).limit(1)).scalars().first()
        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, user_id=user_id):
                if not user_id:
                    self.skipTest("empty users table")
                with self.assertRaises(pydantic.ValidationError):
                    crud.delete_user(arg, user_id)
            # user id
            with self.subTest(arg=arg, user_id=user_id):
                with self.assertRaises(pydantic.ValidationError):
                    crud.delete_user(self.db, arg)

    def test_left_out_of_bound_id(self):
        min_id = self.db.execute(select(func.min(models.User.id))).scalars().first()
        if min_id is None:
            self.skipTest("empty users table")
        result = crud.delete_user(self.db, min_id - 100)
        self.assertEqual(result, (None, constants.StatusCode.USER_NOT_FOUND))

    def test_right_out_of_bound_id(self):
        max_id = self.db.execute(select(func.max(models.User.id))).scalars().first()
        if max_id is None:
            self.skipTest("empty users table")
        result = crud.delete_user(self.db, max_id + 100)
        self.assertEqual(result, (None, constants.StatusCode.USER_NOT_FOUND))

    def test_correct_id(self):
        user_id = self.db.execute(select(models.User.id)).scalars().first()
        if not user_id:
            self.skipTest("empty users table")

        db_user_raw = self.db.get(models.User, user_id)
        self.assertIsNotNone(db_user_raw, "empty users table")
        db_user = schemas.UserOut.model_validate(db_user_raw)

        result = crud.delete_user(self.db, user_id)
        self.assertIsNotNone(result[0], "empty users table")
        del_user = schemas.UserOut.model_validate(result[0])

        self.assertEqual(del_user.model_dump(), db_user.model_dump())


if __name__ == "__main__":
    unittest.main(verbosity=2)
