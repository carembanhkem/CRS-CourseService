from enum import Enum


class CourseType(str, Enum):
    ORDINARY = "ORDINARY"
    COACHING = "COACHING"
    LIVE = "LIVE"


