# 🖼️ Image Watermarking Desktop App

A simple, cross-platform desktop application to add customizable text-based watermarks to images.  
Built with `tkinter`, styled using `ttkbootstrap`, and powered by `Pillow` for image processing.

---

## ✨ Features (MVP)

- ✅ Load JPEG, PNG, or GIF images
- 🎨 Add text watermarks with:
  - Custom font (from bundled `.ttf` files)
  - Size and colour options
  - Adjustable X/Y position
- 🔎 Live preview with real-time updates
- 💾 Save the final image with the watermark applied
- 💡 Clean GUI, resizable image frame, dark/light theme support

---

## 🖥️ Cross-Platform Support

This app runs on:

- Windows
- macOS
- Linux

> ✅ No installation required — only Python 3.8+ and a few standard packages.

---
## 📂 Fonts

All fonts are loaded from the fonts/ folder.
Only .ttf files are supported. You can freely add or remove font files.

---
## 📦 Dependencies
	•	tkinter (included with Python)
	•	ttkbootstrap
	•	Pillow
	•	matplotlib (used for reading font metadata)
 
---
## 🎓 Author Note

This is a demo project, created as part of my learning journey as a junior Python developer.
I focused on building a functional, maintainable, and visually clean app, without unnecessary complexity.

---
## 📝 Licence

MIT License – feel free to use, modify, and learn from it!

---
## 🚀 How to Run

1. Clone this repository
2. Ensure you have Python 3.8 or higher installed
3. Install dependencies:

```bash
pip install -r requirements.txt
```

```
python image_watermarking.py
```
