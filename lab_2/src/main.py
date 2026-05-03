import sys
from PySide6.QtWidgets import QApplication

from models.model import AthleteModel
from views.main_window import MainWindow
from controllers.main_controller import MainController

def main():
    app = QApplication(sys.argv)
    
    # 1. Создаем Модель
    model = AthleteModel()
    
    # 2. Создаем Главное Окно (View)
    view = MainWindow()
    
    # 3. Создаем Контроллер и передаем ему Модель и View
    controller = MainController(view, model)
    
    # Показываем интерфейс
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()