from PySide6.QtWidgets import QFileDialog, QMessageBox
from views.main_window import MainWindow
from models.model import AthleteModel, Athlete
from views.add_dialog import AddAthleteDialog
from views.search_dialog import SearchDialog
from views.delete_dialog import DeleteDialog

class MainController:
    def __init__(self, view: MainWindow, model: AthleteModel):
        self.view = view
        self.model = model
        
        # Настройки пагинации
        self.current_page = 1
        self.items_per_page = int(self.view.combo_items_per_page.currentText())

        self._connect_signals()
        self.update_table_view()

    def _connect_signals(self):
        """Связываем сигналы от кнопок UI с методами контроллера"""
        # Меню и Тулбар
        self.view.action_add.triggered.connect(self.handle_add_record)
        self.view.action_save.triggered.connect(self.handle_save_file)
        self.view.action_load.triggered.connect(self.handle_load_file)
        self.view.action_search.triggered.connect(self.handle_search)
        self.view.action_delete.triggered.connect(self.handle_delete)
        
        # Сигналы пагинации
        self.view.btn_next.clicked.connect(self.next_page)
        self.view.btn_prev.clicked.connect(self.prev_page)
        self.view.btn_first.clicked.connect(self.first_page)
        self.view.btn_last.clicked.connect(self.last_page)
        self.view.combo_items_per_page.currentTextChanged.connect(self.change_items_per_page)

    def update_table_view(self):
        """Получает нужную страницу из Модели и передает во View"""
        total_pages = self.model.get_total_pages(self.items_per_page)
        
        # Защита от выхода за пределы страниц
        if self.current_page > total_pages and total_pages > 0:
            self.current_page = total_pages
        elif self.current_page < 1:
            self.current_page = 1

        # Получаем данные для текущей страницы
        page_data = self.model.get_page(self.current_page, self.items_per_page)
        
        # Обновляем UI
        self.view.populate_table(page_data)
        self.view.update_pagination_labels(
            self.current_page, 
            total_pages, 
            self.model.get_total_count()
        )

    # --- Обработчики действий ---

    def handle_add_record(self):
        dialog = AddAthleteDialog(self.view)
        if dialog.exec():  # Если нажали "ОК"
            data = dialog.get_data()
            if not data["full_name"] or not data["sport_type"]:
                QMessageBox.warning(self.view, "Ошибка", "ФИО и Вид спорта не могут быть пустыми!")
                return
            
            # Создаем объект и добавляем в модель
            new_athlete = Athlete(**data)
            self.model.add_athlete(new_athlete)
            
            # Обновляем таблицу (переходим на последнюю страницу, чтобы увидеть добавленное)
            self.last_page() 

    def handle_save_file(self):
        filepath, _ = QFileDialog.getSaveFileName(self.view, "Сохранить файл", "", "XML Files (*.xml)")
        if filepath:
            self.model.save_to_file(filepath)
            QMessageBox.information(self.view, "Успех", "Данные успешно сохранены.")

    def handle_load_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self.view, "Открыть файл", "", "XML Files (*.xml)")
        if filepath:
            self.model.load_from_file(filepath)
            self.current_page = 1
            self.update_table_view()

    # --- Методы пагинации ---

    def next_page(self):
        total_pages = self.model.get_total_pages(self.items_per_page)
        if self.current_page < total_pages:
            self.current_page += 1
            self.update_table_view()

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_table_view()

    def first_page(self):
        self.current_page = 1
        self.update_table_view()

    def last_page(self):
        self.current_page = self.model.get_total_pages(self.items_per_page)
        if self.current_page == 0:
            self.current_page = 1
        self.update_table_view()

    def change_items_per_page(self, text):
        self.items_per_page = int(text)
        self.current_page = 1  # Сбрасываем на первую страницу
        self.update_table_view()

    def _get_unique_dropdown_data(self):
        """Вспомогательный метод для сбора уникальных видов спорта и разрядов (Требование задания)"""
        all_athletes = self.model.get_all()
        # Используем set, чтобы убрать дубликаты
        unique_sports = list(set([a.sport_type for a in all_athletes if a.sport_type]))
        unique_ranks = list(set([a.rank for a in all_athletes if a.rank]))
        return sorted(unique_sports), sorted(unique_ranks)

    def handle_search(self):
        # 1. Собираем уникальные данные из модели
        sports, ranks = self._get_unique_dropdown_data()
        
        # 2. Создаем диалог
        dialog = SearchDialog(self.view, sports, ranks)
        
        # 3. Определяем, что делать при нажатии кнопки "Найти" внутри диалога
        def perform_search():
            params = dialog.get_search_params()
            results = self.model.search(**params) # Вызываем универсальный метод поиска из Модели
            dialog.set_results(results) # Передаем результаты обратно в диалог для отображения
            
        dialog.btn_search.clicked.connect(perform_search)
        
        # Запускаем окно (оно не закроется, пока пользователь сам не нажмет крестик)
        dialog.exec()

    def handle_delete(self):
        sports, ranks = self._get_unique_dropdown_data()
        dialog = DeleteDialog(self.view, sports, ranks)
        
        if dialog.exec(): # Если пользователь нажал "ОК"
            params = dialog.get_delete_params()
            
            # Сначала ИЩЕМ записи, которые подходят под критерии
            records_to_delete = self.model.search(**params)
            
            if not records_to_delete:
                QMessageBox.information(self.view, "Отчет", "Записи по заданным условиям не найдены.")
                return
                
            # Просим модель УДАЛИТЬ найденные записи
            deleted_count = self.model.delete_records(records_to_delete)
            
            # Строгое требование задания: сообщить, сколько было удалено
            QMessageBox.information(self.view, "Успех", f"Успешно удалено записей: {deleted_count}")
            
            # Обновляем главную таблицу
            self.update_table_view()