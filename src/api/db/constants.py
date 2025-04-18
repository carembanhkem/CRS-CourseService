from enum import Enum


class UserType(str, Enum):
    INSTRUCTOR = "INSTRUCTOR"
    PLAYER = "PLAYER"
