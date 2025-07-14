"""
Application: Note Application
Author: Istvan Godeny
Date: 14/07/2025
License: MIT License
"""

import sys
from PySide6.QtWidgets import QApplication
from database import init_database
from main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)

    if init_database():
        window = MainWindow()
        window.show()

        sys.exit(app.exec())
