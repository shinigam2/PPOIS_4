from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QSpinBox, QPushButton, QTableWidget, 
    QTableWidgetItem, QHeaderView, QLabel, QTabWidget, QWidget, QMessageBox
)
from PySide6.QtCore import Qt

class SearchDialog(QDialog):
    def __init__(self, parent, unique_sports: list, unique_ranks: list):
        super().__init__(parent)
        self.setWindowTitle("Поиск спортсменов")
        self.resize(700, 500)

        # Данные для пагинации
        self.search_results = []
        self.current_page = 1
        self.items_per_page = 10

        self.layout = QVBoxLayout(self)

        # --- 1. Вкладки с условиями поиска ---
        self.tabs = QTabWidget()
        
        # Вкладка 1: По ФИО ИЛИ виду спорта
        self.tab1 = QWidget()
        form1 = QFormLayout(self.tab1)
        self.edit_name1 = QLineEdit()
        self.combo_sport = QComboBox()
        self.combo_sport.addItem("") # Пустой пункт
        self.combo_sport.addItems(unique_sports)
        form1.addRow("ФИО (содержит):", self.edit_name1)
        form1.addRow("Вид спорта:", self.combo_sport)
        self.tabs.addTab(self.tab1, "По ФИО или Спорту")

        # Вкладка 2: По количеству титулов (диапазон)
        self.tab2 = QWidget()
        form2 = QFormLayout(self.tab2)
        self.spin_min_titles = QSpinBox()
        self.spin_max_titles = QSpinBox()
        self.spin_max_titles.setValue(100) # Значение по умолчанию
        form2.addRow("Минимум титулов:", self.spin_min_titles)
        form2.addRow("Максимум титулов:", self.spin_max_titles)
        self.tabs.addTab(self.tab2, "По титулам")

        # Вкладка 3: По ФИО ИЛИ разряду
        self.tab3 = QWidget()
        form3 = QFormLayout(self.tab3)
        self.edit_name3 = QLineEdit()
        self.combo_rank = QComboBox()
        self.combo_rank.addItem("")
        self.combo_rank.addItems(unique_ranks)
        form3.addRow("ФИО (содержит):", self.edit_name3)
        form3.addRow("Разряд:", self.combo_rank)
        self.tabs.addTab(self.tab3, "По ФИО или Разряду")

        self.layout.addWidget(self.tabs)

        # Кнопка Искать
        self.btn_search = QPushButton("Найти")
        self.layout.addWidget(self.btn_search)

        # --- 2. Таблица результатов ---
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ФИО", "Состав", "Позиция", "Титулы", "Вид спорта", "Разряд"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout.addWidget(self.table)

        # --- 3. Панель пагинации ---
        pagination_layout = QHBoxLayout()
        self.btn_prev = QPushButton("< Пред.")
        self.btn_next = QPushButton("След. >")
        self.lbl_page_info = QLabel("Страница: 0 / 0 | Найдено: 0")
        
        pagination_layout.addWidget(self.btn_prev)
        pagination_layout.addWidget(self.lbl_page_info)
        pagination_layout.addWidget(self.btn_next)
        self.layout.addLayout(pagination_layout)

        # Подключение кнопок пагинации (будут работать с локальным массивом search_results)
        self.btn_prev.clicked.connect(self.prev_page)
        self.btn_next.clicked.connect(self.next_page)

    def get_search_params(self) -> dict:
        """Возвращает параметры в зависимости от активной вкладки"""
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            return {"full_name": self.edit_name1.text(), "sport_type": self.combo_sport.currentText()}
        elif current_tab == 1:
            return {"min_titles": self.spin_min_titles.value(), "max_titles": self.spin_max_titles.value()}
        elif current_tab == 2:
            return {"full_name": self.edit_name3.text(), "rank": self.combo_rank.currentText()}
        return {}

    # --- Логика пагинации ВНУТРИ диалога ---
    def set_results(self, results: list):
        """Контроллер передает сюда найденный массив"""
        self.search_results = results
        self.current_page = 1
        self.update_table()

    def update_table(self):
        total_records = len(self.search_results)
        total_pages = (total_records + self.items_per_page - 1) // self.items_per_page if total_records > 0 else 1
        
        self.table.setRowCount(0)
        start_idx = (self.current_page - 1) * self.items_per_page
        end_idx = start_idx + self.items_per_page
        page_data = self.search_results[start_idx:end_idx]

        for row_idx, athlete in enumerate(page_data):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(athlete.full_name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(athlete.roster_status))
            self.table.setItem(row_idx, 2, QTableWidgetItem(athlete.position))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(athlete.titles_count)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(athlete.sport_type))
            self.table.setItem(row_idx, 5, QTableWidgetItem(athlete.rank))

        self.lbl_page_info.setText(f"Страница: {self.current_page} / {total_pages} | Найдено: {total_records}")

    def next_page(self):
        total_pages = (len(self.search_results) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_table()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table()