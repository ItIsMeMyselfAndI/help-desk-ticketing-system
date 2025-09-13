import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


class TestDBUpdateUser(unittest.TestCase):

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
        # existing ticket
        self.existing_ticket_dict = {
            "issuer_id": 1,
            "assignee_id": None,
            "title": "My application is laggy",
            "status": constants.TicketStatus.OPEN,
            "category": constants.TicketCategory.SOFTWARE,
            "description": "My application freezes on start up",
        }
        self.existing_ticket, _ = crud.create_ticket(
            self.db,
            schemas.TicketCreate.model_validate(self.existing_ticket_dict),
        )
        # test case
        self.test_ticket_dict = {
            "issuer_id": 1,
            "assignee_id": None,
            "title": "Computer won't start after power outage",
            "status": constants.TicketStatus.IN_PROGRESS,
            "category": constants.TicketCategory.HARDWARE,
            "description": "My desktop computer refuses to turn on after yesterday's power outage. The power button doesn't respond at all.",
        }

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        if self.existing_ticket is None:
            self.skipTest("existing ticket was not created")
        invalid_args = ["lksdjfd", None, 4.8]
        ticket_id = self.existing_ticket.id
        ticket_update = schemas.TicketUpdate.model_validate(self.test_ticket_dict)

        for arg in invalid_args:
            # db session
            with self.subTest(
                arg=arg, ticket_id=ticket_id, ticket_update=ticket_update
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_ticket(arg, ticket_id, ticket_update)
            # ticket id
            with self.subTest(
                arg=arg, ticket_id=ticket_id, ticket_update=ticket_update
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_ticket(self.db, arg, ticket_update)
            # ticket basemodel
            with self.subTest(
                arg=arg, ticket_id=ticket_id, ticket_update=ticket_update
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_ticket(self.db, ticket_id, arg)

    def test_issuer_not_found(self):
        if self.existing_ticket is None:
            self.skipTest("existing ticket was not created")

        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["issuer_id"] = -100
        test_id = self.existing_ticket.id
        ticket_update = schemas.TicketUpdate.model_validate(test_ticket_dict)
        _, status_code = crud.update_ticket(self.db, test_id, ticket_update)
        self.assertEqual(status_code, constants.StatusCode.ISSUER_NOT_FOUND)

    def test_assignee_not_found(self):
        if self.existing_ticket is None:
            self.skipTest("existing ticket was not created")

        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["assignee_id"] = -100
        test_id = self.existing_ticket.id
        ticket_update = schemas.TicketUpdate.model_validate(test_ticket_dict)
        _, status_code = crud.update_ticket(self.db, test_id, ticket_update)
        self.assertEqual(status_code, constants.StatusCode.ASSIGNEE_NOT_FOUND)

    def test_optional_field_on_ticket_update_basemodel(self):
        if self.existing_ticket is None:
            self.skipTest("existing ticket was not created")

        # issuer id
        ticket_update = schemas.TicketUpdate.model_validate({"issuer_id": 1})
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # assignee id
        ticket_update = schemas.TicketUpdate.model_validate({"assignee_id": 2})
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # title
        ticket_update = schemas.TicketUpdate.model_validate({"title": "my laggy app"})
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # status
        ticket_update = schemas.TicketUpdate.model_validate(
            {"status": constants.TicketStatus.IN_PROGRESS}
        )
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # category
        ticket_update = schemas.TicketUpdate.model_validate(
            {"category": constants.TicketCategory.HARDWARE}
        )
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # description
        ticket_update = schemas.TicketUpdate.model_validate(
            {"description": "my suppeerrr laggy app"}
        )
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)

    def test_invalid_value_on_ticket_update_basemodel(self):
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

    def test_none_in_optional_field_on_ticket_update_basemodel(self):
        # issuer id
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["issuer_id"] = None
        ticket_update = schemas.TicketUpdate.model_validate(test_ticket_dict)
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # assignee_id
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["assignee_id"] = None
        ticket_update = schemas.TicketUpdate.model_validate(test_ticket_dict)
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # title
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["title"] = None
        ticket_update = schemas.TicketUpdate.model_validate(test_ticket_dict)
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # status
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["status"] = None
        ticket_update = schemas.TicketUpdate.model_validate(test_ticket_dict)
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # category
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["category"] = None
        ticket_update = schemas.TicketUpdate.model_validate(test_ticket_dict)
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)
        # description
        test_ticket_dict = self.test_ticket_dict.copy()
        test_ticket_dict["description"] = None
        ticket_update = schemas.TicketUpdate.model_validate(test_ticket_dict)
        self.assertIsInstance(ticket_update, schemas.TicketUpdate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
