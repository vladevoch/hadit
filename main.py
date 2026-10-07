import sys
import datetime
from abc import ABC, abstractmethod
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QListWidget, QComboBox, QSpinBox,
    QCheckBox, QMessageBox, QGroupBox, QFormLayout
)

class CustomMap:
    def __init__(self):
        self._keys, self._values = [], []

    def put(self, key, value):
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key):
        return self._values[self._keys.index(key)] if key in self._keys else None

    def __str__(self):
        return str({k: v for k, v in zip(self._keys, self._values)})


class BaseEntity(ABC):
    @abstractmethod
    def get_info(self):
        pass


class Habit(BaseEntity):
    def __init__(self, name, frequency, target_days):
        self._name = name
        self._frequency = frequency
        self._target_days = target_days
        self._completed_days = 0

    @property
    def name(self): return self._name
    @name.setter
    def name(self, value): self._name = value

    @property
    def frequency(self): return self._frequency
    @frequency.setter
    def frequency(self, value): self._frequency = value

    @property
    def target_days(self): return self._target_days
    @target_days.setter
    def target_days(self, value): self._target_days = value

    @property
    def completed_days(self): return self._completed_days
    @completed_days.setter
    def completed_days(self, value): self._completed_days = value

    def __str__(self):
        return f"{self._name} ({self._frequency}) - {self._completed_days}/{self._target_days} дн."

    def __repr__(self):
        return f"Habit('{self._name}', '{self._frequency}', {self._target_days})"

    def __eq__(self, other):
        return isinstance(other, Habit) and self._name == other._name and self._frequency == other._frequency

    def get_info(self):
        return f"Привычка: {self._name}, Цель: {self._target_days} дней"


class User(BaseEntity):
    def __init__(self, login):
        self._login = login
        self._habits = []
        self._time_in = datetime.datetime.now()
        self._time_out = None

    @property
    def login(self): return self._login
    @login.setter
    def login(self, value): self._login = value

    @property
    def habits(self): return self._habits
    @habits.setter
    def habits(self, value): self._habits = value

    @property
    def time_in(self): return self._time_in

    @property
    def time_out(self): return self._time_out
    @time_out.setter
    def time_out(self, value): self._time_out = value

    def add_habit(self, habit):
        self._habits.append(habit)

    def __str__(self):
        return f"User({self._login})"

    def __eq__(self, other):
        return isinstance(other, User) and self._login == other._login

    def get_info(self):
        return f"Пользователь: {self._login}"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker App")
        self.resize(800, 600)
        self.users_list = []
        self.current_user = None
        self.init_ui()

    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        auth_group = QGroupBox("Авторизация")
        auth_layout = QHBoxLayout()
        self.lbl_login = QLabel("Логин:")
        self.input_login = QLineEdit()
        self.input_login.setPlaceholderText("Введите имя пользователя")
        self.btn_login = QPushButton("Войти / Создать")
        self.btn_login.clicked.connect(self.handle_login)
        auth_layout.addWidget(self.lbl_login)
        auth_layout.addWidget(self.input_login)
        auth_layout.addWidget(self.btn_login)
        auth_group.setLayout(auth_layout)
        main_layout.addWidget(auth_group)

        add_group = QGroupBox("Добавить привычку")
        add_layout = QFormLayout()
        self.input_habit_name = QLineEdit()
        self.input_habit_name.setPlaceholderText("Название привычки")
        self.combo_freq = QComboBox()
        self.combo_freq.addItems(["Ежедневно", "Еженедельно", "Ежемесячно"])
        self.spin_days = QSpinBox()
        self.spin_days.setRange(1, 365)
        self.spin_days.setValue(30)
        self.chk_important = QCheckBox("Важная привычка")
        self.btn_add_habit = QPushButton("Добавить")
        self.btn_add_habit.clicked.connect(self.handle_add_habit)
        add_layout.addRow("Название:", self.input_habit_name)
        add_layout.addRow("Периодичность:", self.combo_freq)
        add_layout.addRow("Цель (дней):", self.spin_days)
        add_layout.addRow("", self.chk_important)
        add_layout.addRow("", self.btn_add_habit)
        add_group.setLayout(add_layout)
        main_layout.addWidget(add_group)

        list_group = QGroupBox("Мои привычки")
        list_layout = QVBoxLayout()
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.show_habit_info)
        self.btn_complete = QPushButton("Отметить выполнение")
        self.btn_complete.clicked.connect(self.handle_complete_habit)
        list_layout.addWidget(self.list_widget)
        list_layout.addWidget(self.btn_complete)
        list_group.setLayout(list_layout)
        main_layout.addWidget(list_group)

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Готов к работе")

    def handle_login(self):
        login = self.input_login.text().strip()
        if not login:
            QMessageBox.warning(self, "Ошибка", "Введите логин!")
            return
        found = next((u for u in self.users_list if u.login == login), None)
        if found:
            self.current_user = found
            self.status_bar.showMessage(f"С возвращением, {login}!")
        else:
            self.current_user = User(login)
            self.users_list.append(self.current_user)
            self.status_bar.showMessage(f"Создан новый пользователь: {login}")
        self.refresh_habit_list()
        self.input_login.clear()

    def handle_add_habit(self):
        if not self.current_user:
            QMessageBox.warning(self, "Ошибка", "Сначала войдите в систему!")
            return
        name = self.input_habit_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Ошибка", "Введите название привычки!")
            return
        habit = Habit(name, self.combo_freq.currentText(), self.spin_days.value())
        self.current_user.add_habit(habit)
        self.refresh_habit_list()
        self.input_habit_name.clear()
        self.chk_important.setChecked(False)
        self.status_bar.showMessage(f"Привычка '{name}' добавлена!")

    def handle_complete_habit(self):
        if not self.current_user:
            return
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "Ошибка", "Выберите привычку из списка!")
            return
        for habit in self.current_user.habits:
            if str(habit) == item.text():
                if habit.completed_days < habit.target_days:
                    habit.completed_days += 1
                    self.refresh_habit_list()
                    self.status_bar.showMessage(f"Прогресс обновлен: {habit.name}")
                else:
                    QMessageBox.information(self, "Инфо", "Цель уже достигнута!")
                break

    def refresh_habit_list(self):
        self.list_widget.clear()
        if self.current_user:
            for habit in self.current_user.habits:
                self.list_widget.addItem(str(habit))

    def show_habit_info(self, item):
        if self.current_user:
            for habit in self.current_user.habits:
                if str(habit) == item.text():
                    QMessageBox.information(self, "Информация", habit.get_info())
                    break

    def closeEvent(self, event):
        lines = [
            "+" + "-"*15 + "+" + "-"*22 + "+" + "-"*22 + "+",
            "| {:^13} | {:^20} | {:^20} |".format("login", "time_in", "time_out"),
            "+" + "-"*15 + "+" + "-"*22 + "+" + "-"*22 + "+"
        ]
        fmt = "%d.%m.%y %H:%M:%S"
        for user in self.users_list:
            if user.time_out is None:
                user.time_out = datetime.datetime.now()
            lines.append("| {:^13} | {:^20} | {:^20} |".format(
                user.login, user.time_in.strftime(fmt), user.time_out.strftime(fmt)))
            lines.append("+" + "-"*15 + "+" + "-"*22 + "+" + "-"*22 + "+")
        try:
            with open("report.txt", "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        except Exception as e:
            print(f"Ошибка сохранения отчета: {e}")
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
