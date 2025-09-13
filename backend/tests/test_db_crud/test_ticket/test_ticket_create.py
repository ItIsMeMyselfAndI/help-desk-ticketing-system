import datetime
import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


class TestDBCreateTicket(unittest.TestCase):

    def setUp(self):
        self.db = next(get_db())
        # reset db
        reset_db(bind=self.db.get_bind())
        # sample data
        crud.create_user(
            self.db,
            schemas.UserCreate.model_validate(
                {
                    "username": "user1",
                    "email": "user1@gmail.com",
                    "password": "123",
                    "role": constants.UserRole.CLIENT,
                }
            ),
        )
        crud.create_user(
            self.db,
            schemas.UserCreate.model_validate(
                {
                    "username": "user2",
                    "email": "user2@gmail.com",
                    "password": "123",
                    "role": constants.UserRole.SUPPORT,
                }
            ),
        )
        # test case
        self.test_ticket_dict = {
            "issuer_id": 1,
            "assignee_id": None,
            "title": "Computer won't start after power outage",
            "status": constants.TicketStatus.IN_PROGRESS,
            "category": constants.TicketCategory.HARDWARE,
            "description": "My desktop computer refuses to turn on after yesterday's power outage. The power button doesn't respond at all.",
            "created_at": datetime.datetime.now().astimezone().isoformat(),
            "updated_at": datetime.datetime.now().astimezone().isoformat(),
        }

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        invalid_args = ["lksdjfd", None, 4.8]
        ticket_create = schemas.TicketCreate.model_validate(self.test_ticket_dict)

        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, ticket_create=ticket_create):
                with self.assertRaises(pydantic.ValidationError):
                    crud.create_ticket(arg, ticket_create)
            # ticket basemodel
            with self.subTest(arg=arg, ticket_create=ticket_create):
                with self.assertRaises(pydantic.ValidationError):
                    crud.create_ticket(self.db, arg)

    def test_issuer_not_found(self):
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["issuer_id"] = -100
        ticket_create = schemas.TicketCreate.model_validate(test_ticket_dict)
        _, status_code = crud.create_ticket(self.db, ticket_create)
        self.assertEqual(status_code, constants.StatusCode.ISSUER_NOT_FOUND)

    def test_assignee_not_found(self):
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["assignee_id"] = -100
        ticket_create = schemas.TicketCreate.model_validate(test_ticket_dict)
        _, status_code = crud.create_ticket(self.db, ticket_create)
        self.assertEqual(status_code, constants.StatusCode.ASSIGNEE_NOT_FOUND)

    def test_same_sender_and_receiver(self):
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["issuer_id"] = 1
        test_ticket_dict["assignee_id"] = 1
        ticket_create = schemas.TicketCreate.model_validate(test_ticket_dict)
        _, status_code = crud.create_ticket(self.db, ticket_create)
        self.assertEqual(status_code, constants.StatusCode.SAME_ISSUER_AND_ASSIGNEE)

    def test_with_dates(self):
        ticket_create = schemas.TicketCreate.model_validate(self.test_ticket_dict)
        result_ticket, _ = crud.create_ticket(self.db, ticket_create)
        if not result_ticket:
            self.fail("valid ticket with dates not created")
        result_ticket_dict = result_ticket.as_dict()

        self.assertEqual(
            result_ticket_dict["issuer_id"], self.test_ticket_dict["issuer_id"]
        )
        self.assertEqual(
            result_ticket_dict["assignee_id"], self.test_ticket_dict["assignee_id"]
        )
        self.assertEqual(result_ticket_dict["title"], self.test_ticket_dict["title"])
        self.assertEqual(result_ticket_dict["status"], self.test_ticket_dict["status"])
        self.assertEqual(
            result_ticket_dict["category"], self.test_ticket_dict["category"]
        )
        self.assertEqual(
            result_ticket_dict["description"], self.test_ticket_dict["description"]
        )
        self.assertEqual(
            result_ticket_dict["created_at"], self.test_ticket_dict["created_at"]
        )
        self.assertEqual(
            result_ticket_dict["updated_at"], self.test_ticket_dict["updated_at"]
        )

    def test_without_dates(self):
        test_ticket_dict = self.test_ticket_dict.copy()
        del test_ticket_dict["created_at"]
        del test_ticket_dict["updated_at"]
        ticket_create = schemas.TicketCreate.model_validate(test_ticket_dict)
        result_ticket, _ = crud.create_ticket(self.db, ticket_create)
        if not result_ticket:
            self.fail("valid ticket without dates not created")
        result_ticket_dict = result_ticket.as_dict()

        self.assertEqual(
            result_ticket_dict["issuer_id"], self.test_ticket_dict["issuer_id"]
        )
        self.assertEqual(
            result_ticket_dict["assignee_id"], self.test_ticket_dict["assignee_id"]
        )
        self.assertEqual(result_ticket_dict["title"], self.test_ticket_dict["title"])
        self.assertEqual(result_ticket_dict["status"], self.test_ticket_dict["status"])
        self.assertEqual(
            result_ticket_dict["category"], self.test_ticket_dict["category"]
        )
        self.assertEqual(
            result_ticket_dict["description"], self.test_ticket_dict["description"]
        )

    def test_missing_required_field_on_ticket_create_basemodel(self):
        # issuer id
        test_ticket_dict = self.test_ticket_dict.copy()
        del test_ticket_dict["issuer_id"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # title
        test_ticket_dict = self.test_ticket_dict.copy()
        del test_ticket_dict["title"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # status
        test_ticket_dict = self.test_ticket_dict.copy()
        del test_ticket_dict["status"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # description
        test_ticket_dict = self.test_ticket_dict.copy()
        del test_ticket_dict["description"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)

    def test_invalid_value_on_ticket_create_basemodel(self):
        # issuer id
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["issuer_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # assignee_id
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["assignee_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # title
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["title"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # status
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["status"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # category
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["category"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # description
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["description"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)

    def test_none_in_required_field_on_ticket_create_basemodel(self):
        # issuer id
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["issuer_id"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # title
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["title"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # status
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["status"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)
        # description
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["description"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.TicketCreate.model_validate(test_ticket_dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
