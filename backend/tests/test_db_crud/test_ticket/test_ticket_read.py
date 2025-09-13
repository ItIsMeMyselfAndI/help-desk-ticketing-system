import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


# read
class TestDBReadTicket(unittest.TestCase):

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

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_id(self):
        if self.existing_ticket is None:
            self.skipTest("existing ticket was not created")
        ticket_id = self.existing_ticket.id

        invalid_args = ["lksdjfd", None, 4.8]
        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, ticket_id=ticket_id):
                with self.assertRaises(pydantic.ValidationError):
                    crud.get_ticket_good(arg, ticket_id)
            # ticket id
            with self.subTest(arg=arg):
                with self.assertRaises(pydantic.ValidationError):
                    crud.get_ticket_good(self.db, arg)

    def test_left_out_of_bound_id(self):
        if self.existing_ticket is None:
            self.skipTest("existing ticket was not created")
        ticket_id = self.existing_ticket.id

        result_ticket, status_code = crud.get_ticket_good(self.db, ticket_id - 100)
        self.assertIsNone(result_ticket)
        self.assertEqual(status_code, constants.StatusCode.TICKET_NOT_FOUND)

    def test_right_out_of_bound_id(self):
        if self.existing_ticket is None:
            self.skipTest("existing ticket was not created")
        ticket_id = self.existing_ticket.id

        result_ticket, status_code = crud.get_ticket_good(self.db, ticket_id + 100)
        self.assertIsNone(result_ticket)
        self.assertEqual(status_code, constants.StatusCode.TICKET_NOT_FOUND)

    def test_correct_id(self):
        if self.existing_ticket is None:
            self.skipTest("existing ticket was not created")
        ticket_id = self.existing_ticket.id

        result_ticket, _ = crud.get_ticket_good(self.db, ticket_id)
        if result_ticket is None:
            self.fail("read ticket failed")
        result_ticket_dict = result_ticket.model_dump()

        self.assertEqual(
            result_ticket_dict["issuer"]["id"], self.existing_ticket_dict["issuer_id"]
        )
        if result_ticket_dict["assignee"]:
            self.assertEqual(
                result_ticket_dict["assignee"]["id"],
                self.existing_ticket_dict["assignee_id"],
            )
        self.assertEqual(
            result_ticket_dict["title"], self.existing_ticket_dict["title"]
        )
        self.assertEqual(
            result_ticket_dict["status"], self.existing_ticket_dict["status"]
        )
        self.assertEqual(
            result_ticket_dict["category"], self.existing_ticket_dict["category"]
        )
        self.assertEqual(
            result_ticket_dict["description"], self.existing_ticket_dict["description"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
