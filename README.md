# Habit Tracker App

Учебное десктопное приложение для отслеживания привычек на Python и PyQt6.

## Возможности
- вход/создание пользователя;
- добавление привычек;
- выбор периодичности;
- цель от 1 до 365 дней;
- отметка выполнения;
- просмотр информации о привычке;
- сохранение отчёта в `report.txt`.

## Технологии
- Python 3.10+
- PyQt6
- ООП
- ABC / абстрактный класс
- наследование
- `@property`
- `__str__`, `__repr__`, `__eq__`
- коллекции `list`
- пользовательский `CustomMap`

## Запуск

```bash
python -m pip install -r requirements.txt
python main.py
```

После закрытия приложения создаётся `report.txt`.

## Структура

```text
habit-tracker-pyqt6/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```
