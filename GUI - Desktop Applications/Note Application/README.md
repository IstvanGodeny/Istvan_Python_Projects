# 📝 Note App — Built with PySide6

This is a minimal, clean, and functional desktop Note Application built using Python and PySide6 (Qt for Python).  
It allows users to create, edit, and delete notes stored locally in an SQLite database.

---
## ✨ Features

- Add new notes with a title and content
- Edit existing notes in a separate window
- Delete notes with confirmation dialog
- Scrollable note list with clickable note cards
- Visually highlighted selection
- Data persistence via SQLite
- Warning messages for accidental data loss
- Responsive and consistent UI (Roboto Mono font style)

---
## 🛠️ Technologies Used

- **Python 3**
- **PySide6** – GUI framework (Qt for Python)
- **SQLite** – Lightweight local database

---
## 📂 Project Structure

├── main.py                    # Application entry point

├── main_window.py             # Main window with note list

├── database.py                # Database setup and connection

├── note_card.py               # Custom note card widget

├── add_new_note_card.py       # Dialog for adding notes

├── edit_note_card.py          # Dialog for editing notes

└── notes.sqlite               # SQLite database (auto-generated)

---
## 🖥️ Cross-Platform Support

This app runs on:

- Windows
- macOS
- Linux

> ✅ No installation required — only Python 3.8+ and a few standard packages.

---
## 🎓 Author Note

This is a demo project, created as part of my learning journey as a junior Python developer.
I focused on building a functional, maintainable, and visually clean app, without unnecessary complexity.

---
## 📝 Licence

MIT Licence – feel free to use, modify, and learn from it!

---
## 🚀 How to Run

1. Clone this repository
```bash
git clone https://github.com/yourusername/note-app.git
cd note-app
```

2. (Optional) Create a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies
```bash
pip install PySide6
```
4 Run the application
```bash
python main.py
```
