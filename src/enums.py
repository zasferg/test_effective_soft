from enum import Enum


class BookStatus(Enum):
    """
    Перечисление статусов книги.
    """

    available = "в наличии"
    given = "выдана"
