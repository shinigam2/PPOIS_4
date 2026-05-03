from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit, 
    QComboBox, QSpinBox, QDialogButtonBox
)

class AddAthleteDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить спортсмена")
        self.resize(300, 250)

        self.layout = QVBoxLayout(self)
        self.form_layout = QFormLayout()

        # Поля для ввода данных
        self.edit_name = QLineEdit()
        
        self.combo_roster = QComboBox()
        self.combo_roster.addItems(["основной", "запасной", "n/a"])
        
        self.edit_position = QLineEdit()
        
        # QSpinBox гарантирует, что пользователь введет только целое число!
        self.spin_titles = QSpinBox()
        self.spin_titles.setRange(0, 1000) 
        
        self.edit_sport = QLineEdit()
        
        self.combo_rank = QComboBox()
        self.combo_rank.addItems([
            "1-й юношеский", "2-й разряд", "3-й разряд", 
            "кмс", "мастер спорта"
        ])

        # Добавляем поля на форму
        self.form_layout.addRow("ФИО:", self.edit_name)
        self.form_layout.addRow("Состав:", self.combo_roster)
        self.form_layout.addRow("Позиция:", self.edit_position)
        self.form_layout.addRow("Титулы:", self.spin_titles)
        self.form_layout.addRow("Вид спорта:", self.edit_sport)
        self.form_layout.addRow("Разряд:", self.combo_rank)

        self.layout.addLayout(self.form_layout)

        # Стандартные кнопки ОК и Отмена
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

    def get_data(self) -> dict:
        """Возвращает данные из формы в виде словаря"""
        return {
            "full_name": self.edit_name.text().strip(),
            "roster_status": self.combo_roster.currentText(),
            "position": self.edit_position.text().strip(),
            "titles_count": self.spin_titles.value(),
            "sport_type": self.edit_sport.text().strip(),
            "rank": self.combo_rank.currentText()
        }