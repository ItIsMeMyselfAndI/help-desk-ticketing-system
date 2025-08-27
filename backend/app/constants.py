from enum import Enum

class Error(Enum):
    SUCCESS = 0
    UNAME_ALREADY_EXIST = 1
    EMAIL_ALREADY_EXIST = 2
    USER_DOESNT_EXIST = 3

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




