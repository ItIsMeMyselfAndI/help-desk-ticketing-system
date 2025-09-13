import datetime
import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


class TestDBCreateMessage(unittest.TestCase):

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
                    "assignee_id": None,
                    "title": "Computer won't start after power outage",
                    "status": constants.TicketStatus.IN_PROGRESS,
                    "category": constants.TicketCategory.HARDWARE,
                    "description": "My desktop computer refuses to turn on after yesterday's power outage. The power button doesn't respond at all.",
                }
            ),
        )
        # test case
        self.test_message_dict = {
            "sender_id": 1,
            "receiver_id": 2,
            "ticket_id": 1,
            "content": "yoww, wassup",
            "sent_at": datetime.datetime.now().astimezone().isoformat(),
            "edited_at": datetime.datetime.now().astimezone().isoformat(),
        }

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        invalid_args = ["lksdjfd", None, 4.8]
        message_create = schemas.MessageCreate.model_validate(self.test_message_dict)

        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, message_create=message_create):
                with self.assertRaises(pydantic.ValidationError):
                    crud.create_message(arg, message_create)
            # message basemodel
            with self.subTest(arg=arg, message_create=message_create):
                with self.assertRaises(pydantic.ValidationError):
                    crud.create_message(self.db, arg)

    def test_sender_not_found(self):
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = -100
        message_create = schemas.MessageCreate.model_validate(test_message_dict)
        _, status_code = crud.create_message(self.db, message_create)
        self.assertEqual(status_code, constants.StatusCode.SENDER_NOT_FOUND)

    def test_receiver_not_found(self):
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["receiver_id"] = -100
        message_create = schemas.MessageCreate.model_validate(test_message_dict)
        _, status_code = crud.create_message(self.db, message_create)
        self.assertEqual(status_code, constants.StatusCode.RECEIVER_NOT_FOUND)

    def test_ticket_not_found(self):
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["ticket_id"] = -100
        message_create = schemas.MessageCreate.model_validate(test_message_dict)
        _, status_code = crud.create_message(self.db, message_create)
        self.assertEqual(status_code, constants.StatusCode.TICKET_NOT_FOUND)

    def test_empty_content(self):
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["content"] = ""
        message_create = schemas.MessageCreate.model_validate(test_message_dict)
        _, status_code = crud.create_message(self.db, message_create)
        self.assertEqual(status_code, constants.StatusCode.CONTENT_IS_EMPTY)

    def test_same_sender_and_receiver(self):
        # same new sender & new receiver
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = 2
        test_message_dict["receiver_id"] = 2
        message_create = schemas.MessageCreate.model_validate(test_message_dict)
        _, status_code = crud.create_message(self.db, message_create)
        self.assertEqual(status_code, constants.StatusCode.SAME_SENDER_AND_RECEIVER)

    def test_with_dates(self):
        message_create = schemas.MessageCreate.model_validate(self.test_message_dict)
        result_message, _ = crud.create_message(self.db, message_create)
        if not result_message:
            self.fail("valid message with dates not created")
        result_message_dict = result_message.as_dict()

        self.assertEqual(
            result_message_dict["sender_id"], self.test_message_dict["sender_id"]
        )
        self.assertEqual(
            result_message_dict["receiver_id"], self.test_message_dict["receiver_id"]
        )
        self.assertEqual(
            result_message_dict["ticket_id"], self.test_message_dict["ticket_id"]
        )
        self.assertEqual(
            result_message_dict["content"], self.test_message_dict["content"]
        )
        self.assertEqual(
            result_message_dict["sent_at"], self.test_message_dict["sent_at"]
        )
        self.assertEqual(
            result_message_dict["edited_at"], self.test_message_dict["edited_at"]
        )

    def test_without_dates(self):
        test_message_dict = self.test_message_dict.copy()
        del test_message_dict["sent_at"]
        del test_message_dict["edited_at"]
        message_create = schemas.MessageCreate.model_validate(test_message_dict)
        result_message, _ = crud.create_message(self.db, message_create)
        if not result_message:
            self.fail("valid message without dates not created")
        result_message_dict = result_message.as_dict()

        self.assertEqual(
            result_message_dict["sender_id"], self.test_message_dict["sender_id"]
        )
        self.assertEqual(
            result_message_dict["receiver_id"], self.test_message_dict["receiver_id"]
        )
        self.assertEqual(
            result_message_dict["ticket_id"], self.test_message_dict["ticket_id"]
        )
        self.assertEqual(
            result_message_dict["content"], self.test_message_dict["content"]
        )

    def test_missing_required_field_on_message_create_basemodel(self):
        # sender id
        test_message_dict = self.test_message_dict.copy()
        del test_message_dict["sender_id"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # receiver id
        test_message_dict = self.test_message_dict.copy()
        del test_message_dict["receiver_id"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # ticket id
        test_message_dict = self.test_message_dict.copy()
        del test_message_dict["ticket_id"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # content
        test_message_dict = self.test_message_dict.copy()
        del test_message_dict["content"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)

    def test_invalid_value_on_message_create_basemodel(self):
        # sender id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # receiver id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["receiver_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # ticket id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["ticket_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # content
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["content"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)

    def test_none_in_required_field_on_message_create_basemodel(self):
        # sender id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # receiver id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["receiver_id"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # ticket id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["ticket_id"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)
        # content
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["content"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageCreate.model_validate(test_message_dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
