import sys
import os

# Добавляем корневую папку проекта в sys.path, чтобы Python видел пакет src
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.main.settings import setup_exchange
from src.interface.cli_menu import ExchangeCLI

def main():
    # Получаем настроенные объекты
    manager, platform, trader = setup_exchange()
    
    # Запускаем интерфейс
    cli = ExchangeCLI(manager, platform, trader)
    cli.run()

if __name__ == "__main__":
    main()