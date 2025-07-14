"""
Application: Note Application
Author: Istvan Godeny
Date: 14/07/2025
License: MIT License
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                               QHBoxLayout, QPushButton, QTextEdit, QMessageBox)
from PySide6.QtGui import QFont

class EditNoteCard(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit Note")
        self.resize(320, 240)

        self._setup_ui_edit_note_card()


    def _setup_ui_edit_note_card(self):
        layout_edit_note_card = QVBoxLayout()

        label_edit_note_card_title = QLabel("Title:")
        label_edit_note_card_title.setStyleSheet("font-family: Roboto Mono;"
                                                "font-weight: bold;"
                                                "font-size: 15px;")

        self.line_edit_edit_note_card_title = QLineEdit()
        self.line_edit_edit_note_card_title.setStyleSheet("font-family: Roboto Mono;"
                                                    "font-weight: normal;"
                                                    "font-size: 12px;")

        label_edit_note_card_content = QLabel("Content:")
        label_edit_note_card_content.setStyleSheet("font-family: Roboto Mono;"
                                                  "font-weight: bold;"
                                                  "font-size: 15px;")

        self.text_edit_edit_note_card_content = QTextEdit()
        self.text_edit_edit_note_card_content.setStyleSheet("font-family: Roboto Mono;"
                                                      "font-weight: normal;"
                                                      "font-size: 12px;")

        layout_buttons = QHBoxLayout()

        btn_save = QPushButton("Save")
        btn_save.setFont(QFont("Roboto Mono", 12))
        btn_save.setStyleSheet("font-weight: bold")
        btn_save.setMinimumSize(200, 30)
        btn_save.setMaximumSize(200, 50)
        btn_save.clicked.connect(self.save_edited_note)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFont(QFont("Roboto Mono", 12))
        btn_cancel.setStyleSheet("font-weight: bold")
        btn_cancel.setMinimumSize(200, 30)
        btn_cancel.setMaximumSize(200, 50)
        btn_cancel.clicked.connect(self.close)

        layout_buttons.addWidget(btn_save)
        layout_buttons.addWidget(btn_cancel)

        layout_edit_note_card.addWidget(label_edit_note_card_title)
        layout_edit_note_card.addWidget(self.line_edit_edit_note_card_title)
        layout_edit_note_card.addWidget(label_edit_note_card_content)
        layout_edit_note_card.addWidget(self.text_edit_edit_note_card_content)
        layout_edit_note_card.addLayout(layout_buttons)

        self.setLayout(layout_edit_note_card)


    # Send all changes to the main window
    def save_edited_note(self):
        self.accept()

    # Warning for cancel
    def closeEvent(self, event):
        confirm = QMessageBox.question(self, "Discard Changes",
                                       "Are you sure you want to discard the changes?")
        if confirm == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()