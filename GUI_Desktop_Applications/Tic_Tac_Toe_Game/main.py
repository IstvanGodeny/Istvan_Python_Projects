"""
Application: Tic Tac Toe Game
Author: Istvan Godeny
Date: 11/10/2024
License: MIT License
"""

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.behaviors import HoverBehavior
from kivy.core.window import Window

# ---------------------------------------------------- Button hovering --------------------------------------
class HoverRaisedButton(MDRaisedButton, HoverBehavior):
        def __init__(self, *args, **kwargs):
            super().__init__(args, kwargs)

        def on_enter(self):
            # Handle hover behavior
            self.md_bg_color = (68 / 255, 41 / 255, 99 / 255, 1)
            self.elevation = 3

        def on_leave(self):
            # Restore original appearance when not hovered
            self.md_bg_color = (48 / 255, 21 / 255, 79 / 255, 1)
            self.elevation = 1

# ---------------------------------------------------- Responsive Screen ------------------------------------
class ResponsiveScreen(MDScreen):
    def on_window_resize(self, *args):
        width = Window.width

        if width < 1200:
            self.ids.player1.font_style = "H5"
            self.ids.player1_score.font_style = "H5"
            self.ids.player2_score.font_style = "H5"
            self.ids.player2.font_style = "H5"
            self.ids.buttons_layout.size_hint = (1, 0.75)
            self.ids.reset_btn.font_style = "H6"
            self.ids.exit_btn.font_style = "H6"
        elif width < 1980:
            self.ids.player1.font_style = "H4"
            self.ids.player1_score.font_style = "H4"
            self.ids.player2_score.font_style = "H4"
            self.ids.player2.font_style = "H4"
            self.ids.buttons_layout.size_hint = (0.5, 1)
            self.ids.reset_btn.font_style = "H5"
            self.ids.exit_btn.font_style = "H5"
        else:
            self.ids.player1.font_style = "H1"
            self.ids.player1_score.font_style = "H1"
            self.ids.player2_score.font_style = "H1"
            self.ids.player2.font_style = "H1"
            self.ids.buttons_layout.size_hint = (0.75, 1)
            self.ids.reset_btn.font_style = "H2"
            self.ids.exit_btn.font_style = "H2"


class TicTacToeApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.dialog_1 = None
        self.dialog_2 = None
        self.player_name_1 = None
        self.player_name_2 = None
        self.r_dialog = None

        self.q_dialog = None
        self.w_dialog = None
        self.d_dialog = None
        self.actual_player = 1
        self.player1_score = 0
        self.player2_score = 0
        self.player = ""



    # ================================================ Dialogs ==============================================
    # ------------------------------------------------ Player 1 setup ---------------------------------------
    def dialog_player_name_1(self):
        if not self.dialog_1:
            # - TextField for input
            self.player_name_1 = MDTextField(
                hint_text="Enter a name of the first player",
                size_hint_x=None,
                width=300
            )
            # - Crete the dialog
            self.dialog_1 = MDDialog(
                type="custom",
                title="Name of the first player",
                text="Please, enter the name of the first player: ",
                content_cls=self.player_name_1,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_press=self.get_player_name_1
                    ),
                    MDRaisedButton(
                        text="Cancel",
                        on_release=self.dialog_close_1
                    ),
                ],
                auto_dismiss=False
            )
        self.dialog_1.pos_hint = {"center_x": 0.5, "center_y": 0.75}
        self.dialog_1.size_hint = (0.9, None)
        self.dialog_1.open()

    def dialog_close_1(self, *args):
        self.dialog_1.dismiss()

    def get_player_name_1(self, *args):
        player_name = self.player_name_1.text
        self.root.ids.player1.text = player_name
        self.dialog_close_1()
        self.dialog_player_name_2()

    # ------------------------------------------------ Player 2 setup ---------------------------------------
    def dialog_player_name_2(self):
        if not self.dialog_2:
            # - TextField for input
            self.player_name_2 = MDTextField(
                hint_text="Enter a name of the second player",
                size_hint_x=None,
                width=300
            )
            # - Crete the dialog
            self.dialog_2 = MDDialog(
                type="custom",
                title="Name of the second player",
                text="Please, enter the name of the second player: ",
                content_cls=self.player_name_2,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_press=self.get_player_name_2
                    ),
                    MDRaisedButton(
                        text="Cancel",
                        on_release=self.dialog_close_2
                    ),
                ],
                auto_dismiss=False
            )
        self.dialog_2.pos_hint = {"center_x": 0.5, "center_y": 0.75}
        self.dialog_2.size_hint = (0.9, None)
        self.dialog_2.open()

    def dialog_close_2(self, *args):
        self.dialog_2.dismiss()

    def get_player_name_2(self, *args):
        player_name = self.player_name_2.text
        self.root.ids.player2.text = player_name
        self.dialog_close_2()

    # ------------------------------------------------ Reset the game ---------------------------------------
    def reset_dialog(self):
        if not self.r_dialog:
            self.r_dialog = MDDialog(
                title="Reset Game",
                text="Are you sure that you want to reset the game? All of your progress will be deleted! You need to setup the players again.",
                type="alert",
                buttons=[
                    MDRaisedButton(
                        text="Reset",
                        on_press=self.reset
                    ),
                    MDRaisedButton(
                        text="Cancel",
                        on_press=self.cancel_reset
                    ),
                ],
                auto_dismiss=False
            )
        self.r_dialog.size_hint = (0.8, None)
        self.r_dialog.open()

    def reset(self, *args):
        # -------------------------------- Reset Player 1 -------------------------
        self.root.ids.player1.text = "Player_1"
        self.root.ids.player1_score.text = "0"
        self.root.player1_score = 0
        # -------------------------------- Reset Player 2 -------------------------
        self.root.ids.player2.text = "Player_2"
        self.root.ids.player2_score.text = "0"
        self.root.player2_score = 0
        # ------------------------------- Reset buttons ---------------------------
        self.root.ids.a1.text = ""
        self.root.ids.a1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.a2.text = ""
        self.root.ids.a2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.a3.text = ""
        self.root.ids.a3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b1.text = ""
        self.root.ids.b1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b2.text = ""
        self.root.ids.b2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b3.text = ""
        self.root.ids.b3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c1.text = ""
        self.root.ids.c1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c2.text = ""
        self.root.ids.c2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c3.text = ""
        self.root.ids.c3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.r_dialog.dismiss()

        self.dialog_player_name_1()

    def cancel_reset(self, *args):
        self.r_dialog.dismiss()

    # ------------------------------------------------ Exit -------------------------------------------------
    def quit_dialog(self):
        if not self.q_dialog:
            self.q_dialog = MDDialog(
                title="Warning for exit",
                type="alert",
                text="Are you sure that you want to exit? All of your progress will be deleted!",
                buttons=[
                    MDRaisedButton(
                        text="Exit",
                        on_press=self.exit
                    ),
                    MDRaisedButton(
                        text="Cancel",
                        on_press=self.cancel_quit
                    ),
                ],
                auto_dismiss=False
            )
        self.q_dialog.size_hint = (0.8, None)
        self.q_dialog.open()

    def exit(self, *args):
        TicTacToeApp().stop()

    def cancel_quit(self, *args):
        self.q_dialog.dismiss()

    # ------------------------------------------------ Winner -----------------------------------------------
    def winner_dialog(self):
        if not self.w_dialog:
            self.w_dialog = MDDialog(
                title="Winner",
                text=f"{self.player} is the winner",
                type="alert",
                buttons=[
                    MDRaisedButton(
                        text="Ok",
                        on_press=self.winner_ok
                    ),
                ],
                auto_dismiss=False
            )
        else:
            self.w_dialog = MDDialog(
                title="Winner",
                text=f"{self.player} is the winner",
                type="alert",
                buttons=[
                    MDRaisedButton(
                        text="Ok",
                        on_press=self.winner_ok
                    ),
                ],
                auto_dismiss=False
            )
        self.w_dialog.size_hint = (0.8, None)
        self.w_dialog.open()

    def winner_ok(self, *args):
        if self.player == self.root.ids.player1.text:
            self.player1_score += 1
            self.root.ids.player1_score.text = str(self.player1_score)
            self.actual_player = 2
        else:
            self.player2_score += 1
            self.root.ids.player2_score.text = str(self.player2_score)
            self.actual_player = 1

        self.root.ids.a1.text = ""
        self.root.ids.a1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.a2.text = ""
        self.root.ids.a2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.a3.text = ""
        self.root.ids.a3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b1.text = ""
        self.root.ids.b1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b2.text = ""
        self.root.ids.b2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b3.text = ""
        self.root.ids.b3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c1.text = ""
        self.root.ids.c1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c2.text = ""
        self.root.ids.c2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c3.text = ""
        self.root.ids.c3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.player = ""

        self.w_dialog.dismiss()

    # ------------------------------------------------ Draw -------------------------------------------------
    def draw_dialog(self):
        if not self.d_dialog:
            self.d_dialog = MDDialog(
                title="Draw",
                text=" Draw! ",
                type="alert",
                buttons=[
                    MDRaisedButton(
                        text="Ok",
                        on_press=self.draw_ok
                    ),
                ],
                auto_dismiss=False
            )
        self.d_dialog.size_hint = (0.8, None)
        self.d_dialog.open()

    def draw_ok(self, *args):
        self.root.ids.a1.text = ""
        self.root.ids.a1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.a2.text = ""
        self.root.ids.a2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.a3.text = ""
        self.root.ids.a3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b1.text = ""
        self.root.ids.b1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b2.text = ""
        self.root.ids.b2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.b3.text = ""
        self.root.ids.b3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c1.text = ""
        self.root.ids.c1.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c2.text = ""
        self.root.ids.c2.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.root.ids.c3.text = ""
        self.root.ids.c3.line_color = 48 / 255, 21 / 255, 79 / 255, 1

        self.player = ""

        self.d_dialog.dismiss()


    # ================================================ Game Functions =======================================
    # ------------------------------------------------ Press the buttons ------------------------------------
    def press(self, obj):
        # Check for active player
        if self.actual_player == 1:
            if obj.text == "":
                obj.text = "X"
                obj.text_color = 91 / 255, 221 / 255, 212 / 255, 1
                obj.line_color = 91 / 255, 221 / 255, 212 / 255, 1
                self.actual_player += 1
                self.root.ids.player1.text_color = 53 / 255, 45 / 255, 88 / 255, 1
                self.root.ids.player2.text_color = 210 / 255, 83 / 255, 194 / 255, 1
                # Search for winner
                if self.search_winner() == 0:
                    # Check for full table
                    self.is_the_table_full()
        else:
            if obj.text == "":
                obj.text = "O"
                obj.text_color = 210 / 255, 83 / 255, 194 / 255, 1
                obj.line_color = 210 / 255, 83 / 255, 194 / 255
                self.actual_player -= 1
                self.root.ids.player1.text_color = 91 / 255, 221 / 255, 212 / 255, 1
                self.root.ids.player2.text_color = 53 / 255, 45 / 255, 88 / 255, 1
                # Search for winner
                if self.search_winner() == 0:
                    # Check for full table
                    self.is_the_table_full()

    # ------------------------------------------------ Search for winner ------------------------------------
    def search_winner(self):
        if (self.root.ids.a1.text == "X" and self.root.ids.a2.text == "X" and self.root.ids.a3.text == "X") or (
                self.root.ids.b1.text == "X" and self.root.ids.b2.text == "X" and self.root.ids.b3.text == "X") or (
                self.root.ids.c1.text == "X" and self.root.ids.c2.text == "X" and self.root.ids.c3.text == "X") or (
                self.root.ids.a1.text == "X" and self.root.ids.b1.text == "X" and self.root.ids.c1.text == "X") or (
                self.root.ids.a2.text == "X" and self.root.ids.b2.text == "X" and self.root.ids.c2.text == "X") or (
                self.root.ids.a3.text == "X" and self.root.ids.b3.text == "X" and self.root.ids.c3.text == "X") or (
                self.root.ids.a3.text == "X" and self.root.ids.b2.text == "X" and self.root.ids.c1.text == "X") or (
                self.root.ids.a1.text == "X" and self.root.ids.b2.text == "X" and self.root.ids.c3.text == "X"):
            self.player = self.root.ids.player1.text
            self.winner_dialog()
        elif (self.root.ids.a1.text == "O" and self.root.ids.a2.text == "O" and self.root.ids.a3.text == "O") or (
                self.root.ids.b1.text == "O" and self.root.ids.b2.text == "O" and self.root.ids.b3.text == "O") or (
                self.root.ids.c1.text == "O" and self.root.ids.c2.text == "O" and self.root.ids.c3.text == "O") or (
                self.root.ids.a1.text == "O" and self.root.ids.b1.text == "O" and self.root.ids.c1.text == "O") or (
                self.root.ids.a2.text == "O" and self.root.ids.b2.text == "O" and self.root.ids.c2.text == "O") or (
                self.root.ids.a3.text == "O" and self.root.ids.b3.text == "O" and self.root.ids.c3.text == "O") or (
                self.root.ids.a3.text == "O" and self.root.ids.b2.text == "O" and self.root.ids.c1.text == "O") or (
                self.root.ids.a1.text == "O" and self.root.ids.b2.text == "O" and self.root.ids.c3.text == "O"):
            self.player = self.root.ids.player2.text
            self.winner_dialog()
        else:
            return 0

    # ------------------------------------------------ Checking for draw ------------------------------------
    def is_the_table_full(self):
        if self.root.ids.a1.text != "" and self.root.ids.a2.text != "" and self.root.ids.a3.text != "" and self.root.ids.b1.text != "" and self.root.ids.b2.text != "" and self.root.ids.b3.text != "" and self.root.ids.c1.text != "" and self.root.ids.c2.text != "" and self.root.ids.c3.text != "":
            self.draw_dialog()


    def build(self):
        Window.bind(on_resize=self.update_layout)
        return ResponsiveScreen()

    def update_layout(self, *args):
        self.root.on_window_resize()

    def on_start(self):
        self.update_layout()
        self.dialog_player_name_1()


if __name__ == "__main__":
    TicTacToeApp().run()
