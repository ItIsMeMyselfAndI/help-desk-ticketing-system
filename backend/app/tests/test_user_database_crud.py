import datetime
import json
import unittest

import pydantic_core
from sqlalchemy import func, select
from app import crud, models, schemas, constants
from app.db import get_db, reset_db


# create
class TestCreateTicketDB(unittest.TestCase):

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
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.subTest(i=i, role=role):
                user_dict = {
                    "username": f"name{i}",
                    "email": f"name{i}@gmail.com",
                    "password": "123",
                    "role": role,
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
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.subTest(i=i, role=role):
                user_dict = {
                    "username": f"name{i}",
                    "email": f"name{i}@gmail.com",
                    "password": "123",
                    "role": role,
                }
                user_create = schemas.UserCreate(**user_dict)
                result = crud.create_user(self.db, user_create)
                if not result[0]:
                    self.fail("valid user with dates not created")
                del user_dict["password"]  # no password in models.User.as_dict()
                for key in user_dict.keys():  # stop sub test if not eq
                    self.assertEqual(result[0].as_dict()[key], user_dict[key])

    def test_missing_username(self):
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.subTest(i=i, role=role):
                with self.assertRaises(pydantic_core.ValidationError):
                    schemas.UserCreate.model_validate(
                        {
                            "email": f"name{i}@gmail.com",
                            "role": role,
                            "password": "123",
                        }
                    )

    def test_missing_email(self):
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.subTest(i=i, role=role):
                with self.assertRaises(pydantic_core.ValidationError):
                    schemas.UserCreate.model_validate(
                        {
                            "username": f"name{i}",
                            "role": role,
                            "password": "123",
                        }
                    )

    def test_missing_password(self):
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.subTest(i=i, role=role):
                with self.assertRaises(pydantic_core.ValidationError):
                    schemas.UserCreate.model_validate(
                        {
                            "username": f"name{i}",
                            "email": f"name{i}@gmail.com",
                            "role": role,
                        }
                    )

    def test_invalid_role(self):
        roles = ["CLIENT", "SUPPORT", "ADMIN"]
        for i, role in enumerate(roles):
            with self.subTest(i=i, role=role):
                with self.assertRaises(pydantic_core.ValidationError):
                    schemas.UserCreate.model_validate(
                        {
                            "username": f"name{i}",
                            "email": f"name{i}@gmail.com",
                            "role": role,
                            "password": "123",
                        }
                    )

    def test_none_required_field(self):
        user_dict_list = [
            {
                "username": None,
                "email": "name@gmail.com",
                "role": constants.UserRole.CLIENT,
                "password": "123",
            },
            {
                "username": "name",
                "email": None,
                "role": constants.UserRole.CLIENT,
                "password": "123",
            },
            {
                "username": "name",
                "email": "name@gmail.com",
                "role": constants.UserRole.CLIENT,
                "password": None,
            },
        ]
        for user_dict in user_dict_list:
            with self.subTest(user_dict=user_dict):
                with self.assertRaises(pydantic_core.ValidationError):
                    schemas.UserCreate.model_validate(user_dict)


# @unittest.skip("get ticket tests")
# read
class TestGetTicketDB(unittest.TestCase):

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

    @unittest.skip("TODO: catch invalid arg type")
    def test_invalid_type_id(self):
        invalid_type_ids = ["lksdjfd", None, 4.8]
        for id in invalid_type_ids:
            with self.subTest(id=id):
                with self.assertRaises(TypeError):
                    crud.get_user_good(self.db, id)

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
