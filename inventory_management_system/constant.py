from enum import Enum

MIN_STOCK: int = 1
LOW_STOCK_THRESHOLD: int = 10


class Role(Enum):
    ADMIN = 1,
    USER = 2