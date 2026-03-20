# Лабораторная работа: Источники задач и контракты

## Введение

В проекте сделана простая платформа приема задач из разных источников.
Все источники работают через один контракт `TaskSource` (`Protocol` + `runtime_checkable`).

Задача хранит только 2 поля:
- `id`
- `payload`

Реализованы 3 источника:
- `FileTaskSource` (читает задачи из JSON-файла)
- `GeneratorTaskSource` (генерирует задачи программно)
- `ApiTaskSource` (получает вакансии с hh.ru API)

Также есть `TaskPlatform`, которая регистрирует источники и собирает все задачи в один список.

## Архитектура проекта

```shell
mai-python-lab6-protocol/
├── data/
│   └── tasks.json                  # Пример задач для FileTaskSource
├── src/
│   ├── constants.py                # Константы
│   ├── main.py                     # Точка входа
│   ├── task.py                     # Модель Task
│   ├── task_contracts.py           # Protocol-контракт
│   ├── task_platform.py            # Платформа сбора задач
│   ├── task_sources.py             # Реализации источников задач по контракту
│   └── __init__.py
├── tests/
│   ├── test_task.py
│   ├── test_task_contracts.py
│   ├── test_task_platform.py
│   └── test_task_sources.py
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Запуск проекта

1. Клонировать репозиторий:

```shell
git clone <ссылка-на-репозиторий>
cd mai-python-lab6-protocol
```

2. Создать и активировать виртуальное окружение:

```shell
python -m venv .venv
.venv\Scripts\activate
```

3. Установить зависимости:

```shell
pip install -r requirements.txt
```

Если `requirements.txt` пустой, можно установить напрямую:

```shell
pip install attrs requests pytest
```

4. Запуск программы:

```shell
python -m src.main
```

Программа зарегистрирует источники, соберет задачи и выведет их в консоль.

## Тесты
Написано 17 тестов. Для запуска тестов:

```shell
pytest tests -vv
```

