import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


# read
class TestDBReadMessage(unittest.TestCase):

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
        crud.create_ticket(
            self.db,
            schemas.TicketCreate.model_validate(
                {
                    "issuer_id": 1,
                    "assignee_id": 2,
                    "title": "Computer won't start after power outage",
                    "status": constants.TicketStatus.IN_PROGRESS,
                    "category": constants.TicketCategory.HARDWARE,
                    "description": "My desktop computer refuses to turn on after yesterday's power outage. The power button doesn't respond at all.",
                }
            ),
        )
        # existing message
        self.existing_message_dict = {
            "sender_id": 1,
            "receiver_id": 2,
            "ticket_id": 1,
            "content": "yoww, wassup",
        }
        self.existing_message, _ = crud.create_message(
            self.db,
            schemas.MessageCreate.model_validate(self.existing_message_dict),
        )

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_id(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")
        message_id = self.existing_message.id

        invalid_args = ["lksdjfd", None, 4.8]
        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, message_id=message_id):
                with self.assertRaises(pydantic.ValidationError):
                    crud.get_message_good(arg, message_id)
            # message id
            with self.subTest(arg=arg):
                with self.assertRaises(pydantic.ValidationError):
                    crud.get_message_good(self.db, arg)

    def test_left_out_of_bound_id(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")
        message_id = self.existing_message.id

        result_message, status_code = crud.get_message_good(self.db, message_id - 100)
        self.assertIsNone(result_message)
        self.assertEqual(status_code, constants.StatusCode.FILE_NOT_FOUND)

    def test_right_out_of_bound_id(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")
        message_id = self.existing_message.id

        result_message, status_code = crud.get_message_good(self.db, message_id + 100)
        self.assertIsNone(result_message)
        self.assertEqual(status_code, constants.StatusCode.FILE_NOT_FOUND)

    def test_correct_id(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")
        message_id = self.existing_message.id

        result_message, _ = crud.get_message_good(self.db, message_id)
        if result_message is None:
            self.fail("read message failed")
        result_message_dict = result_message.model_dump()

        self.assertEqual(
            result_message_dict["sender"]["id"], self.existing_message_dict["sender_id"]
        )
        self.assertEqual(
            result_message_dict["receiver"]["id"],
            self.existing_message_dict["receiver_id"],
        )
        self.assertEqual(
            result_message_dict["ticket"]["id"], self.existing_message_dict["ticket_id"]
        )
        self.assertEqual(
            result_message_dict["content"], self.existing_message_dict["content"]
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
