import pytest


def test_book_creation(test_library):

    test_library.create_book(title="test 1", author="author a", year="1111")
    test_library.create_book(title="test 2", author="author a", year="1112")
    test_library.create_book(title="test 3", author="author a", year="1113")
    test_library.create_book(title="test 4", author="author b", year="1111")
    test_library.create_book(title="test 5", author="author b", year="1112")
    test_library.create_book(title="test 6", author="author b", year="1113")

    list_of_books = test_library.books

    assert len(list_of_books) == 6

    with pytest.raises(FileExistsError):
        test_library.create_book(title="test 1", author="author a", year="1111")

    with pytest.raises(ValueError):
        bad_value_title = "te/st"
        test_library.create_book(title=bad_value_title, author="author", year="1113")

    with pytest.raises(TypeError):
        bad_value_title = 222
        test_library.create_book(title=bad_value_title, author="author", year="1113")

    with pytest.raises(ValueError):
        bad_value_author = "auth2or"
        test_library.create_book(title="test 7", author=bad_value_author, year="1113")

    with pytest.raises(TypeError):
        bad_value_author = 222
        test_library.create_book(title="test 7", author=bad_value_author, year="1113")

    with pytest.raises(ValueError):
        bad_value_year = "11111"
        test_library.create_book(title="test 7", author="author b", year=bad_value_year)

    with pytest.raises(TypeError):
        bad_value_year = "-222"
        test_library.create_book(title="test 7", author="author b", year=bad_value_year)


def test_get_all_books(test_library, get_check_data):

    test_library.create_book(title="test 1", author="author a", year="1111")
    test_library.create_book(title="test 2", author="author a", year="1112")
    test_library.create_book(title="test 3", author="author a", year="1113")
    test_library.create_book(
        title=get_check_data["title"],
        author=get_check_data["author"],
        year=get_check_data["year"],
    )

    list_of_books = test_library.get_all_books()
    check_book = list_of_books[3]
    assert len(list_of_books) == 4

    assert get_check_data["title"] == check_book.title
    assert get_check_data["author"] == check_book.author
    assert get_check_data["year"] == check_book.year


def test_get_book_by_param(test_library, get_check_data):
    check_title = "test 1"
    check_author = "author a"
    check_year = "1112"

    test_library.create_book(title=check_title, author=check_author, year="1111")
    test_library.create_book(title="test 2", author=check_author, year=check_year)
    test_library.create_book(title="test 3", author=check_author, year=check_year)
    test_library.create_book(
        title=get_check_data["title"],
        author=get_check_data["author"],
        year=get_check_data["year"],
    )

    list_of_books = test_library.get_book_by_param(query=check_title)
    assert len(list_of_books) == 1
    list_of_books = test_library.get_book_by_param(query=check_author)
    assert len(list_of_books) == 3
    list_of_books = test_library.get_book_by_param(query=check_year)
    assert len(list_of_books) == 2

    list_of_books = test_library.get_book_by_param(query=get_check_data["title"])
    book = list_of_books[0]

    assert get_check_data["title"] == book.title
    assert get_check_data["author"] == book.author
    assert get_check_data["year"] == book.year

    wrong_query_letters = "wrong"
    list_of_books = test_library.get_book_by_param(query=wrong_query_letters)

    assert list_of_books == None

    wrong_query_digit = "1100"
    list_of_books = test_library.get_book_by_param(query=wrong_query_digit)

    assert list_of_books == None


def test_update_book_status(test_library, get_check_data):

    new_status = "выдана"
    wrong_status = "wrong"

    test_library.create_book(
        title=get_check_data["title"],
        author=get_check_data["author"],
        year=get_check_data["year"],
    )
    list_of_books = test_library.get_book_by_param(query=get_check_data["title"])
    id = list_of_books[0].id

    test_library.update_status(book_id=id, new_status=new_status)
    list_of_books = test_library.get_book_by_param(query=id)

    book = list_of_books[0]

    assert book.status.value == new_status

    with pytest.raises(FileExistsError):
        test_library.update_status(book_id=id, new_status=new_status)
    with pytest.raises(ValueError):
        test_library.update_status(book_id=id, new_status=wrong_status)


def test_delete_book(test_library, get_check_data):

    test_library.create_book(
        title=get_check_data["title"],
        author=get_check_data["author"],
        year=get_check_data["year"],
    )
    list_of_books = test_library.get_book_by_param(query=get_check_data["title"])
    id = list_of_books[0].id
    test_library.delete_book(book_id=id)
    list_of_books = test_library.get_book_by_param(query=id)

    assert list_of_books == None

    with pytest.raises(FileNotFoundError):
        wrong_id = "wrong_id"
        test_library.delete_book(book_id=wrong_id)
