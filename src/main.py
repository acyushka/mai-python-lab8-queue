from src.constants import DEFAULT_GENERATED_COUNT, DEMO_TASKS_FILEPATH
from src.task_platform import TaskPlatform
from src.task_sources import ApiTaskSource, FileTaskSource, GeneratorTaskSource


def main() -> None:
    """
    Точка входа в программу. Создает платформу, регистрирует источники задач и собирает задачи для обработки
    """

    platform = TaskPlatform()

    generator_source = GeneratorTaskSource(
        count=DEFAULT_GENERATED_COUNT, prefix="demo")
    api_source = ApiTaskSource()
    file_source = FileTaskSource(filepath=DEMO_TASKS_FILEPATH)

    print("\n=== Регистрация источников ===")
    try:
        platform.add_source(file_source)
        platform.add_source(generator_source)
        platform.add_source(api_source)
        print(f"\nЗарегистрировано источников: {platform.source_count}")
    except (TypeError, ValueError) as error:
        print(f"Ошибка: {error}")
        return

    print("\n=== Сбор задач ===")
    try:
        tasks = platform.collect_all_tasks()
    except (FileNotFoundError, ValueError) as error:
        print(f"Ошибка при сборе задач: {error}")
        return

    for task in tasks:
        print(f"\n[{task.id}] payload={task.payload}")

    print(f"\nВсего задач: {len(tasks)}")


if __name__ == "__main__":
    main()
