import json
import re
from time import sleep
from typing import List, Optional
import uuid
from enums import BookStatus
from settings import DATA_FILE
import os


class Book:
    """
    Класс, представляющий книгу в библиотеке
    """

    def __init__(
        self,
    ):
        self._id: str = str(uuid.uuid4())
        self._title: str = None
        self._author: str = None
        self._year: str = None
        self._status: str = BookStatus.available

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title: str):
        """
        Инициализация названия книги с валидацией.
        """

        if not title:
            raise ValueError("Поле 'Название' не может быть пустым")
        if not isinstance(title, str):
            raise TypeError("Ошибка валидации")
        if not re.match(r"^[a-zA-Zа-яА-Я0-9\s]+$", title):
            raise ValueError("Поле 'Название' содержит только буквы и цифры")
        self._title = title

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author: str):
        """
        Инициализация автора книги с валидацией.
        """

        if not author:
            raise ValueError("Поле 'автор' не может быть пустым.")
        if not isinstance(author, str):
            raise TypeError("Ошибка валидации")
        if not re.match(r"^[a-zA-Zа-яА-Я\s]+$", author):
            raise ValueError("Поле 'автор' содержит только буквы и пробелы")
        self._author = author

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year: int):
        """
        Инициализация года книги с валидацией.
        """
        if not year:
            raise ValueError("Поле 'год' не может быть пустым.")
        if not isinstance(year, int):
            raise TypeError("Поле 'год' должно содержать только цифры.")
        if year < 0 or year > 2025:
            raise ValueError("Невалидное число")
        self._year = str(year)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: BookStatus):
        """
        Инициализация статуса книги с валидацией.
        """
        if not isinstance(status, BookStatus):
            raise ValueError(
                f"Недопустимый статус: {status}. Допустимые значения: {[status.value for status in BookStatus]}"
            )
        self._status = status

    def to_dict(self):
        """
        Преобразование объекта книги в словарь.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, data: dict):
        """
        Создание объекта книги из словаря.
        """
        book = cls()
        book._id = data.get("id", str(uuid.uuid4()))
        book.title = data["title"]
        book.author = data["author"]
        book.year = int(data["year"]) if data["year"].isdigit() else Exception
        book.status = BookStatus(data["status"])

        return book


class Library:
    """
    Класс библиотеки для работы с обьектами книг.
    """

    def __init__(self, data_file: str = DATA_FILE):
        """
        Инициализация библиотеки с загрузкой данных из файла.
        """
        self.data_file = data_file
        self.books = self.load_data()

    def load_data(self) -> List[Book]:
        """
        Загружает данные о книгах из файла.
        """
        try:
            if not os.path.exists(self.data_file):
                print(f"Файл {self.data_file} не найден, создается новый файл.")
                return []
            with open(self.data_file, "r") as file:
                data = json.load(file)
                return [Book.from_dict(item) for item in data]
        except json.JSONDecodeError:
            print(f"Ошибка чтения файла {self.data_file}.")
            return []

    def save_data(self) -> None:
        """
        Сохраняет данные о книгах в файл.
        """
        try:
            with open(self.data_file, "w") as file:
                json.dump([book.to_dict() for book in self.books], file, indent=4)
        except Exception as e:
            raise e

    def create_book(self, title: str, author: str, year: str) -> None:
        """
        Создает новую книгу и добавляет её в библиотеку.

        :param title: Название книги
        :param author: Автор книги
        :param year: Год издания книги
        """
        try:
            if self.get_book_by_param(query=title):
                raise FileExistsError("Данная книга уже в библиотеке")
            book = Book()
            book.title = title
            book.author = author
            book.year = int(year) if year.isdigit() else Exception
            self.books.append(book)
            self.save_data()
            print(f'Книга "{title}" добавлена.')
        except FileExistsError as e:
            raise e

    def delete_book(self, book_id: str):
        """
        Удаляет книгу из библиотеки по её ID.

        :param book_id: ID книги
        """
        try:
            if not self.get_book_by_param(query=book_id):
                raise FileNotFoundError(f"Книга с id {book_id} не найдена")
            self.books = [book for book in self.books if book.id != book_id]
            self.save_data()
            print(f'Книга с id "{book_id}" удалена.')
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise e

    def get_book_by_param(
        self, query: str = None, results=None
    ) -> Optional[List[Book]]:
        """
        Ищет книги по заданному параметру (название, автор, год или ID).

        :param query: Параметр для поиска
        :return: Список найденных книг
        """
        try:
            if query.isdigit():
                results = [book for book in self.books if query == book.year]
            elif isinstance(query, str):
                results = [
                    book
                    for book in self.books
                    if query.lower() in book.title.lower()
                    or query.lower() in book.author.lower()
                    or query in book.id
                ]
            if not results:
                raise FileNotFoundError("Книги не найдены.")
            else:
                for book in results:
                    print(
                        f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status.value}"
                    )
                return results
        except FileNotFoundError as e:
            print(e)
            return None
        except AttributeError as e:
            raise ("Невалидные данные")

    def get_all_books(self)-> Optional[List[Book]]:
        """
        Возвращает список всех книг в библиотеке.
        """
        try:
            if not self.books:
                raise FileNotFoundError("Библиотека пуста.")
            else:
                for book in self.books:
                    print(
                        f"ID: {book.id}, Название: {book.title}, Автор: {book.author}, Год: {book.year}, Статус: {book.status.value}"
                    )
                return self.books
        except FileNotFoundError as e:
            raise e
        except Exception as e:
            raise e

    def update_status(self, book_id: str, new_status: str) -> None:
        """
        Обновляет статус книги по её ID.

        :param book_id: ID книги
        :param new_status: Новый статус книги
        """
        try:
            if not self.get_book_by_param(book_id):
                raise FileNotFoundError(f'Книга с id "{book_id}" не найдена.')

            if new_status not in [status.value for status in BookStatus]:
                raise ValueError(
                    f"Недопустимый статус: {new_status}. Допустимые значения: {[status.value for status in BookStatus]}"
                )
            for book in self.books:
                if book.id == book_id:
                    if book.status.value == new_status:
                        raise FileExistsError("Данный статус уже уже присвоен книге")
                    book.status = BookStatus(new_status)
                    self.save_data()
                    print(
                        f'Статус книги с id "{book_id}" обновлен на "{book.status.value}".'
                    )
                    return
        except FileNotFoundError as e:
            raise e
        except FileExistsError as e:
            raise e
        except ValueError as e:
            raise e
        except TypeError as e:
            raise e
