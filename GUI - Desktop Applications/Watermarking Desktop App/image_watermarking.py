from tkinter import Menu, Canvas
from ttkbootstrap import Window, Style, StringVar, DoubleVar
from ttkbootstrap.widgets import (
    Label, Button, Entry, Combobox, Labelframe,
    Menubutton, Separator, Scale
)
from ttkbootstrap.dialogs.dialogs import Messagebox
from ttkbootstrap.dialogs.colorchooser import ColorChooserDialog
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import matplotlib.font_manager as fm


class App(Window):
    def __init__(self):
        super().__init__(themename="morph")

        self.font_paths = None
        self.img_path = None
        self.original_img = None
        self.thumb_img = None
        self.color_rgb = (0,0,0)
        self.color_hex = "#000000"
        self.actual_font_size = "150"
        self.actual_font_pos_x = 0.0
        self.actual_font_pos_y = 0.0


        self.width = int(self.winfo_screenwidth() * 0.9)  # Window width
        self.height = int(self.winfo_screenheight() * 0.9)  # Window height
        self.x_offset = int((self.winfo_screenwidth() - self.width) / 2)  # Window position in x
        self.y_offset = 0  # Window position in y
        self.geometry(f"{self.width}x{self.height}+{self.x_offset}+{self.y_offset}")  # Setup the Window size and pos
        self.minsize(width=self.width, height=self.height)  # Minimum size of the Window
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.app_exit)

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(3, weight=1)

        # ======================================== Elements Setup ===================================================
        self.menu_buttons_frame = Labelframe(master=self, text="Menu", relief="raised", border=10)

        self.file_menubutton = Menubutton(master=self.menu_buttons_frame, text="File")
        self.file_menu = Menu(master=self.file_menubutton)
        self.file_menu.add_command(label="Open File        [CTRL + O]", font=("Arial", 12), command=self.open_file)
        self.file_menu.add_command(label="Save File        [CTRL + S]", font=("Arial", 12), command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit                  [SHIFT + F4]", font=("Arial", 12),
                                   command=self.app_exit)
        self.file_menubutton["menu"] = self.file_menu

        self.edit_menubutton = Menubutton(master=self.menu_buttons_frame, text="Edit")

        self.view_menubutton = Menubutton(master=self.menu_buttons_frame, text="View")
        self.view_menu = Menu(master=self.view_menubutton)
        self.view_menu.add_command(label="Full Screen          [F12]", font=("Arial", 12), command=self.full_screen)
        self.view_menu.add_command(label="Exit Full Screen  [ESC]", font=("Arial", 12), command=self.exit_full_screen)
        self.view_menubutton["menu"] = self.view_menu

        self.help_menubutton = Menubutton(master=self.menu_buttons_frame, text="Help")

        self.title_label = Label(master=self, text="Watermark Creator", font=("Arial", 45, "bold"))

        self.theme_label = Label(master=self, text="Select a theme: ", font=("Arial", 16, "bold"))

        self.theme = Style()
        self.default_theme = StringVar()
        self.default_theme.set("morph")
        self.theme_combobox = Combobox(master=self, font=("Arial", 14),
                                       values=["cosmo", "flatly", "litera", "lumen", "yeti", "morph",
                                               "solar", "superhero", "darkly", "cyborg"],
                                       textvariable=self.default_theme)

        self.separator = Separator(master=self)

        self.image_frame = Labelframe(master=self, text="Image", relief="raised", border=10)
        self.image_canvas = Canvas(master=self.image_frame)

        self.watermark_creator_frame = Labelframe(master=self, text="Watermark Creator", relief="raised", border=10)
        self.watermark_text_entry_frame = Labelframe(master=self.watermark_creator_frame, text="Watermark text")

        self.vcmd = self.register(self.limit_text_length)
        self.watermark_text_entry = Entry(master=self.watermark_text_entry_frame, font=("Arial", 14),
                                          validate="key", validatecommand=(self.vcmd, "%P"))

        self.watermark_text_position_frame = Labelframe(master=self.watermark_creator_frame,
                                                        text="Watermark Text Position", relief="raised", border=10)

        self.watermark_text_position_frame_x_axel = Labelframe(master=self.watermark_text_position_frame,
                                                               text="Text Position X axel", relief="raised", border=10)
        self.watermark_text_position_x_axel_default = DoubleVar()
        self.watermark_text_position_x_axel_default.set(self.actual_font_pos_x)
        self.watermark_text_position_x_axel = Scale(master=self.watermark_text_position_frame_x_axel,
                                                    from_=1, to=2000, variable=self.watermark_text_position_x_axel_default)

        self.watermark_text_position_frame_y_axel = Labelframe(master=self.watermark_text_position_frame,
                                                               text="Text Position Y axel", relief="raised", border=10)
        self.watermark_text_position_y_axel_default = DoubleVar()
        self.watermark_text_position_y_axel_default.set(self.actual_font_pos_y)
        self.watermark_text_position_y_axel = Scale(master=self.watermark_text_position_frame_y_axel,
                                                    from_=1, to=2000, variable=self.watermark_text_position_y_axel_default)

        # ====================== Text Setup ========================
        self.watermark_text_font_frame = Labelframe(master=self.watermark_creator_frame,
                                                    text="Watermark Text Font Setup", relief="raised", border=10)

        # ---------------------- Font Family -----------------------
        self.watermark_text_font_family_label = Label(master=self.watermark_text_font_frame, text="Font Family:",
                                                      font=("Ariel", 14))

        self.watermark_text_font_family_default = StringVar()
        self.watermark_text_font_family_chosen_combobox = Combobox(master=self.watermark_text_font_frame,
                                                                   font=("Ariel", 12),
                                                                   textvariable=self.watermark_text_font_family_default)
        self.font_setup()

        # ---------------------- Font Size -------------------------
        self.watermark_text_font_size_label = Label(master=self.watermark_text_font_frame, text="Font Size:",
                                                    font=("Ariel", 14))

        self.watermark_text_font_size_default = StringVar()
        self.watermark_text_font_size_default.set(self.actual_font_size)
        self.watermark_text_font_size_chosen_combobox = Combobox(master=self.watermark_text_font_frame,
                                                                 font=("Ariel", 12),
                                                                 textvariable=self.watermark_text_font_size_default)

        # --------------------- Text Colour -------------------------
        self.watermark_text_font_colour_frame = Labelframe(master=self.watermark_creator_frame,
                                                           text="Watermark Text Colour Setup", relief="raised", border=10)
        self.watermark_text_font_colour_label = Label(master=self.watermark_text_font_colour_frame, text="Font Colour:",
                                                      font=("Ariel", 14))

        self.watermark_text_font_colour_show_label = Label(master=self.watermark_text_font_colour_frame,
                                                           font=("Ariel", 14), relief="raised",
                                                           text="          ",
                                                           background=self.color_hex)
        self.watermark_text_font_colour_btn = Button(master=self.watermark_text_font_colour_frame,
                                                     text="Colour",
                                                     command=self.colour_setup)


        # =========================================== Grid Setup ======================================================
        # ======================================  Row = 0, Column = 0 =================================================
        self.menu_buttons_frame.grid(row=0, column=0, padx=10, sticky="w")

        self.file_menubutton.grid(row=0, column=0, padx=10, pady=10)
        self.edit_menubutton.grid(row=0, column=1, padx=5, pady=10)
        self.view_menubutton.grid(row=0, column=2, padx=5, pady=10)
        self.help_menubutton.grid(row=0, column=3, padx=10, pady=10)
        # ======================================  Row = 1, Column = 0 =================================================
        self.title_label.grid(row=1, column=0, padx=10, pady=10, columnspan=2, sticky="w")

        self.theme_label.grid(row=1, column=2, padx=5, sticky="e")

        self.theme_combobox.grid(row=1, column=3, padx=10, sticky="w")
        # ======================================  Row = 2, Column = 0 =================================================
        self.separator.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="ew")
        # ======================================  Row = 3, Column = 0 =================================================
        self.image_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="nesw")
        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_rowconfigure(0, weight=1)

        self.image_canvas.grid(row=0, column=0, padx=2, pady=2, sticky="nesw")
        # ======================================  Row = 3, Column = 3 =================================================
        self.watermark_creator_frame.grid(row=3, column=3, padx=10, pady=10, sticky="new")
        self.watermark_creator_frame.grid_columnconfigure(0, weight=1)
        self.watermark_creator_frame.grid_rowconfigure((0, 1), weight=1)

        self.watermark_text_entry_frame.grid(row=0, column=0, padx=2, pady=10, sticky="nwe")  ####################
        self.watermark_text_entry_frame.grid_columnconfigure(0, weight=1)
        self.watermark_text_entry_frame.grid_rowconfigure(0, weight=1)

        self.watermark_text_entry.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        self.watermark_text_position_frame.grid(row=1, column=0, padx=2, pady=2, sticky="nwe")  ##################
        self.watermark_text_position_frame.grid_columnconfigure(0, weight=1)
        self.watermark_text_position_frame.grid_rowconfigure(0, weight=1)

        self.watermark_text_position_frame_x_axel.grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        self.watermark_text_position_frame_x_axel.grid_columnconfigure(0, weight=1)
        self.watermark_text_position_frame_x_axel.grid_rowconfigure(0, weight=1)

        self.watermark_text_position_x_axel.grid(row=0, column=0, padx=2, pady=2, sticky="ew")
        self.watermark_text_position_frame_y_axel.grid_columnconfigure(0, weight=1)
        self.watermark_text_position_frame_y_axel.grid_rowconfigure(0, weight=1)

        self.watermark_text_position_frame_y_axel.grid(row=1, column=0, padx=2, pady=2, sticky="ew")
        self.watermark_text_position_frame_y_axel.grid_columnconfigure(0, weight=1)
        self.watermark_text_position_frame_y_axel.grid_rowconfigure(0, weight=1)

        self.watermark_text_position_y_axel.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        self.watermark_text_font_frame.grid(row=2, column=0, padx=2, pady=10, sticky="nwe")  ################
        self.watermark_text_font_frame.grid_columnconfigure((0, 1), weight=1)
        self.watermark_text_font_frame.grid_rowconfigure(0, weight=1)

        self.watermark_text_font_family_label.grid(row=0, column=0, padx=2, pady=2, sticky="ew")

        self.watermark_text_font_family_chosen_combobox.grid(row=0, column=1, padx=2, pady=2, sticky="ew")

        self.watermark_text_font_size_label.grid(row=1, column=0, padx=2, pady=2, sticky="ew")

        self.watermark_text_font_size_chosen_combobox.grid(row=1, column=1, padx=2, pady=2, sticky="we")

        self.watermark_text_font_colour_frame.grid(row=3, column=0, padx=2, pady=10, sticky="new")  ###################
        self.watermark_text_font_colour_frame.grid_columnconfigure((0,1), weight=1)
        self.watermark_text_font_colour_frame.grid_rowconfigure(0, weight=1)

        self.watermark_text_font_colour_label.grid(row=0, column=0, padx=2, pady=2, sticky="w")

        self.watermark_text_font_colour_show_label.grid(row=0, column=1, padx=5, pady=2, sticky="ew")
        self.watermark_text_font_colour_btn.grid(row=0, column=0, columnspan=2, padx=2, pady=2)

        # ======================================= Binds Setup ========================================================
        self.theme_combobox.bind("<<ComboboxSelected>>", self.theme_changer)  # Change the theme
        self.bind("<F12>", self.full_screen)  # Full Screen Mode
        self.bind("<Escape>", self.exit_full_screen)  # Exit from Full Screen Mode
        self.bind("<Shift-F4>", self.app_exit)  # Exit from the App
        self.bind("<Control-o>", self.open_file)  # Open File
        self.image_canvas.bind("<Configure>", self.display_image)  # Resize thumb image to frame
        self.watermark_text_entry.bind("<KeyRelease>", self.watermark)
        self.bind("<Configure>", self.watermark)
        self.watermark_text_position_x_axel.bind("<Motion>", self.watermark)  # Change the watermark text x pos
        self.watermark_text_position_y_axel.bind("<Motion>", self.watermark)  # Change the watermark text y pos
        self.watermark_text_font_family_chosen_combobox.bind("<<ComboboxSelected>>", self.watermark)  # Apply Font
        self.watermark_text_font_size_chosen_combobox.bind("<<ComboboxSelected>>", self.watermark)  # Apply Font size

    def theme_changer(self, event=None):
        self.theme.theme_use(themename=self.theme_combobox.get())

    def app_exit(self, event=None):
        exit_app = Messagebox.yesno(title="Close Application",
                                    message="Are you sure, you want to exit? If so, you will loose all unsaved progress!")
        if exit_app == "Yes":
            app.quit()

    def full_screen(self, event=None):
        self.attributes('-fullscreen', True)

    def exit_full_screen(self, event=None):
        self.attributes('-fullscreen', False)

    def limit_text_length(self, text_length):
        return len(text_length) <= 30

    def open_file(self, event=None):
        path = filedialog.askopenfile(filetypes=[
            ("JPEG", "*.jpg"), ("JPEG", "*.jpeg"), ("GIF", "*.gif"), ("PNG", "*.png")
        ])
        if path:
            self.img_path = path.name
            self.original_img = Image.open(self.img_path)
            self.display_image()

    def save_file(self):
        if not self.original_img:
            return

        img_to_save = self.original_img.copy()

        scale_x = self.original_img.width / self.thumb_img.width
        scale_y = self.original_img.height / self.thumb_img.height

        true_x = float(self.watermark_text_position_x_axel.get()) * scale_x
        true_y = float(self.watermark_text_position_y_axel.get()) * scale_y

        font_size = int(self.watermark_text_font_size_chosen_combobox.get())
        true_font_size = int(font_size * ((scale_x + scale_y) / 2))

        draw = ImageDraw.Draw(img_to_save)
        # Changed
        font_key = self.watermark_text_font_family_chosen_combobox.get()
        font_path = self.font_paths.get(font_key)

        font = ImageFont.truetype(font=font_path, size=true_font_size)

        draw.text((true_x, true_y),
                  text=self.watermark_text_entry.get(),
                  fill=self.color_rgb,
                  font=font,
                  anchor='ms')

        file_types = [("All files", "*.*"), ("Images file", "*.png")]
        file_name = filedialog.asksaveasfilename(initialfile="watermarked", filetypes=file_types,
                                                 defaultextension="png")
        if file_name:
            img_to_save.save(f"{file_name}.png")
            self.watermark_text_entry.delete(0, "end")
            self.img_path = None
            self.original_img = None
            self.thumb_img = None
            self.image_canvas.delete("all")

    def display_image(self, event=None):
        if not self.img_path:
            return

        self.img_canvas_width = self.image_canvas.winfo_width()
        self.img_canvas_height = self.image_canvas.winfo_height()

        self.thumb_img = self.original_img.copy()
        self.thumb_img.thumbnail((self.img_canvas_width, self.img_canvas_height))
        self.displayed_img = ImageTk.PhotoImage(self.thumb_img)

        self.image_canvas.delete("all")
        self.image_canvas.create_image(self.img_canvas_width / 2, self.img_canvas_height / 2,
                                       image=self.displayed_img, anchor="center")

        if self.actual_font_pos_x == 0.0 and self.actual_font_pos_y == 0.0:
            self.watermark_text_position_x_axel.configure(variable=DoubleVar(value=self.thumb_img.width / 2))
            self.watermark_text_position_y_axel.configure(variable=DoubleVar(value=self.thumb_img.height / 2))

        self.setter()

    def watermark(self, event=None):
        if self.img_path and self.thumb_img:
            image_for_watermark = self.thumb_img.copy()
            draw = ImageDraw.Draw(image_for_watermark)

            font_family = self.watermark_text_font_family_chosen_combobox.get()
            font_size = int(self.watermark_text_font_size_chosen_combobox.get())
            font_path = self.font_paths.get(font_family)
            font = ImageFont.truetype(font=font_path, size=font_size)

            draw.text((float(self.watermark_text_position_x_axel.get()), float(self.watermark_text_position_y_axel.get())),
                text=self.watermark_text_entry.get(),
                fill=self.color_rgb,
                font=font,
                anchor='ms')

            self.img_canvas_width = self.image_canvas.winfo_width()
            self.img_canvas_height = self.image_canvas.winfo_height()

            self.watermark_img = ImageTk.PhotoImage(image_for_watermark)

            self.image_canvas.delete("all")
            self.image_canvas.create_image(self.img_canvas_width // 2, self.img_canvas_height // 2,
                                           image=self.watermark_img, anchor="center")
            self.actual_font_size = self.watermark_text_font_size_chosen_combobox.get()
            self.actual_font_pos_x = float(self.watermark_text_position_x_axel.get())
            self.actual_font_pos_y = float(self.watermark_text_position_y_axel.get())

            return image_for_watermark

    def setter(self):
        image_width = ImageTk.PhotoImage(Image.open(self.img_path)).width()
        image_height = ImageTk.PhotoImage(Image.open(self.img_path)).height()
        if self.img_path:
            self.watermark_text_position_x_axel.configure(to=image_width)
            self.watermark_text_position_y_axel.configure(to=image_height)

        x, y = int(image_width / 2), int(image_height / 2)
        if x > y:
            self.watermark_text_font_size_chosen_combobox.config(values=[str(size) for size in range(1, int(y * 1.5))])
        elif y > x:
            self.watermark_text_font_size_chosen_combobox.config(values=[str(size) for size in range(1, int(x * 1.5))])
        else:
            self.watermark_text_font_size_chosen_combobox.config(values=[str(size) for size in range(1, int(x * 1.5))])

    def font_setup(self):
        import os
        font_dir = os.path.join(os.path.dirname(__file__), "fonts")
        font_files = [f for f in os.listdir(font_dir) if f.lower().endswith(".ttf")]
        font_display_names = []
        self.font_paths = {}

        for f in font_files:
            path = os.path.join(font_dir, f)
            try:
                font_prop = fm.FontProperties(fname=path)
                name = font_prop.get_name()
                display_name = f"{name} ({f})"
                font_display_names.append(display_name)
                self.font_paths[display_name] = path
            except Exception:
                continue

        font_display_names.sort()
        self.watermark_text_font_family_chosen_combobox.config(values=font_display_names)
        if font_display_names:
            self.watermark_text_font_family_default.set(font_display_names[0])

    def colour_setup(self):
        cd = ColorChooserDialog()
        cd.show()
        color = cd.result
        self.watermark_text_font_colour_show_label.config(background=color[2])
        self.color_rgb = color[0]
        self.watermark()


if __name__ == "__main__":
    app = App()

    app.mainloop()
