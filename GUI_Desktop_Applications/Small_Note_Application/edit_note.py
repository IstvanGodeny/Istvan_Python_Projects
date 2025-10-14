"""
Application: Small Note Application
Author: Istvan Godeny
Date: 07/07/2025
License: MIT License
"""

from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                               QLabel, QFrame, QSizePolicy, QTextEdit, QMessageBox, QLineEdit)
from PySide6.QtGui import QFont, QTextOption, QKeyEvent
from PySide6.QtCore import Signal, Qt


# Disabled Enter in text edit
class SingleLineTextEdit(QTextEdit):
    def keyPressEvent(self, event: QKeyEvent):
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            return
        super().keyPressEvent(event)



class EditNote(QDialog):
    signal_edit_note = Signal(str, str)


    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add New Note")
        self.resize(480, 360)

        self._add_new_note_layout = QVBoxLayout()
        self.setLayout(self._add_new_note_layout)

        self._setup_ui_add_new_note()


    def _setup_ui_add_new_note(self):
        label_title = QLabel("Edit Note")
        label_title.setFrameShape(QFrame.WinPanel)
        label_title.setFrameShadow(QFrame.Sunken)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(QFont("Roboto Mono", 17))

        label_note_title = QLabel("Note's Title:")
        label_note_title.setFont(QFont("Roboto Mono", 12))

        self.line_edit_note_title = QLineEdit()
        self.line_edit_note_title.setFont(QFont("Roboto Mono", 12))

        label_note = QLabel("Note:")
        label_note.setFont(QFont("Roboto Mono", 12))

        # self.text_edit_note = SingleLineTextEdit()
        self.text_edit_note = QTextEdit()
        self.text_edit_note.setFont(QFont("Roboto Mono", 10))
        self.text_edit_note.setAlignment(Qt.AlignTop)
        self.text_edit_note.setWordWrapMode(QTextOption.WordWrap)
        self.text_edit_note.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout_btn = QHBoxLayout()
        layout_btn.setContentsMargins(10, 0, 10, 0)
        layout_btn.setSpacing(10)

        btn_add_new_note = QPushButton("Save Note", default=True)
        btn_add_new_note.setFont(QFont("Roboto Mono", 12))
        btn_add_new_note.setMinimumSize(0, 30)
        btn_add_new_note.clicked.connect(self.save_note)

        btn_exit_edit_note_window = QPushButton("Exit")
        btn_exit_edit_note_window.setFont(QFont("Roboto Mono", 12))
        btn_exit_edit_note_window.setMinimumSize(0, 30)
        btn_exit_edit_note_window.clicked.connect(self.confirm_exit)

        self._add_new_note_layout.addWidget(label_title)

        self._add_new_note_layout.addWidget(label_note_title)
        self._add_new_note_layout.addWidget(self.line_edit_note_title)

        self._add_new_note_layout.addWidget(label_note)
        self._add_new_note_layout.addWidget(self.text_edit_note)

        layout_btn.addWidget(btn_add_new_note)
        layout_btn.addWidget(btn_exit_edit_note_window)
        self._add_new_note_layout.addLayout(layout_btn)


    def confirm_exit(self):
        confirm = QMessageBox.question(self, "Confirm exit", "Are you sure you want to close this window without save the note? All unsaved data will be lost!")
        if confirm == QMessageBox.StandardButton.Yes:
            self.close()


    def save_note(self):
        notes_title = self.line_edit_note_title.text()
        note = self.text_edit_note.toPlainText()
        self.signal_edit_note.emit(notes_title, note)
        self.close()
