"""
Application: Note Application
Author: Istvan Godeny
Date: 14/07/2025
License: MIT License
"""

from PySide6.QtWidgets import QFrame, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

from PySide6.QtCore import Signal


class NoteCard(QFrame):
    # Signal for delete request
    signal_delete_requested = Signal(int)
    # Signal for selection
    signal_selected = Signal(int, bool)

    def __init__(self, note_id: int, title: str, content: str, parent=None):
        super().__init__(parent)

        self.note_id = note_id

        self.selected = False
        self.hovered = False
        self.update_style()

        # Card's layout
        layout_for_card = QVBoxLayout()

        # Layout for title and delete button
        layout_header_with_title_and_delete_button = QHBoxLayout()
        # Note's title
        self.label_note_title = QLabel(title)
        self.label_note_title.setStyleSheet("font-family: Roboto Mono;"
                                            "font-weight: bold;"
                                            "font-size: 16px;")

        # Note's delete button
        self.button_delete_note = QPushButton("X")
        self.button_delete_note.setFixedSize(25, 25)
        self.button_delete_note.setStyleSheet("font_family: Roboto Mono;"
                                              "font-weight: bold;"
                                              "font-size: 10px;"
                                              "border: none;"
                                              "background-color: transparent;")
        self.button_delete_note.clicked.connect(self.request_delete)

        # Add the title and button to the header layout
        layout_header_with_title_and_delete_button.addWidget(self.label_note_title)
        layout_header_with_title_and_delete_button.addStretch()
        layout_header_with_title_and_delete_button.addWidget(self.button_delete_note)

        # Note's content
        self.label_note_content = QLabel(content)
        self.label_note_content.setStyleSheet("font-family: Roboto Mono;"
                                              "font-weight: normal;"
                                              "font-size: 12px;")
        self.label_note_content.setWordWrap(True)


        ## Add the elements to the crd's layout
        # Header layout with title and button
        layout_for_card.addLayout(layout_header_with_title_and_delete_button)
        # Content Widget
        layout_for_card.addWidget(self.label_note_content)

        # Add the card's layout to the QFrame
        self.setLayout(layout_for_card)

        # Set up the object name for card
        self.setObjectName("noteCard")


    # Send the delete request signal
    def request_delete(self):
        self.signal_delete_requested.emit(self.note_id)


    # Mouse press event override for selection
    def mousePressEvent(self, event):
        self.selected = not self.selected
        self.update_style()
        self.signal_selected.emit(self.note_id, self.selected)


    # Set up the basic card style and changed the style when hovered
    def update_style(self):
        if self.selected:
            bg = "#e6f2ff"
        elif self.hovered:
            bg = "#eef6ff"
        else:
            bg = "#fdfdfd"

        border = "2px solid #007acc" if self.selected else "1px solid #ccc"

        self.setStyleSheet(f"""
               #noteCard {{
                   background-color: {bg};
                   border: {border};
                   border-radius: 8px;
                   padding: 10px;
               }}
           """)


    # Activate the hovered effect
    def enterEvent(self, event):
        self.hovered = not self.hovered
        self.update_style()


    # Deactivate the hovered effect
    def leaveEvent(self, event):
        self.hovered = not self.hovered
        self.update_style()
