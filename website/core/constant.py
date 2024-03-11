import enum


class YnEnum(enum.Enum):
    YES = 1
    NO = 0


class DateTimeFormatEnum(enum.Enum):
    DATETIME = "%Y-%m-%d %H:%M:%S"
    DATE = "%Y-%m-%d"
