from enum import Enum

class Error(Enum):
    SUCCESS = 0
    # user
    UNAME_ALREADY_EXIST = 1
    EMAIL_ALREADY_EXIST = 2
    USER_NOT_FOUND = 3
    # ticket
    TICKET_NOT_FOUND = 4
    ISSUER_NOT_FOUND = 5
    ASSIGNEE_NOT_FOUND = 6
    SAME_ISSUER_AND_ASSIGNEE = 7
    # attachment
    FILE_NOT_FOUND = 8
    FILE_ALREADY_EXIST = 9
    # message
    MESSAGE_NOT_FOUND = 10
    CONTENT_IS_EMPTY = 11
    SENDER_NOT_FOUND = 12
    RECEIVER_NOT_FOUND = 13


class TableName(Enum):
    USERS = "users"
    TICKETS = "tickets"
    ATTACHMENTS = "attachments"
    MESSAGES = "messages"

class UserRole(Enum):
    CLIENT = "client"
    SUPPORT = "support"
    ADMIN = "admin"

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"

class TicketCategory(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    ACCESS = "access"
    ACCOUNT = "account"
    OTHER = "other"




