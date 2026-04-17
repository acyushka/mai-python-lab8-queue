# Лабораторная работа №3: Очередь задач (итераторы и генераторы)

## Введение

В проекте реализована очередь задач `TaskQueue` с поддержкой итерации, ленивых фильтров и потоковой обработки.
Все источники работают через один контракт `TaskSource` (`Protocol` + `runtime_checkable`).

Платформа собирает задачи из нескольких источников, очередь дает такие возможности:
- **Итерацию** через благодаря dunder методам `__iter__` и `__len__`
- **Ленивые фильтры** на основе генераторов (по статусу, приоритету, готовности)
- **Экономную работу** с большими объемами данных через `yield` в источниках

Реализованы 3 источника задач:
- `FileTaskSource` (читает из JSON-файла, возвращает генератор)
- `GeneratorTaskSource` (программно генерирует задачи через `yield`)
- `ApiTaskSource` (получает вакансии с hh.ru API, обрабатывает ошибки)

## Архитектура проекта

```shell
mai-python-lab6-protocol/
├── data/
│   └── tasks.json                  # Пример задач для FileTaskSource
├── src/
│   ├── constants.py                # Константы
│   ├── main.py                     # Точка входа
│   ├── task.py                     # Модель Task с дескрипторами
│   ├── task_contracts.py           # Protocol-контракт TaskSource
│   ├── task_queue.py               # Очередь задач с итераторами и ленивыми фильтрами
│   ├── task_platform.py            # Платформа сбора задач из источников
│   ├── task_sources.py             # Реализации источников (File, Generator, Api)
│   └── __init__.py
├── tests/
│   ├── test_task.py
│   ├── test_task_contracts.py
│   ├── test_task_queue.py
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

3. Установить зависимости через uv

4. Запуск программы:

```shell
python -m src.main
```

Программа зарегистрирует источники, соберет задачи и выведет их в консоль.

## Тесты
Написано 30 тестов. Для запуска:

```shell
pytest tests -vv
```

