from enum import Enum


class UserType(str, Enum):
    INSTRUCTOR = "INSTRUCTOR"
    PLAYER = "PLAYER"


class LectureType(str, Enum):
    VIDEO = "VIDEO"
    TEXT = "TEXT"


class LectureVisibilityStatus(str, Enum):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"


class ProcessingStatus(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
