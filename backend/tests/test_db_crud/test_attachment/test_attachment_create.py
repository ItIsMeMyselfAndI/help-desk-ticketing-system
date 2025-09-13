import datetime
import unittest

import pydantic
from app import crud, schemas, constants
from app.db import get_db, reset_db


class TestDBCreateAttachment(unittest.TestCase):

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
        self.test_attachment_dict = {
            "ticket_id": 1,
            "filename": "myfile.pdf",
            "filetype": "pdf",
            "filesize": 1020,
            "uploaded_at": datetime.datetime.now().astimezone().isoformat(),
            "updated_at": datetime.datetime.now().astimezone().isoformat(),
        }

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        invalid_args = ["lksdjfd", None, 4.8]
        attachment_create = schemas.AttachmentCreate.model_validate(
            self.test_attachment_dict
        )

        for arg in invalid_args:
            # db session
            with self.subTest(arg=arg, attachment_create=attachment_create):
                with self.assertRaises(pydantic.ValidationError):
                    crud.create_attachment(arg, attachment_create)
            # attachment basemodel
            with self.subTest(arg=arg, attachment_create=attachment_create):
                with self.assertRaises(pydantic.ValidationError):
                    crud.create_attachment(self.db, arg)

    def test_ticket_not_found(self):
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["ticket_id"] = -100
        attachment_create = schemas.AttachmentCreate.model_validate(
            test_attachment_dict
        )
        _, status_code = crud.create_attachment(self.db, attachment_create)
        self.assertEqual(status_code, constants.StatusCode.TICKET_NOT_FOUND)

    def test_with_dates(self):
        attachment_create = schemas.AttachmentCreate.model_validate(
            self.test_attachment_dict
        )
        result_attachment, _ = crud.create_attachment(self.db, attachment_create)
        if not result_attachment:
            self.fail("valid attachment with dates not created")
        result_attachment_dict = result_attachment.as_dict()

        self.assertEqual(
            result_attachment_dict["ticket_id"],
            self.test_attachment_dict["ticket_id"],
        )
        self.assertEqual(
            result_attachment_dict["filename"],
            self.test_attachment_dict["filename"],
        )
        self.assertEqual(
            result_attachment_dict["filetype"],
            self.test_attachment_dict["filetype"],
        )
        self.assertEqual(
            result_attachment_dict["filesize"],
            self.test_attachment_dict["filesize"],
        )

    def test_without_dates(self):
        test_attachment_dict = self.test_attachment_dict.copy()
        del test_attachment_dict["uploaded_at"]
        del test_attachment_dict["updated_at"]
        attachment_create = schemas.AttachmentCreate.model_validate(
            test_attachment_dict
        )
        result_attachment, _ = crud.create_attachment(self.db, attachment_create)
        if not result_attachment:
            self.fail("valid attachment without dates not created")
        result_attachment_dict = result_attachment.as_dict()

        self.assertEqual(
            result_attachment_dict["ticket_id"],
            self.test_attachment_dict["ticket_id"],
        )
        self.assertEqual(
            result_attachment_dict["filename"],
            self.test_attachment_dict["filename"],
        )
        self.assertEqual(
            result_attachment_dict["filetype"],
            self.test_attachment_dict["filetype"],
        )
        self.assertEqual(
            result_attachment_dict["filesize"],
            self.test_attachment_dict["filesize"],
        )

    def test_missing_required_field_on_attachment_create_basemodel(self):
        # ticket id
        test_attachment_dict = self.test_attachment_dict.copy()
        del test_attachment_dict["ticket_id"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filename
        test_attachment_dict = self.test_attachment_dict.copy()
        del test_attachment_dict["filename"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filetype
        test_attachment_dict = self.test_attachment_dict.copy()
        del test_attachment_dict["filetype"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filesize
        test_attachment_dict = self.test_attachment_dict.copy()
        del test_attachment_dict["filesize"]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)

    def test_invalid_value_on_attachment_create_basemodel(self):
        # ticket id
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["ticket_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filename
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filename"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filetype
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filetype"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filesize
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filesize"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)

    def test_none_in_required_field_on_attachment_create_basemodel(self):
        # ticket id
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["ticket_id"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filename
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filename"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filetype
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filetype"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)
        # filesize
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filesize"] = None
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentCreate.model_validate(test_attachment_dict)


if __name__ == "__main__":
    unittest.main(verbosity=2)
