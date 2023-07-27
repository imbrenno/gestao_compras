from enum import Enum


class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    def __str__(self):
        return self.value