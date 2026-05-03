from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QTableWidget, QTableWidgetItem, QHeaderView, 
    QToolBar, QMenu, QPushButton, QLabel, QComboBox
)
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Справочник спортсменов (Вариант 7)")
        self.resize(900, 600)

        # Основной виджет и компоновка
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # 1. Инициализация меню и панели инструментов
        self._setup_actions()
        self._setup_menu()
        self._setup_toolbar()

        # 2. Инициализация таблицы
        self._setup_table()

        # 3. Инициализация панели пагинации
        self._setup_pagination_panel()

    def _setup_actions(self):
        """Создаем действия (QAction), которые будут общими для меню и тулбара"""
        self.action_add = QAction("Добавить", self)
        self.action_search = QAction("Поиск", self)
        self.action_delete = QAction("Удалить", self)
        self.action_save = QAction("Сохранить (XML)", self)
        self.action_load = QAction("Загрузить (XML)", self)

    def _setup_menu(self):
        """Создание выпадающего меню"""
        menu_bar = self.menuBar()
        
        file_menu = menu_bar.addMenu("Файл")
        file_menu.addAction(self.action_save)
        file_menu.addAction(self.action_load)

        edit_menu = menu_bar.addMenu("Записи")
        edit_menu.addAction(self.action_add)
        edit_menu.addAction(self.action_search)
        edit_menu.addAction(self.action_delete)

    def _setup_toolbar(self):
        """Создание панели инструментов (дублирует меню по заданию)"""
        toolbar = QToolBar("Основная панель")
        self.addToolBar(toolbar)
        
        toolbar.addAction(self.action_add)
        toolbar.addAction(self.action_search)
        toolbar.addAction(self.action_delete)
        toolbar.addSeparator()
        toolbar.addAction(self.action_save)
        toolbar.addAction(self.action_load)

    def _setup_table(self):
        """Настройка таблицы для вывода спортсменов"""
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ФИО спортсмена", "Состав", "Позиция", 
            "Титулы", "Вид спорта", "Разряд"
        ])
        
        # Растягиваем столбцы по ширине окна
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        self.main_layout.addWidget(self.table)

    def _setup_pagination_panel(self):
        """Создание панели управления страницами под таблицей"""
        pagination_layout = QHBoxLayout()

        # Кнопки навигации
        self.btn_first = QPushButton("<< Первая")
        self.btn_prev = QPushButton("< Пред.")
        self.btn_next = QPushButton("След. >")
        self.btn_last = QPushButton("Последняя >>")

        # Выбор количества записей на странице
        self.combo_items_per_page = QComboBox()
        self.combo_items_per_page.addItems(["10", "20", "50"])
        
        # Информационные метки
        self.lbl_page_info = QLabel("Страница: 1 / 1")
        self.lbl_records_info = QLabel("Записей: 0")

        # Добавляем виджеты в слой
        pagination_layout.addWidget(QLabel("Записей на странице:"))
        pagination_layout.addWidget(self.combo_items_per_page)
        pagination_layout.addStretch() # Пружина для выравнивания
        pagination_layout.addWidget(self.btn_first)
        pagination_layout.addWidget(self.btn_prev)
        pagination_layout.addWidget(self.lbl_page_info)
        pagination_layout.addWidget(self.btn_next)
        pagination_layout.addWidget(self.btn_last)
        pagination_layout.addStretch()
        pagination_layout.addWidget(self.lbl_records_info)

        self.main_layout.addLayout(pagination_layout)

    # --- Методы для обновления интерфейса Контроллером ---

    def populate_table(self, athletes):
        """Очищает таблицу и заполняет ее новыми данными (одной страницей)"""
        self.table.setRowCount(0) # Очистка
        for row_idx, athlete in enumerate(athletes):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(athlete.full_name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(athlete.roster_status))
            self.table.setItem(row_idx, 2, QTableWidgetItem(athlete.position))
            self.table.setItem(row_idx, 3, QTableWidgetItem(str(athlete.titles_count)))
            self.table.setItem(row_idx, 4, QTableWidgetItem(athlete.sport_type))
            self.table.setItem(row_idx, 5, QTableWidgetItem(athlete.rank))

    def update_pagination_labels(self, current_page, total_pages, total_records):
        """Обновляет текст информационных меток"""
        self.lbl_page_info.setText(f"Страница: {current_page} / {total_pages}")
        self.lbl_records_info.setText(f"Всего записей: {total_records}")