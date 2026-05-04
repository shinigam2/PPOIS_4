import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.main.settings import setup_exchange
from src.interface.cli_menu import ExchangeCLI

def main():
    manager, platform, trader = setup_exchange()
    
    cli = ExchangeCLI(manager, platform, trader)
    cli.run()

if __name__ == "__main__":
    main()