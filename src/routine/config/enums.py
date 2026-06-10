from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class RoutineType(str, Enum):
    CHECKBOX = "Checkbox"
    MULTISELECT = "Multiselect"
    TEXT = "Text"
    FEEDBACK = "Feedback"
    NUMBER = "Number"
    TIME = "Time"
