import sys
import json
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QGridLayout, QListWidget, QPushButton, QLineEdit

class WeeklyPlanner(QMainWindow):
    def __init__(self):
        super().__init__()

        # Main window setup
        self.setWindowTitle("Weekly Planner")
        self.setGeometry(100, 100, 1200, 600)  # x, y, width, height

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QGridLayout(central_widget)

        # Define the columns
        columns = ["To Do", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        self.task_lists = []
        self.add_buttons = []
        self.task_inputs = []

        # Create labels, lists, and buttons for each day
        for index, day in enumerate(columns):
            label = QLabel(day)
            layout.addWidget(label, 0, index)  # row, column

            # Task list widget
            task_list = QListWidget()
            layout.addWidget(task_list, 1, index)
            self.task_lists.append(task_list)

            # Input field for new task
            task_input = QLineEdit("Enter a new task")
            layout.addWidget(task_input, 2, index)
            self.task_inputs.append(task_input)

            # Add button
            add_button = QPushButton("Add Task")
            layout.addWidget(add_button, 3, index)
            self.add_buttons.append(add_button)
            add_button.clicked.connect(lambda checked, idx=index: self.add_task(idx))

            # Remove button
            remove_button = QPushButton("Remove Selected Task")
            layout.addWidget(remove_button, 4, index)
            remove_button.clicked.connect(lambda checked, idx=index: self.remove_task(idx))

        self.load_tasks()

    def add_task(self, column_index):
        task_input = self.task_inputs[column_index]
        task_list = self.task_lists[column_index]
        task_text = task_input.text()
        if task_text:  # Ensure non-empty task text
            task_list.addItem(task_text)
            task_input.clear()
            self.save_tasks()

    def remove_task(self, column_index):
        task_list = self.task_lists[column_index]
        list_items = task_list.selectedItems()
        if not list_items: return
        for item in list_items:
            task_list.takeItem(task_list.row(item))
        self.save_tasks()

    def save_tasks(self):
        tasks = {}
        for index, task_list in enumerate(self.task_lists):
            tasks[index] = [task_list.item(i).text() for i in range(task_list.count())]
        with open('tasks.json', 'w') as file:
            json.dump(tasks, file)

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks = json.load(file)
            for index, task_items in tasks.items():
                try:
                    list_index = int(index)  # Ensure the index can be converted to an integer
                except ValueError:
                    continue  # Skip this key if it's not an integer
                for item in task_items:
                    self.task_lists[list_index].addItem(item)
        except FileNotFoundError:
            pass  # No tasks file exists yet, nothing to load
        except json.JSONDecodeError:
            print("Error decoding JSON from file.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeeklyPlanner()
    window.show()
    sys.exit(app.exec())
