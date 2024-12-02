Library Management System

Это система управления библиотекой книг, позволяющая добавлять, удалять, искать книги, просматривать список книг и изменять статус книги.

Установка

1. Клонируйте этот репозиторий на ваш локальный компьютер:

    git clone https://github.com/zasferg/test_effective_soft.git

2. Перейдите в директорию проекта:

    cd test_effective_soft

3. Создайте виртуальное окружение и активируйте его:

    python3 -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`

4. Установите зависимости:

    pip install -r requirements.txt

5. Перейдите в папку с проектом

    сd src

Использование

Для управления библиотекой книг используйте команду `python app.py` с соответствующими подкомандами и аргументами.

Команды

- `add` - Добавить книгу
    - `--title` - Название книги
    - `--author` - Автор книги
    - `--year` - Год издания книги

    Пример:

    python main.py add --title "Война и мир" --author "Лев Толстой" --year 1869

- `del` - Удалить книгу
    - `--id` - ID книги

    Пример:

    python main.py del --id "12345"

- `sbp` - Поиск книги по параметру
    - `--query` - Запрос для поиска

    Пример:

    python main.py sbp --query "Толстой"

- `ga` - Просмотр списка всех книг

    Пример:

    python main.py ga

- `us` - Изменить статус книги
    - `--id` - ID книги
    - `--status` - Новый статус книги

    Пример:

    python main.py us --id "12345" --status "выдана"

  Teсты

  1. Перейдите в папку
     
     cd tests

  2. Запустите тесты при помощи команы

     pytest test_func.py -v -s
     

  


