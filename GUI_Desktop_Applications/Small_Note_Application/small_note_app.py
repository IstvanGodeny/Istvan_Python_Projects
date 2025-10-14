"""
Application: Small Note Application
Author: Istvan Godeny
Date: 07/07/2025
License: MIT License
"""

import sys
from PySide6.QtWidgets import QApplication

from main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
