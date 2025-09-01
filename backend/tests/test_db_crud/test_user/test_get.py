import json
import unittest

import pydantic
from sqlalchemy import func, select
from app import crud, models, schemas, constants
from app.db import get_db, reset_db


# read
class TestDBGetTicket(unittest.TestCase):

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
            with self.subTest(arg=arg):
                if not user_id:
                    self.skipTest("empty users table")
                with self.assertRaises(pydantic.ValidationError):
                    crud.get_user_good(arg, user_id)
            # user id
            with self.subTest(arg=arg):
                with self.assertRaises(pydantic.ValidationError):
                    crud.get_user_good(self.db, arg)

    def test_left_out_of_bound_id(self):
        min_id = self.db.execute(select(func.min(models.User.id))).scalars().first()
        if min_id is None:
            self.skipTest("empty users table")
        result = crud.get_user_good(self.db, min_id - 100)
        self.assertEqual(result, (None, constants.StatusCode.USER_NOT_FOUND))

    def test_right_out_of_bound_id(self):
        max_id = self.db.execute(select(func.max(models.User.id))).scalars().first()
        if max_id is None:
            self.skipTest("empty users table")
        result = crud.get_user_good(self.db, max_id + 100)
        self.assertEqual(result, (None, constants.StatusCode.USER_NOT_FOUND))

    def test_correct_id(self):
        min_id = self.db.execute(select(func.min(models.User.id))).scalars().first()
        max_id = self.db.execute(select(func.max(models.User.id))).scalars().first()
        if min_id is None or max_id is None:
            self.skipTest("empty users table")

        for user_id in [min_id, max_id]:
            with self.subTest(user_id=user_id):
                result = crud.get_user_good(self.db, user_id)
                if not result[0]:
                    self.skipTest(result[1])
                user_dict = schemas.UserOut.model_validate(
                    self.db.get(models.User, user_id)
                ).model_dump()
                for key in user_dict.keys():  # stop sub test if not eq
                    self.assertEqual(
                        (result[0].model_dump()[key], result[1]),
                        (user_dict[key], constants.StatusCode.SUCCESS),
                    )


if __name__ == "__main__":
    unittest.main(verbosity=2)
