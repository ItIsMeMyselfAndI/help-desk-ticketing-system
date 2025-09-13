import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


# read
class TestDBDeleteAttachment(unittest.TestCase):

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
        # existing attachment
        self.existing_attachment_dict = {
            "ticket_id": 1,
            "filename": "myfile.pdf",
            "filetype": "pdf",
            "filesize": 1020,
        }
        self.existing_attachment, _ = crud.create_attachment(
            self.db,
            schemas.AttachmentCreate.model_validate(self.existing_attachment_dict),
        )

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_id(self):
        print(self.existing_attachment)
        if self.existing_attachment is None:
            self.skipTest("existing attachment was not created")
        attachment_id = self.existing_attachment.id

        invalid_args = ["lksdjfd", None, 4.8]
        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, attachment_id=attachment_id):
                with self.assertRaises(pydantic.ValidationError):
                    crud.delete_attachment(arg, attachment_id)
            # attachment id
            with self.subTest(arg=arg):
                with self.assertRaises(pydantic.ValidationError):
                    crud.delete_attachment(self.db, arg)

    def test_left_out_of_bound_id(self):
        if self.existing_attachment is None:
            self.skipTest("existing attachment was not created")
        attachment_id = self.existing_attachment.id

        result_attachment, status_code = crud.delete_attachment(
            self.db, attachment_id - 100
        )
        self.assertIsNone(result_attachment)
        self.assertEqual(status_code, constants.StatusCode.FILE_NOT_FOUND)

    def test_right_out_of_bound_id(self):
        if self.existing_attachment is None:
            self.skipTest("existing attachment was not created")
        attachment_id = self.existing_attachment.id

        result_attachment, status_code = crud.delete_attachment(
            self.db, attachment_id + 100
        )
        self.assertIsNone(result_attachment)
        self.assertEqual(status_code, constants.StatusCode.FILE_NOT_FOUND)

    def test_correct_id(self):
        if self.existing_attachment is None:
            self.skipTest("existing attachment was not created")
        attachment_id = self.existing_attachment.id

        result_attachment, _ = crud.delete_attachment(self.db, attachment_id)
        if result_attachment is None:
            self.fail("delete attachment failed")
        result_attachment_dict = result_attachment.as_dict()

        self.assertEqual(
            result_attachment_dict["ticket_id"],
            self.existing_attachment_dict["ticket_id"],
        )
        self.assertEqual(
            result_attachment_dict["filename"],
            self.existing_attachment_dict["filename"],
        )
        self.assertEqual(
            result_attachment_dict["filetype"],
            self.existing_attachment_dict["filetype"],
        )
        self.assertEqual(
            result_attachment_dict["filesize"],
            self.existing_attachment_dict["filesize"],
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
