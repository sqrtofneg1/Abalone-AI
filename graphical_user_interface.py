import tkinter as tk
from settings import *


class GUI:
    """
    - 0 is not a space
    - 1 is black (player 1)
    - 2 is white (player 2)
    - 3 is empty
    """
    DEFAULT_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0],
                     [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 0],
                     [0, 0, 0, 3, 3, 2, 2, 2, 3, 3, 0],
                     [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                     [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                     [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                     [0, 3, 3, 1, 1, 1, 3, 3, 0, 0, 0],
                     [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
                     [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    BELGIAN_DAISY_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 2, 2, 3, 1, 1, 0],
                           [0, 0, 0, 0, 2, 2, 2, 1, 1, 1, 0],
                           [0, 0, 0, 3, 2, 2, 3, 1, 1, 3, 0],
                           [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                           [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                           [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                           [0, 3, 1, 1, 3, 2, 2, 3, 0, 0, 0],
                           [0, 1, 1, 1, 2, 2, 2, 0, 0, 0, 0],
                           [0, 1, 1, 3, 2, 2, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    GERMAN_DAISY_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 1, 1, 3, 2, 2, 0],
                          [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 0],
                          [0, 0, 0, 3, 1, 1, 3, 2, 2, 3, 0],
                          [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                          [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                          [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                          [0, 3, 2, 2, 3, 1, 1, 3, 0, 0, 0],
                          [0, 2, 2, 2, 1, 1, 1, 0, 0, 0, 0],
                          [0, 2, 2, 3, 1, 1, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    STARTING_LAYOUT = {1: DEFAULT_START, 2: BELGIAN_DAISY_START, 3: GERMAN_DAISY_START}

    PLAYER_COLOR_DICT = {1: "black", 2: "white", 3: "grey"}

    def __init__(self, settings=Settings.default_settings()):
        self.window = tk.Tk()
        self.window.title("Abalone AI")

        self.settings = settings

        # Center frame: Game Board, Moves History
        self.center_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="#7F694C")
        self.center_frame.grid(row=1, sticky="nsew")

        self.setup_bottom_frame()

        self.setup_directional_arrows()

        self.reset_game()

    def setup_top_frame(self):
        top_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="tan")
        top_frame.grid(row=0, sticky="ew")
        game_score = tk.Label(top_frame, text="Player 1: 0 \t Player 2: 0\t", bg="tan")
        game_score.grid(row=0, column=0, sticky="nsw")

        turn_counter = tk.Label(top_frame, text="\tTurn: 1\t\t", bg="tan")
        turn_counter.grid(row=0, column=1, sticky="ns")

        settings_btn = tk.Button(top_frame, text="Settings", padx=25, pady=5, command=self.new_game_settings)
        settings_btn.grid(row=0, column=3, sticky="e")

        return game_score, turn_counter

    def setup_game_board_and_nodes(self, frame, starting_setup=None):
        if starting_setup is None:
            starting_setup = self.DEFAULT_START
        game_board = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="#7F694C")
        game_board.grid(row=0, column=0)

        arr_len = len(starting_setup)
        nodes = [[None for row in range(arr_len)] for column in range(arr_len)]
        for row in range(arr_len):
            for column in range(arr_len):
                node_val = starting_setup[row][column]
                if node_val:
                    nodes[row][column] = tk.Button(game_board, padx=3, pady=3,
                                                   text=f"{chr(abs(arr_len - row) + 64)}{column}",
                                                   bg=self.PLAYER_COLOR_DICT[node_val],
                                                   fg="pink")
                    nodes[row][column].configure(font=("Consolas", 20))
                    nodes[row][column].grid(row=row, column=column * 2 + row + arr_len, columnspan=2)

        return game_board, nodes

    @staticmethod
    def setup_moves_history(frame):
        pad_y = 5
        history_frame = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, bg="brown")
        history_frame.grid(row=0, column=2, sticky="ns")

        history_p1 = tk.Label(history_frame, text="Player 1", pady=pad_y, bg="brown", fg="white")
        history_p1.grid(row=0, column=0, columnspan=2)
        history_p2 = tk.Label(history_frame, text="Player 2", pady=pad_y, bg="brown", fg="white")
        history_p2.grid(row=0, column=2, columnspan=2)

        hist_h = 30
        hist_w = 30, 15

        history_p1_move_label = tk.Label(history_frame, text="Move:", pady=pad_y, bg="brown",
                                         fg="white")
        history_p1_move_label.grid(row=1, column=0, sticky="w")
        history_p1_time_label = tk.Label(history_frame, text="Time:", pady=pad_y, bg="brown",
                                         fg="white")
        history_p1_time_label.grid(row=1, column=1, sticky="w")
        history_p2_move_label = tk.Label(history_frame, text="Move:", pady=pad_y, bg="brown",
                                         fg="white")
        history_p2_move_label.grid(row=1, column=2, sticky="w")
        history_p2_time_label = tk.Label(history_frame, text="Time:", pady=pad_y, bg="brown",
                                         fg="white")
        history_p2_time_label.grid(row=1, column=3, sticky="w")

        history_p1_move = tk.Listbox(history_frame, borderwidth=1, height=hist_h, width=hist_w[0])
        history_p1_move.grid(row=2, column=0)
        history_p1_time = tk.Listbox(history_frame, borderwidth=1, height=hist_h, width=hist_w[1])
        history_p1_time.grid(row=2, column=1)

        history_p2_move = tk.Listbox(history_frame, borderwidth=1, height=hist_h, width=hist_w[0])
        history_p2_move.grid(row=2, column=2)
        history_p2_time = tk.Listbox(history_frame, borderwidth=1, height=hist_h, width=hist_w[1])
        history_p2_time.grid(row=2, column=3)

        history_p1_total_time = tk.Label(history_frame, text="Total time: 0:00", pady=pad_y, bg="brown",
                                         fg="white")
        history_p1_total_time.grid(row=3, column=1)
        history_p2_total_time = tk.Label(history_frame, text="Total time: 0:00", pady=pad_y, bg="brown",
                                         fg="white")
        history_p2_total_time.grid(row=3, column=3)
        return history_p1_move, history_p1_time, history_p2_move, \
            history_p2_time, history_p1_total_time, history_p2_total_time

    def setup_bottom_frame(self):
        bottom_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="tan")
        bottom_frame.grid(row=3, sticky="ew")
        btn_pad_x = 25
        btn_pad_y = 5
        start_btn = tk.Button(bottom_frame, text="Start", padx=btn_pad_x, pady=btn_pad_y)
        start_btn.grid(row=0, column=0)
        pause_btn = tk.Button(bottom_frame, text="Pause", padx=btn_pad_x, pady=btn_pad_y)
        pause_btn.grid(row=0, column=1)
        stop_btn = tk.Button(bottom_frame, text="Stop", padx=btn_pad_x, pady=btn_pad_y)
        stop_btn.grid(row=0, column=2)
        reset_btn = tk.Button(bottom_frame, text="Reset", padx=btn_pad_x, pady=btn_pad_y)
        reset_btn.grid(row=0, column=3)
        undo_btn = tk.Button(bottom_frame, text="Undo", padx=btn_pad_x, pady=btn_pad_y)
        undo_btn.grid(row=0, column=4)

    def setup_directional_arrows(self):
        arrows_frame = tk.Frame(self.center_frame, relief=tk.RAISED, borderwidth=1)
        arrows_frame.grid(row=0, column=1, sticky="n")

        self.top_left_arrow = tk.Button(arrows_frame, text=" 🡔 ")
        self.top_left_arrow.configure(font=("Consolas", 20))
        self.top_left_arrow.grid(row=0, column=1, columnspan=2)

        self.top_right_arrow = tk.Button(arrows_frame, text=" 🡕 ")
        self.top_right_arrow.configure(font=("Consolas", 20))
        self.top_right_arrow.grid(row=0, column=3, columnspan=2)

        self.left_arrow = tk.Button(arrows_frame, text="🡐")
        self.left_arrow.configure(font=("Consolas", 20))
        self.left_arrow.grid(row=1, column=0, columnspan=2)

        self.right_arrow = tk.Button(arrows_frame, text="🡒")
        self.right_arrow.configure(font=("Consolas", 20))
        self.right_arrow.grid(row=1, column=4, columnspan=2)

        self.bottom_left_arrow = tk.Button(arrows_frame, text=" 🡗 ")
        self.bottom_left_arrow.configure(font=("Consolas", 20))
        self.bottom_left_arrow.grid(row=2, column=1, columnspan=2)

        self.bottom_right_arrow = tk.Button(arrows_frame, text=" 🡖 ")
        self.bottom_right_arrow.configure(font=("Consolas", 20))
        self.bottom_right_arrow.grid(row=2, column=3, columnspan=2)

    def new_game_settings(self):  # might have to mess with `self.` to get values to be returned.
        self.settings_window = tk.Toplevel(self.window)

        pad = 5

        layout_frame = tk.Frame(self.settings_window, relief=tk.GROOVE, borderwidth=1, padx=pad, pady=pad)
        self.layout_var = tk.IntVar()
        layout_radio_default = tk.Radiobutton(layout_frame, text="Default", variable=self.layout_var,
                                              value=Layout.DEFAULT.value)
        layout_radio_default.grid(row=0, column=0, sticky="w")
        layout_radio_belgian_daisy = tk.Radiobutton(layout_frame, text="Belgian Daisy", variable=self.layout_var,
                                                    value=Layout.BELGIAN_DAISY.value)
        layout_radio_belgian_daisy.grid(row=1, column=0, sticky="w")
        layout_radio_german_daisy = tk.Radiobutton(layout_frame, text="German Daisy", variable=self.layout_var,
                                                   value=Layout.GERMAN_DAISY.value)
        layout_radio_german_daisy.grid(row=2, column=0, sticky="w")
        layout_radio_default.select()
        layout_frame.grid(row=0, column=0, sticky="ew")

        colour_frame = tk.Frame(self.settings_window, relief=tk.GROOVE, borderwidth=1, padx=pad, pady=pad)
        self.colour_var = tk.IntVar()
        colour_radio1 = tk.Radiobutton(colour_frame, text="P1 = black, P2 = white", variable=self.colour_var,
                                       value=Colour.BLACK.value)
        colour_radio1.grid(row=0, column=0, sticky="w")
        colour_radio2 = tk.Radiobutton(colour_frame, text="P1 = white, P2 = black", variable=self.colour_var,
                                       value=Colour.WHITE.value)
        colour_radio2.grid(row=1, column=0, sticky="w")
        colour_radio1.select()
        colour_frame.grid(row=1, column=0, sticky="ew")

        gamemode_frame = tk.Frame(self.settings_window, relief=tk.GROOVE, borderwidth=1, padx=pad, pady=pad)
        self.gamemode_var = tk.IntVar()
        gamemode_radio_human_ai = tk.Radiobutton(gamemode_frame, text="Human vs AI", variable=self.gamemode_var,
                                                 value=Gamemode.HUMAN_HUMAN.value)
        gamemode_radio_human_ai.grid(row=0, column=0, sticky="w")
        gamemode_radio_human_ai.select()
        gamemode_radio_human_human = tk.Radiobutton(gamemode_frame, text="Human vs Human", variable=self.gamemode_var,
                                                    value=Gamemode.HUMAN_AI.value)
        gamemode_radio_human_human.grid(row=1, column=0, sticky="w")
        gamemode_radio_ai_ai = tk.Radiobutton(gamemode_frame, text="AI vs AI", variable=self.gamemode_var,
                                              value=Gamemode.AI_AI.value)
        gamemode_radio_ai_ai.grid(row=2, column=0, sticky="w")
        gamemode_frame.grid(row=2, column=0, sticky="ew")

        move_limit_frame = tk.Frame(self.settings_window, relief=tk.GROOVE, borderwidth=1, padx=pad, pady=pad)
        self.move_limit_var = tk.IntVar()
        move_limit_entry = tk.Entry(move_limit_frame, width=3, textvariable=self.move_limit_var)
        move_limit_entry.grid(row=0, column=0)
        move_limit_label = tk.Label(move_limit_frame, text="Move limit")
        move_limit_label.grid(row=0, column=1)
        move_limit_frame.grid(row=3, column=0, sticky="ew")

        time_limit_frame = tk.Frame(self.settings_window, relief=tk.GROOVE, borderwidth=1, padx=pad, pady=pad)
        self.time_limit_p1_var = tk.IntVar()
        time_limit_p1 = tk.Entry(time_limit_frame, width=3, textvariable=self.time_limit_p1_var)
        time_limit_p1.grid(row=0, column=0)
        time_limit_p1_label = tk.Label(time_limit_frame, text="P1 time limit per move (s)")
        time_limit_p1_label.grid(row=0, column=1)

        self.time_limit_p2_var = tk.IntVar()
        time_limit_p2 = tk.Entry(time_limit_frame, width=3, textvariable=self.time_limit_p2_var)
        time_limit_p2.grid(row=1, column=0)
        time_limit_p2_label = tk.Label(time_limit_frame, text="P2 time limit per move (s)")
        time_limit_p2_label.grid(row=1, column=1)
        time_limit_frame.grid(row=4, column=0, sticky="ew")

        ok_button = tk.Button(self.settings_window, relief=tk.RAISED, borderwidth=5, padx=pad, pady=pad,
                              text="Create new game with these settings!", command=self.set_and_get_settings)
        ok_button.grid(row=5, column=0, sticky="ew")

    def set_and_get_settings(self):
        self.settings = Settings(self.layout_var.get(), self.colour_var.get(), self.gamemode_var.get(),
                                 self.move_limit_var.get(), self.time_limit_p1_var.get(), self.time_limit_p2_var.get())
        self.settings_window.destroy()
        self.reset_game()

    def reset_game(self):
        # Top frame: Player Score, Turn Counter, Settings button
        self.game_score, self.turn_counter = self.setup_top_frame()

        # Game Board
        self.game_board, self.nodes = self.setup_game_board_and_nodes(self.center_frame,
                                                                      self.STARTING_LAYOUT[self.settings.layout])
        # Moves History
        self.history_p1_move, self.history_p1_time, \
            self.history_p2_move, self.history_p2_time, \
            self.history_p1_total_time, self.history_p2_total_time = self.setup_moves_history(self.center_frame)

    def run_gui(self):
        self.window.mainloop()

    def close_gui(self):
        self.window.destroy()
