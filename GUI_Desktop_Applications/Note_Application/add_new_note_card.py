"""
Application: Note Application
Author: Istvan Godeny
Date: 14/07/2025
License: MIT License
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit,
                               QTextEdit, QHBoxLayout, QPushButton, QMessageBox)
from PySide6.QtGui import QFont

class AddNewNoteCard(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Note")
        self.resize(320, 240)

        self._setup_ui_add_new_note_card()

    def _setup_ui_add_new_note_card(self):
        layout_add_new_note_card = QVBoxLayout()

        label_new_note_card_title = QLabel("Title:")
        label_new_note_card_title.setStyleSheet("font-family: Roboto Mono;"
                                                "font-weight: bold;"
                                                "font-size: 15px;")

        self.line_edit_new_note_card_title = QLineEdit()
        self.line_edit_new_note_card_title.setStyleSheet("font-family: Roboto Mono;"
                                                    "font-weight: normal;"
                                                    "font-size: 12px;")

        label_new_note_card_content = QLabel("Content:")
        label_new_note_card_content.setStyleSheet("font-family: Roboto Mono;"
                                                  "font-weight: bold;"
                                                  "font-size: 15px;")

        self.text_edit_new_note_card_content = QTextEdit()
        self.text_edit_new_note_card_content.setStyleSheet("font-family: Roboto Mono;"
                                                      "font-weight: normal;"
                                                      "font-size: 12px;")

        layout_buttons = QHBoxLayout()

        btn_save = QPushButton("Save")
        btn_save.setFont(QFont("Roboto Mono", 12))
        btn_save.setStyleSheet("font-weight: bold")
        btn_save.setMinimumSize(200, 30)
        btn_save.setMaximumSize(200, 50)
        btn_save.clicked.connect(self.save_new_note)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFont(QFont("Roboto Mono", 12))
        btn_cancel.setStyleSheet("font-weight: bold")
        btn_cancel.setMinimumSize(200, 30)
        btn_cancel.setMaximumSize(200, 50)
        btn_cancel.clicked.connect(self.close)

        layout_buttons.addWidget(btn_save)
        layout_buttons.addWidget(btn_cancel)

        layout_add_new_note_card.addWidget(label_new_note_card_title)
        layout_add_new_note_card.addWidget(self.line_edit_new_note_card_title)
        layout_add_new_note_card.addWidget(label_new_note_card_content)
        layout_add_new_note_card.addWidget(self.text_edit_new_note_card_content)
        layout_add_new_note_card.addLayout(layout_buttons)

        self.setLayout(layout_add_new_note_card)


    # Save the new card, send all input to the main_window.open_
    def save_new_note(self):
        # Check for empty inputs
        if not self.line_edit_new_note_card_title.text().strip():
            QMessageBox.warning(self, "Missing Title", "Please enter a title for the note.")
            return

        self.accept()


    # Warning for cancel
    def closeEvent(self, event):
        confirm = QMessageBox.question(self, "Discard New Note",
                                       "Are you sure you want to discard this new note?")
        if confirm == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
