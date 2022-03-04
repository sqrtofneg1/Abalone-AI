import tkinter as tk

from game import Game
from settings import *
import node_arrays


class GUI:

    PLAYER_COLOR_DICT = {1: "black", 2: "white", 3: "grey"}

    def __init__(self, settings=Settings.default_settings()):
        self.window = tk.Tk()
        self.window.title("Abalone AI")

        self.settings_window = None
        self.layout_var = None
        self.colour_var = None
        self.gamemode_var = None
        self.move_limit_var = None
        self.time_limit_p1_var = None
        self.time_limit_p2_var = None
        self.settings = settings

        # Center frame: Game Board, Moves History
        self.center_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="#7F694C")
        self.center_frame.grid(row=1, sticky="nsew")

        options_frame = tk.Frame(self.center_frame, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="#d5a976")
        options_frame.grid(row=0, column=1, sticky="ns")
        self.setup_directional_arrows(options_frame)
        self.setup_options_frame(options_frame)

        self.game_score = None
        self.turn_counter = None
        self.game_board = None
        self.nodes = None
        self.history_p1_time = None
        self.history_p1_move = None
        self.history_p1_total_time = None
        self.history_p2_time = None
        self.history_p2_move = None
        self.history_p2_total_time = None
        self.game = self.reset_game()
        print(self.game.state_rep)

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
            starting_setup = node_arrays.STARTING_LAYOUT
        game_board = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="#7F694C")
        game_board.grid(row=0, column=0)

        arr_len = len(starting_setup)
        nodes = [[None for _ in range(arr_len)] for _ in range(arr_len)]
        for row in range(arr_len):
            for column in range(arr_len):
                node_val = starting_setup[row][column]
                if node_val:
                    nodes[row][column] = tk.Button(game_board, padx=3, pady=3,
                                                   text=f"{chr(abs(arr_len - row) + 63)}{column}",
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

    @staticmethod
    def setup_options_frame(frame):
        btn_pad_x = 25
        btn_pad_y = 5
        pad_y = 10
        start_btn = tk.Button(frame, text="Start", padx=btn_pad_x, pady=btn_pad_y)
        start_btn.grid(row=1, column=0, pady=pad_y)
        pause_btn = tk.Button(frame, text="Pause", padx=btn_pad_x, pady=btn_pad_y)
        pause_btn.grid(row=2, column=0, pady=pad_y)
        stop_btn = tk.Button(frame, text="Stop", padx=btn_pad_x, pady=btn_pad_y)
        stop_btn.grid(row=3, column=0, pady=pad_y)
        reset_btn = tk.Button(frame, text="Reset", padx=btn_pad_x, pady=btn_pad_y)
        reset_btn.grid(row=4, column=0, pady=pad_y)
        undo_btn = tk.Button(frame, text="Undo", padx=btn_pad_x, pady=btn_pad_y)
        undo_btn.grid(row=5, column=0, pady=pad_y)

    @staticmethod
    def setup_directional_arrows(frame):
        arrows_frame = tk.Frame(frame, relief=tk.RAISED, borderwidth=1)
        arrows_frame.grid(row=0, column=0, sticky="n", pady=10)

        top_left_arrow = tk.Button(arrows_frame, text=" 🡔 ")
        top_left_arrow.configure(font=("Consolas", 20))
        top_left_arrow.grid(row=0, column=1, columnspan=2)

        top_right_arrow = tk.Button(arrows_frame, text=" 🡕 ")
        top_right_arrow.configure(font=("Consolas", 20))
        top_right_arrow.grid(row=0, column=3, columnspan=2)

        left_arrow = tk.Button(arrows_frame, text="🡐")
        left_arrow.configure(font=("Consolas", 20))
        left_arrow.grid(row=1, column=0, columnspan=2)

        right_arrow = tk.Button(arrows_frame, text="🡒")
        right_arrow.configure(font=("Consolas", 20))
        right_arrow.grid(row=1, column=4, columnspan=2)

        bottom_left_arrow = tk.Button(arrows_frame, text=" 🡗 ")
        bottom_left_arrow.configure(font=("Consolas", 20))
        bottom_left_arrow.grid(row=2, column=1, columnspan=2)

        bottom_right_arrow = tk.Button(arrows_frame, text=" 🡖 ")
        bottom_right_arrow.configure(font=("Consolas", 20))
        bottom_right_arrow.grid(row=2, column=3, columnspan=2)

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
                                                                      node_arrays.STARTING_LAYOUT[self.settings.layout])
        # Moves History
        self.history_p1_move, self.history_p1_time, \
            self.history_p2_move, self.history_p2_time, \
            self.history_p1_total_time, self.history_p2_total_time = self.setup_moves_history(self.center_frame)

        return Game(self.settings)

    def run_gui(self):
        self.window.mainloop()

    def close_gui(self):
        self.window.destroy()
