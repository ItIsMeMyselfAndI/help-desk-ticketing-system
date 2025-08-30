import datetime
import json
from sys import modules
import unittest
from time import sleep

from pydantic import EmailStr
import pydantic_core
from sqlalchemy import func, select
import sqlalchemy
from app import crud, models, schemas, constants
from app.db import drop_db, get_db, init_db


# create
class TestCreateTicketDB(unittest.TestCase):

    def setUp(self):
        self.sample_users = self.__get_sample_users()
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

    def tearDown(self):
        pass

    def test_existing_username(self):
        username = (
            self.db.execute(select(models.User.username).limit(1)).scalars().first()
        )
        if not username:
            self.skipTest("empty users table")
        user_create = schemas.UserCreate(
            username=username,
            email="new@gmail.com",
            password="123",
            role=constants.UserRole.CLIENT,
        )
        user_entity, status_code = crud.create_user(self.db, user_create)
        if user_entity:
            self.fail("unintended user creation")
        self.assertEqual(status_code, constants.StatusCode.UNAME_ALREADY_EXIST)

    def test_existing_email(self):
        email = self.db.execute(select(models.User.email).limit(1)).scalars().first()
        if not email:
            self.skipTest("empty users table")
        user_create = schemas.UserCreate(
            username="hello",
            email=email,
            password="123",
            role=constants.UserRole.CLIENT,
        )
        user_entity, status_code = crud.create_user(self.db, user_create)
        if user_entity:
            self.fail("unintended user creation")
        self.assertEqual(status_code, constants.StatusCode.EMAIL_ALREADY_EXIST)

    def test_with_dates(self):
        user_create_list = []
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            user_create_list.append(
                schemas.UserCreate(
                    email=f"{self.available_unames[i]}@gmail.com",
                    username=self.available_unames[i],
                    role=role,
                    password="123",
                )
            )
        for user_create in user_create_list:
            with self.subTest(user_create=user_create):
                user_entity, status_code = crud.create_user(self.db, user_create)
                if not user_entity:
                    self.fail(status_code)
                db_user_entity = self.db.get(models.User, user_entity.id)
                if not db_user_entity:
                    self.fail(status_code)
                user_dict = user_entity.as_dict()
                db_user_dict = db_user_entity.as_dict()
                self.assertEqual(
                    (user_dict, status_code),
                    (db_user_dict, constants.StatusCode.SUCCESS),
                )

    def test_without_dates(self):
        user_create_list = []
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            user_create_list.append(
                schemas.UserCreate(
                    email=f"{self.available_unames[i]}@gmail.com",
                    username=self.available_unames[i],
                    role=role,
                    password="123",
                )
            )
        for user_create in user_create_list:
            with self.subTest(user_create=user_create):
                user_entity, status_code = crud.create_user(self.db, user_create)
                if not user_entity:
                    self.fail(status_code)
                db_user_entity = self.db.get(models.User, user_entity.id)
                if not db_user_entity:
                    self.fail(status_code)
                user_dict = user_entity.as_dict()
                db_user_dict = db_user_entity.as_dict()
                self.assertEqual(
                    (user_dict, status_code),
                    (db_user_dict, constants.StatusCode.SUCCESS),
                )

    def test_missing_username(self):
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.assertRaises(pydantic_core.ValidationError):
                schemas.UserCreate(
                    email=f"{self.available_unames[i]}@gmail.com",
                    role=role,
                    password="123",
                )

    def test_missing_email(self):
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.assertRaises(pydantic_core.ValidationError):
                schemas.UserCreate(
                    username=self.available_unames[i],
                    role=role,
                    password="123",
                )

    def test_missing_email(self):
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.assertRaises(pydantic_core.ValidationError):
                schemas.UserCreate(
                    email=f"{self.available_unames[i]}@gmail.com",
                    username=self.available_unames[i],
                    role=role,
                )

    def test_invalid_role(self):
        roles = ["CLIENT", "SUPPORT", "ADMIN"]
        for i, role in enumerate(roles):
            with self.assertRaises(pydantic_core.ValidationError):
                schemas.UserCreate(
                    email=f"{self.available_unames[i]}@gmail.com",
                    username=self.available_unames[i],
                    role=role,
                    password="123",
                )

    def test_none_required_field(self):
        roles = [
            constants.UserRole.CLIENT,
            constants.UserRole.SUPPORT,
            constants.UserRole.ADMIN,
        ]
        for i, role in enumerate(roles):
            with self.assertRaises(pydantic_core.ValidationError):
                schemas.UserCreate(
                    email=None,
                    username=self.available_unames[i],
                    role=role,
                    password="123",
                )


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
    unittest.main()
