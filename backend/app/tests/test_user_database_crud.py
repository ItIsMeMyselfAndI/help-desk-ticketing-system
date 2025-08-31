import datetime
import json
import unittest

from pydantic import EmailStr
import pydantic_core
from sqlalchemy import delete, func, select
from sqlalchemy.sql.functions import user
from app import crud, models, schemas, constants
from app.db import engine, drop_db, get_db, init_db


# create
class TestCreateTicketDB(unittest.TestCase):

    def setUp(self):
        # Ensure all sessions are closed first
        self.db = next(get_db())
        self.db.execute(delete(models.User))
        self.db.commit()
        with open("app/datasets.json", "r") as file:
            self.sample_users = json.load(file)["users"]

    def tearDown(self):
        pass

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
                    self.assertEqual(user_dict[key], result[0].as_dict()[key])

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
                    self.assertEqual(user_dict[key], result[0].as_dict()[key])

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


@unittest.skip("get ticket tests")
# read
class TestGetTicketDB(unittest.TestCase):
    def setUp(self):
        self.sample_users = self.__get_sample_users()
        self.max_id, self.min_id = self.__get_min_and_max_id()
        self.available_unames = self.__get_available_unames()
        self.db = next(get_db())

    def __get_sample_users(self):
        with open("app/datasets.json", "r") as file:
            users = json.load(file)["users"]
        if not users:
            self.fail("empty sample users")
        return users

    def __get_available_unames(self):
        db = next(get_db())
        usernames = []
        for user in self.sample_users:
            uname = db.execute(
                select(models.User.username).where(
                    models.User.username == user["username"]
                )
            ).first()
            if not uname:
                usernames.append(user["username"])
        if not usernames:
            self.skipTest("empty users table")
        return usernames

    def __get_min_and_max_id(self):
        db = next(get_db())
        max_id = db.execute(select(func.max(models.User.id))).scalars().first()
        min_id = db.execute(select(func.min(models.User.id))).scalars().first()
        if not max_id or not min_id:
            self.skipTest("empty users table")
        return max_id, min_id

    def tearDown(self):
        pass

    def test_left_out_of_bound_id(self):
        result = crud.get_user_good(self.db, self.min_id - 100)
        self.assertEqual(result, (None, constants.StatusCode.USER_NOT_FOUND))

    def test_right_out_of_bound_id(self):
        result = crud.get_user_good(self.db, self.max_id + 100)
        self.assertEqual(result, (None, constants.StatusCode.USER_NOT_FOUND))

    # TODO-2: fix invalid type args
    def test_invalid_type_id(self):
        invalid_type_ids = ["lksdjfd", None, 4.8]
        for id in invalid_type_ids:
            with self.subTest(id=id):
                crud.get_user_good(self.db, id)

    def test_correct_id(self):
        for user_id in [self.min_id, self.max_id]:
            user_out, status_code = crud.get_user_good(self.db, user_id)
            if not user_out:
                self.skipTest(status_code)
            db_user_dict = user_out.model_dump()
            email: EmailStr = db_user_dict["email"]
            role: constants.UserRole = db_user_dict["role"]
            created_at: datetime.datetime = db_user_dict["created_at"]
            updated_at: datetime.datetime = db_user_dict["updated_at"]
            db_user_dict.update(
                {
                    "email": email,
                    "role": role.value,
                    "created_at": created_at.isoformat(),
                    "updated_at": updated_at.isoformat(),
                }
            )
            sample_user_dict = None
            for sample_user_dict in self.sample_users:
                if sample_user_dict["username"] == db_user_dict["username"]:
                    break
            if not sample_user_dict:
                self.skipTest("sample user not found")
            self.assertEqual(
                (sample_user_dict, status_code),
                (db_user_dict, constants.StatusCode.SUCCESS),
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
