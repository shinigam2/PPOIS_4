from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QSpinBox, QDialogButtonBox, QTabWidget, QWidget
)

class DeleteDialog(QDialog):
    def __init__(self, parent, unique_sports: list, unique_ranks: list):
        super().__init__(parent)
        self.setWindowTitle("Удаление записей")
        self.resize(350, 250)

        self.layout = QVBoxLayout(self)
        self.tabs = QTabWidget()
        
        # Вкладка 1: По ФИО ИЛИ виду спорта
        self.tab1 = QWidget()
        form1 = QFormLayout(self.tab1)
        self.edit_name1 = QLineEdit()
        self.combo_sport = QComboBox()
        self.combo_sport.addItem("")
        self.combo_sport.addItems(unique_sports)
        form1.addRow("ФИО (содержит):", self.edit_name1)
        form1.addRow("Вид спорта:", self.combo_sport)
        self.tabs.addTab(self.tab1, "По ФИО или Спорту")

        # Вкладка 2: По титулам
        self.tab2 = QWidget()
        form2 = QFormLayout(self.tab2)
        self.spin_min_titles = QSpinBox()
        self.spin_max_titles = QSpinBox()
        self.spin_max_titles.setValue(100)
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

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_delete_params(self) -> dict:
        current_tab = self.tabs.currentIndex()
        if current_tab == 0:
            return {"full_name": self.edit_name1.text(), "sport_type": self.combo_sport.currentText()}
        elif current_tab == 1:
            return {"min_titles": self.spin_min_titles.value(), "max_titles": self.spin_max_titles.value()}
        elif current_tab == 2:
            return {"full_name": self.edit_name3.text(), "rank": self.combo_rank.currentText()}
        return {}