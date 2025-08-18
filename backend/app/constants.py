from enum import Enum
from typing import Literal

class TableNames(Enum):
    USERS = "users"
    TICKETS = "tickets"
    ATTACHMENTS = "attachments"
    MESSAGES = "messages"
TableNamesLiterals = Literal[
    "users",
    "tickets",
    "attachments",
    "messages"
]

class UserRoles(Enum):
    CLIENT = "client"
    SUPPORT = "support"
    ADMIN = "admin"
UserRolesLiterals = Literal[
    "client",
    "support",
    "admin"
]

class TicketStatus(Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"
    CANCELLED = "cancelled"
TicketStatusLiterals = Literal[
    "open",
    "in_progress",
    "resolved",
    "closed",
    "cancelled"
]

class TicketCategory(Enum):
    HARDWARE = "hardware"
    SOFTWARE = "software"
    NETWORK = "network"
    ACCESS = "access"
    ACCOUNT = "account"
    OTHER = "other"
TicketCategoryLiterals = Literal[
    "hardware",
    "software",
    "network",
    "access",
    "account",
    "other"
]




