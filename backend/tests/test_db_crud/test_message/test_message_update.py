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
        # test case
        self.test_message_dict = {
            "sender_id": 1,
            "receiver_id": 2,
            "ticket_id": 1,
            "content": "yoww, wassup",
        }

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")
        invalid_args = ["lksdjfd", None, 4.8]
        message_id = self.existing_message.id
        message_update = schemas.MessageUpdate.model_validate(self.test_message_dict)

        for arg in invalid_args:
            # db session
            with self.subTest(
                arg=arg, message_id=message_id, message_update=message_update
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_message(arg, message_id, message_update)
            # message id
            with self.subTest(
                arg=arg, message_id=message_id, message_update=message_update
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_message(self.db, arg, message_update)
            # message basemodel
            with self.subTest(
                arg=arg, message_id=message_id, message_update=message_update
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_message(self.db, message_id, arg)

    def test_sender_not_found(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")

        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = -100
        message_id = self.existing_message.id
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        _, status_code = crud.update_message(self.db, message_id, message_update)
        self.assertEqual(status_code, constants.StatusCode.SENDER_NOT_FOUND)

    def test_receiver_not_found(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")

        message_id = self.existing_message.id
        message_update = schemas.MessageUpdate.model_validate({"receiver_id": -100})
        _, status_code = crud.update_message(self.db, message_id, message_update)
        self.assertEqual(status_code, constants.StatusCode.RECEIVER_NOT_FOUND)

    def test_ticket_not_found(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")

        test_message_dict = self.test_message_dict.copy()
        test_message_dict["ticket_id"] = -100
        message_id = self.existing_message.id
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        _, status_code = crud.update_message(self.db, message_id, message_update)
        self.assertEqual(status_code, constants.StatusCode.TICKET_NOT_FOUND)

    def test_same_sender_and_receiver(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")

        # same new sender & new receiver
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = 2
        test_message_dict["receiver_id"] = 2
        message_id = self.existing_message.id
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        _, status_code = crud.update_message(self.db, message_id, message_update)
        self.assertEqual(status_code, constants.StatusCode.SAME_SENDER_AND_RECEIVER)
        # same new sender & prev receiver
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = 2
        message_id = self.existing_message.id
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        _, status_code = crud.update_message(self.db, message_id, message_update)
        self.assertEqual(status_code, constants.StatusCode.SAME_SENDER_AND_RECEIVER)
        # same prev sender & new receiver
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["receiver_id"] = 1
        message_id = self.existing_message.id
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        _, status_code = crud.update_message(self.db, message_id, message_update)
        self.assertEqual(status_code, constants.StatusCode.SAME_SENDER_AND_RECEIVER)

    def test_optional_field_on_message_update_basemodel(self):
        if self.existing_message is None:
            self.skipTest("existing message was not created")

        # sender id
        message_update = schemas.MessageUpdate.model_validate({"sender_id": 1})
        self.assertIsInstance(message_update, schemas.MessageUpdate)
        # reciever id
        message_update = schemas.MessageUpdate.model_validate({"receiver_id": 2})
        self.assertIsInstance(message_update, schemas.MessageUpdate)
        # ticket id
        message_update = schemas.MessageUpdate.model_validate({"ticket_id": 1})
        self.assertIsInstance(message_update, schemas.MessageUpdate)
        # content
        message_update = schemas.MessageUpdate.model_validate(
            {"content": "yoww, wassup"}
        )
        self.assertIsInstance(message_update, schemas.MessageUpdate)

    def test_invalid_value_on_message_update_basemodel(self):
        # sender id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageUpdate.model_validate(test_message_dict)
        # receiver id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["receiver_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageUpdate.model_validate(test_message_dict)
        # ticket id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["ticket_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageUpdate.model_validate(test_message_dict)
        # content
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["content"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.MessageUpdate.model_validate(test_message_dict)

    def test_none_in_optional_field_on_message_update_basemodel(self):
        # sender id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["sender_id"] = None
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        self.assertIsInstance(message_update, schemas.MessageUpdate)
        # receiver id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["receiver_id"] = None
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        self.assertIsInstance(message_update, schemas.MessageUpdate)
        # ticket id
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["ticket_id"] = None
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        self.assertIsInstance(message_update, schemas.MessageUpdate)
        # content
        test_message_dict = self.test_message_dict.copy()
        test_message_dict["content"] = None
        message_update = schemas.MessageUpdate.model_validate(test_message_dict)
        self.assertIsInstance(message_update, schemas.MessageUpdate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
