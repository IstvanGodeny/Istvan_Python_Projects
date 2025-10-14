"""
Application: Small Note Application
Author: Istvan Godeny
Date: 07/07/2025
License: MIT License
"""

from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                               QPushButton, QFrame, QListWidget, QMessageBox, QFileDialog)
from PySide6.QtGui import QAction, QFont
from PySide6.QtCore import Qt, Slot

from add_note import AddNote
from edit_note import EditNote


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up the window parameters
        self.setWindowTitle("Small Note Application")
        self.resize(640, 480)

        # Central widget - must have for QMainWindow
        self._central_widget = QWidget()
        self._main_window_layout = QVBoxLayout()
        self._central_widget.setLayout(self._main_window_layout)
        self.setCentralWidget(self._central_widget)

        # Menu bar
        self.menubar = self.menuBar()

        ## File Menu
        self.file_menu = self.menubar.addMenu("File")
        # File --> Open action
        self.open_file_action = QAction("Open File", self)
        self.open_file_action.triggered.connect(self.open_file)
        self.file_menu.addAction(self.open_file_action)
        # File --> Save action
        self.save_file_action = QAction("Save File", self)
        self.save_file_action.triggered.connect(self.save_file)
        self.file_menu.addAction(self.save_file_action)
        self.file_menu.addSeparator()
        # File --> Exit
        self.exit_action = QAction("Exit", self)
        self.exit_action.triggered.connect(self.close)
        self.file_menu.addAction(self.exit_action)

        ## Edit Menu
        self.edit_menu = self.menubar.addMenu("Edit")
        # Edit Note --> Edit Note action
        self.edit_note_action = QAction("Edit Note", self)
        self.edit_note_action.triggered.connect(self.open_edit_note_window)
        self.edit_menu.addAction(self.edit_note_action)
        # Delete Note --> Delete Note action
        self.delete_note_action = QAction("Delete Note", self)
        self.delete_note_action.triggered.connect(self.delete_note)
        self.edit_menu.addAction(self.delete_note_action)

        self._setup_ui_main_window()

        self.add_new_note_window = None
        self.edit_note_window = None

        self.notes = {}


    def _setup_ui_main_window(self):
        self._main_window_layout.setSpacing(10)
        self._main_window_layout.setContentsMargins(10, 10, 10, 10)

        label_title = QLabel("My Notes")
        label_title.setFrameShape(QFrame.WinPanel)
        label_title.setFrameShadow(QFrame.Sunken)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(QFont("Roboto Mono", 17))

        self.list_notes = QListWidget()
        self.list_notes.setFont(QFont("Roboto Mono", 10))
        self.list_notes.setFrameShape(QFrame.WinPanel)
        self.list_notes.setFrameShadow(QFrame.Sunken)
        self.list_notes.itemDoubleClicked.connect(self.open_edit_note_window)

        layout_btn = QHBoxLayout()
        layout_btn.setContentsMargins(10,0,10,0)
        layout_btn.setSpacing(10)

        btn_open_add_new_note = QPushButton("New Note", default=True)
        btn_open_add_new_note.setFont(QFont("Roboto Mono", 12))
        btn_open_add_new_note.setMinimumSize(0, 30)
        btn_open_add_new_note.clicked.connect(self.open_add_new_note_window)

        btn_exit_app = QPushButton("Exit")
        btn_exit_app.setFont(QFont("Roboto Mono", 12))
        btn_exit_app.setMinimumSize(0, 30)
        btn_exit_app.clicked.connect(self.close)

        self._main_window_layout.addWidget(label_title)
        self._main_window_layout.addWidget(self.list_notes)
        layout_btn.addWidget(btn_open_add_new_note)
        layout_btn.addWidget(btn_exit_app)
        self._main_window_layout.addLayout(layout_btn)


    def open_add_new_note_window(self):
        self.add_new_note_window = AddNote()
        self.add_new_note_window.signal_note.connect(self.handle_note)
        self.add_new_note_window.show()


    def open_edit_note_window(self):
        selected_item = self.list_notes.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No selection", "Please select a note to edit.")
            return

        titels_note = selected_item.text()
        note = self.notes.get(titels_note, "")

        self.edit_note_window = EditNote()
        self.edit_note_window.line_edit_note_title.setText(titels_note)
        self.edit_note_window.text_edit_note.setPlainText(note)
        self.edit_note_window.signal_edit_note.connect(self.update_note)
        self.edit_note_window.show()


    @Slot(str, str)
    def handle_note(self, notes_title, note):
        self.notes[notes_title] = note
        self.refresh_note_list()

    @Slot(str, str)
    def update_note(self, notes_title, note):
        self.notes[notes_title] = note
        self.refresh_note_list()


    def refresh_note_list(self):
        current_title = self.list_notes.currentItem().text() if self.list_notes.currentItem() else None
        self.list_notes.clear()
        for title in self.notes:
            self.list_notes.addItem(title)
        if current_title and current_title in self.notes:
            items = self.list_notes.findItems(current_title, Qt.MatchExactly)
            if items:
                self.list_notes.setCurrentItem(items[0])


    def open_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Notes", "./", "JSON Files (*.json)")
        if not file:
            return

        import json
        try:
            with open(file, 'r', encoding="utf-8") as file_open:
                data = json.load(file_open)
            self.notes = data.get("notes", {})
            self.refresh_note_list()
            QMessageBox.information(self, "Success", "Notes loaded successfully.")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open file:\n{e}")


    def save_file(self):
        file, _ = QFileDialog.getSaveFileName(self, "Save Notes", "./", "JSON Files (*.json)")
        if not file:
            return

        import json
        data = {"notes": self.notes}
        try:
            with open(file, "w", encoding="utf-8") as file_save:
                json.dump(data, file_save, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Success", "Notes saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save notes:\n{e}")


    def delete_note(self):
        selected_note = self.list_notes.currentItem()
        if not selected_note:
            QMessageBox.warning(self, "No selection", "Please select a note to delete.")
            return

        confirm_deleting = QMessageBox.question(self, "Note deleting", f"Are yo sure you want to delete: {selected_note.text()} note?")
        if confirm_deleting == QMessageBox.StandardButton.Yes:
            self.notes.pop(selected_note.text())
            self.refresh_note_list()


    def closeEvent(self, event):
        confirm = QMessageBox.question(self, "Confirm exit",
                                       "Are you sure you want to exit? All unsaved data will be lost!")
        if confirm == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()
