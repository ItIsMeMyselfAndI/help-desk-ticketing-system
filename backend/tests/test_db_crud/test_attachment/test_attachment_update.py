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
        # test case
        self.test_attachment_dict = {
            "ticket_id": 1,
            "filename": "myfile2.pdf",
            "filetype": "pdf",
            "filesize": 1020,
        }

    def tearDown(self):
        # just to make sure
        self.db.close()  # not necessary since get_db closes it on success/fail

    def test_invalid_arg(self):
        if self.existing_attachment is None:
            self.skipTest("existing attachment was not created")
        invalid_args = ["lksdjfd", None, 4.8]
        attachment_id = self.existing_attachment.id
        attachment_update = schemas.AttachmentUpdate.model_validate(
            self.test_attachment_dict
        )

        for arg in invalid_args:
            # db session
            with self.subTest(
                arg=arg,
                attachment_id=attachment_id,
                attachment_update=attachment_update,
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_attachment(arg, attachment_id, attachment_update)
            # attachment id
            with self.subTest(
                arg=arg,
                attachment_id=attachment_id,
                attachment_update=attachment_update,
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_attachment(self.db, arg, attachment_update)
            # attachment basemodel
            with self.subTest(
                arg=arg,
                attachment_id=attachment_id,
                attachment_update=attachment_update,
            ):
                with self.assertRaises(pydantic.ValidationError):
                    crud.update_attachment(self.db, attachment_id, arg)

    def test_ticket_not_found(self):
        if self.existing_attachment is None:
            self.skipTest("existing attachment was not created")

        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["ticket_id"] = -100
        test_id = self.existing_attachment.id
        attachment_update = schemas.AttachmentUpdate.model_validate(
            test_attachment_dict
        )
        _, status_code = crud.update_attachment(self.db, test_id, attachment_update)
        self.assertEqual(status_code, constants.StatusCode.TICKET_NOT_FOUND)

    def test_optional_field_on_attachment_update_basemodel(self):
        if self.existing_attachment is None:
            self.skipTest("existing attachment was not created")

        # ticket id
        attachment_update = schemas.AttachmentUpdate.model_validate({"ticket_id": 1})
        self.assertIsInstance(attachment_update, schemas.AttachmentUpdate)
        # filename
        attachment_update = schemas.AttachmentUpdate.model_validate(
            {"filename": "myfile2.pdf"}
        )
        self.assertIsInstance(attachment_update, schemas.AttachmentUpdate)
        # filetype
        attachment_update = schemas.AttachmentUpdate.model_validate({"filetype": "pdf"})
        self.assertIsInstance(attachment_update, schemas.AttachmentUpdate)
        # filesize
        attachment_update = schemas.AttachmentUpdate.model_validate({"filesize": 1020})
        self.assertIsInstance(attachment_update, schemas.AttachmentUpdate)

    def test_invalid_value_on_attachment_update_basemodel(self):
        # ticket id
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["ticket_id"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentUpdate.model_validate(test_attachment_dict)
        # filename
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filename"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentUpdate.model_validate(test_attachment_dict)
        # filetype
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filetype"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentUpdate.model_validate(test_attachment_dict)
        # filesize
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filesize"] = [1, 2, 3]
        with self.assertRaises(pydantic.ValidationError):
            schemas.AttachmentUpdate.model_validate(test_attachment_dict)

    def test_none_in_optional_field_on_attachment_update_basemodel(self):
        # ticket id
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["ticket_id"] = None
        attachment_update = schemas.AttachmentUpdate.model_validate(
            test_attachment_dict
        )
        self.assertIsInstance(attachment_update, schemas.AttachmentUpdate)
        # filename
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filename"] = None
        attachment_update = schemas.AttachmentUpdate.model_validate(
            test_attachment_dict
        )
        self.assertIsInstance(attachment_update, schemas.AttachmentUpdate)
        # filetype
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filetype"] = None
        attachment_update = schemas.AttachmentUpdate.model_validate(
            test_attachment_dict
        )
        self.assertIsInstance(attachment_update, schemas.AttachmentUpdate)
        # filesize
        test_attachment_dict = self.test_attachment_dict.copy()
        test_attachment_dict["filesize"] = None
        attachment_update = schemas.AttachmentUpdate.model_validate(
            test_attachment_dict
        )
        self.assertIsInstance(attachment_update, schemas.AttachmentUpdate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
