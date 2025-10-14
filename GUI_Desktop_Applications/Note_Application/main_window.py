"""
Application: Note Application
Author: Istvan Godeny
Date: 14/07/2025
License: MIT License
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                               QHBoxLayout, QPushButton, QScrollArea, QMessageBox)
from PySide6.QtGui import QFont, Qt
from PySide6.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PySide6.QtCore import Slot

from note_card import NoteCard
from add_new_note_card import AddNewNoteCard
from edit_note_card import EditNoteCard
from database import DB_PATH

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Set up the window parameters
        self.setWindowTitle("Note Application")
        self.resize(640, 480)

        self.selected_note_id = None

        self.note_cards = []

        self._setup_database_model()
        self._setup_ui_main_window()
        self.load_notes_from_database()


    def _setup_database_model(self):
        self.db = QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(DB_PATH)

        if not self.db.open():
            print("Could not open the database")
            return

        self.model = QSqlTableModel(self, self.db)
        self.model.setTable("notes")
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "title")
        self.model.setHeaderData(2, Qt.Horizontal, "content")


    def _setup_ui_main_window(self):
        self.layout_main_window = QVBoxLayout()
        self.layout_main_window.setSpacing(10)
        self.layout_main_window.setContentsMargins(10, 10, 10, 10)

        ## Label for the Title
        label_title = QLabel("My Notes")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(QFont("Roboto Mono", 17))

        ## Cardholder with rolling option
        self.card_container_widget = QWidget()
        self.card_layout = QVBoxLayout()
        self.card_layout.setSpacing(10)
        self.card_layout.setContentsMargins(5, 5, 5, 5)
        self.card_container_widget.setLayout(self.card_layout)

        # Scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.card_container_widget)

        ## Button layout for buttons
        layout_btn = QHBoxLayout()
        layout_btn.setContentsMargins(10,0,10,0)
        layout_btn.setSpacing(10)

        btn_open_add_new_note = QPushButton("New Note")
        btn_open_add_new_note.setFont(QFont("Roboto Mono", 12))
        btn_open_add_new_note.setStyleSheet("font-weight: bold")
        btn_open_add_new_note.setMinimumSize(200, 30)
        btn_open_add_new_note.setMaximumSize(200, 50)
        btn_open_add_new_note.clicked.connect(self.open_add_new_note)

        btn_open_edit_note_card = QPushButton("Edit Note")
        btn_open_edit_note_card.setFont(QFont("Roboto Mono", 12))
        btn_open_edit_note_card.setStyleSheet("font-weight: bold")
        btn_open_edit_note_card.setMinimumSize(200, 30)
        btn_open_edit_note_card.setMaximumSize(200, 50)
        btn_open_edit_note_card.clicked.connect(self.open_edit_note_card)

        btn_exit_app = QPushButton("Exit")
        btn_exit_app.setFont(QFont("Roboto Mono", 12))
        btn_exit_app.setStyleSheet("font-weight: bold")
        btn_exit_app.setMinimumSize(200, 30)
        btn_exit_app.setMaximumSize(200, 50)
        btn_exit_app.clicked.connect(self.close)

        layout_btn.addWidget(btn_open_add_new_note)
        layout_btn.addWidget(btn_open_edit_note_card)
        layout_btn.addWidget(btn_exit_app)

        self.layout_main_window.addWidget(label_title)
        self.layout_main_window.addWidget(self.scroll_area)
        self.layout_main_window.addLayout(layout_btn)

        self.setLayout(self.layout_main_window)


    def load_notes_from_database(self):
        # Create the cards from the database
        row_count = self.model.rowCount()
        for row in range(row_count):
            id_index = self.model.index(row, 0)
            title_index = self.model.index(row, 1)
            content_index = self.model.index(row, 2)

            note_id = self.model.data(id_index)
            title = self.model.data(title_index)
            content = self.model.data(content_index)

            note_card = NoteCard(note_id, title, content)
            note_card.signal_delete_requested.connect(self.delete_note)
            note_card.signal_selected.connect(self.set_selected_note)

            self.note_cards.append(note_card)

            self.card_layout.addWidget(note_card)


    def open_add_new_note(self):
        dialog = AddNewNoteCard()

        if dialog.exec():
            # Receive the inputs from the new note dialog
            title = dialog.line_edit_new_note_card_title.text()
            content = dialog.text_edit_new_note_card_content.toPlainText()

            # Save to database
            query = QSqlQuery(self.db)
            query.prepare("INSERT INTO notes (title, content) VALUES (:title, :content)")
            query.bindValue(":title", title)
            query.bindValue(":content", content)
            query.exec()

            # Ask for the last added item
            note_id = query.lastInsertId()

            # Update the model
            self.model.select()

            # Create the new card and added to the scroll_area
            note_card = NoteCard(note_id, title, content)
            note_card.signal_delete_requested.connect(self.delete_note)
            note_card.signal_selected.connect(self.set_selected_note)

            self.note_cards.append(note_card)

            self.card_layout.addWidget(note_card)


    def open_edit_note_card(self):
        if not hasattr(self, 'selected_note_id') or self.selected_note_id is None:
            return

        # Data from DB
        query = QSqlQuery(self.db)
        query.prepare("SELECT title, content FROM notes WHERE id = :id")
        query.bindValue(":id", self.selected_note_id)
        query.exec()

        if query.next():
            title = query.value(0)
            content = query.value(1)

            dialog = EditNoteCard()
            dialog.line_edit_edit_note_card_title.setText(title)
            dialog.text_edit_edit_note_card_content.setPlainText(content)

            # Receive the inputs from the edit note dialog
            if dialog.exec():
                new_title = dialog.line_edit_edit_note_card_title.text()
                new_content = dialog.text_edit_edit_note_card_content.toPlainText()

                update_query = QSqlQuery(self.db)
                update_query.prepare("UPDATE notes SET title = :title, content = :content WHERE id = :id")
                update_query.bindValue(":title", new_title)
                update_query.bindValue(":content", new_content)
                update_query.bindValue(":id", self.selected_note_id)
                update_query.exec()

                # Update the GUI
                for i in range(self.card_layout.count()):
                    widget = self.card_layout.itemAt(i).widget()
                    if isinstance(widget, NoteCard) and widget.note_id == self.selected_note_id:
                        widget.label_note_title.setText(new_title)
                        widget.label_note_content.setText(new_content)


    @Slot(int)
    def delete_note(self, note_id):
        # Testing part, check before deleting
        # for note_card in self.note_cards:
        #     print(note_card)
        # print()

        # Warning before delete
        warning = QMessageBox.question(self, "Confirm Deletion", "Are you sure you want to permanently delete this note? This action cannot be undone.")
        if warning == QMessageBox.StandardButton.Yes:
            # Delete from DB
            query = QSqlQuery(self.db)
            query.prepare("DELETE FROM notes WHERE id = :id")
            query.bindValue(":id", note_id)
            if not query.exec():
                print("Failed to delete", query.lastError().text())


            # Remove the card from the GUI
            for i in reversed(range(self.card_layout.count())):
                widget = self.card_layout.itemAt(i).widget()
                if isinstance(widget, NoteCard) and widget.note_id == note_id:
                    self.card_layout.removeWidget(widget)
                    widget.setParent(None)
                    widget.deleteLater()

            # Remove the card from tha array which helps for only 1 selection at the time
            self.note_cards = [card for card in self.note_cards if card.note_id != note_id]


            # # Testing part, check after deleting
            # for note_card in self.note_cards:
            #     print(note_card)


    @Slot(int, bool)
    def set_selected_note(self, note_id, selected):
        self.selected_note_id = note_id

        sender = self.sender()  # This is the selected card
        if selected:
            for card in self.note_cards:
                if card is not sender:
                    card.selected = False
                    card.update_style()
