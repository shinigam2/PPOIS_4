import sys
from PySide6.QtWidgets import QApplication
from views.main_window import MainWindow

def main():
    # Создаем объект приложения
    app = QApplication(sys.argv)
    
    # Создаем и показываем наше главное окно
    window = MainWindow()
    window.show()
    
    # Запускаем бесконечный цикл обработки событий
    sys.exit(app.exec())

if __name__ == "__main__":
    main()