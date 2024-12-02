from service.service import Library
import argparse


library = Library()


def main():
    """
    Основная функция для управления библиотекой книг с использованием командной строки.
    """

    parser = argparse.ArgumentParser(description="Управление библиотекой книг.")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="Добавить книгу")
    add_parser.add_argument("--title", type=str, help="Название книги")
    add_parser.add_argument("--author", type=str, help="Автор книги")
    add_parser.add_argument("--year", type=str, help="Год издания книги")

    remove_parser = subparsers.add_parser("del", help="Удалить книгу")
    remove_parser.add_argument("--id", type=str, help="ID книги")

    search_parser = subparsers.add_parser("sbp", help="Поиск книги")
    search_parser.add_argument("--query", type=str, help="Запрос для поиска")

    subparsers.add_parser("ga", help="Просмотр списка книг")

    update_parser = subparsers.add_parser("us", help="Изменить статус книги")
    update_parser.add_argument("--id", type=str, help="ID книги")
    update_parser.add_argument("--status", type=str, help="Новый статус книги")

    args = parser.parse_args()

    if args.command == "add":
        library.create_book(title=args.title, author=args.author, year=args.year)
    elif args.command == "del":
        library.delete_book(args.id)
    elif args.command == "sbp":
        library.get_book_by_param(args.query)
    elif args.command == "ga":
        library.get_all_books()
    elif args.command == "us":
        library.update_status(args.id, args.status)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
