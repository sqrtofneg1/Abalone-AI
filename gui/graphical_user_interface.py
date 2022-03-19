"""
This module houses the GUI class.
"""
import tkinter as tk

from core.game import Game
from gui.settings import *
from layouts import layout_arrays


class GUI:
    PLAYER_COLOR_DICT = {1: "black", 2: "white", 3: "grey"}

    def __init__(self, settings=Settings.default_settings()):
        """
        Initializes the GUI.

        :param settings: a Settings object
        """
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
        self.setup_ai_next_move(options_frame)
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
        self.ai_next_move = None
        self.game = self.reset_game()
        print(self.game.state)
        print(self.game.state.get_nodes_count_for_player(1))
        self.selected_nodes = set()

    @staticmethod
    def setup_moves_history(frame):
        """
        Sets up the move history section.

        :param frame: the frame to draw this section in
        :return: Label and Listbox objects created in this section
        """
        pad_y = 5
        history_frame = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, bg="brown")
        history_frame.grid(row=0, column=2, sticky="ns")

        history_p1 = tk.Label(history_frame, text="Player 1", bg="brown", fg="white")
        history_p1.configure(font=("Segoe UI", 16))
        history_p1.grid(row=0, column=0, columnspan=2)
        history_p2 = tk.Label(history_frame, text="Player 2", bg="brown", fg="white")
        history_p2.configure(font=("Segoe UI", 16))
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
        """
        Sets up the options section.

        :param frame: the frame to draw in
        :return: None
        """
        btn_pad_x = 25
        btn_pad_y = 5
        pad_y = 10
        start_btn = tk.Button(frame, text="Start", padx=btn_pad_x, pady=btn_pad_y)
        start_btn.grid(row=2, column=0, pady=pad_y)
        pause_btn = tk.Button(frame, text="Pause", padx=btn_pad_x, pady=btn_pad_y)
        pause_btn.grid(row=3, column=0, pady=pad_y)
        stop_btn = tk.Button(frame, text="Stop", padx=btn_pad_x, pady=btn_pad_y)
        stop_btn.grid(row=4, column=0, pady=pad_y)
        reset_btn = tk.Button(frame, text="Reset", padx=btn_pad_x, pady=btn_pad_y)
        reset_btn.grid(row=5, column=0, pady=pad_y)
        undo_btn = tk.Button(frame, text="Undo", padx=btn_pad_x, pady=btn_pad_y)
        undo_btn.grid(row=6, column=0, pady=pad_y)

    @staticmethod
    def is_valid_selection(start_marble, end_marble):
        """
        Checks that the selected marbles (from start to end) are in-line
        and only counts up to 3 marbles total.

        :param start_marble: the first of the selected marbles
        :param end_marble: the last of the selected marbles
        :return: True if the selection is valid, False otherwise
        """
        pass  # TODO: implementation

    def setup_top_frame(self):
        """
        Sets up the frame at the top of the main window.

        :return: the game score and turn counter Labels
        """
        top_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="tan")
        top_frame.grid(row=0, sticky="ew")
        top_frame.grid_columnconfigure(0, weight=1)
        top_frame.grid_columnconfigure(1, weight=1)
        top_frame.grid_columnconfigure(2, weight=1)

        settings_btn = tk.Button(top_frame, text="Settings", padx=25, pady=3, command=self.new_game_settings)
        settings_btn.grid(row=0, column=0, sticky="nsw")

        game_score = tk.Label(top_frame, text="Player 1: 0 \t Player 2: 0", bg="tan")
        game_score.configure(font=("Consolas", 24))
        game_score.grid(row=0, column=1, sticky="ns")

        turn_counter = tk.Label(top_frame, text="Turn: 1", bg="tan", padx=20)
        turn_counter.configure(font=("Consolas", 14))
        turn_counter.grid(row=0, column=2, sticky="nse")

        return game_score, turn_counter

    def setup_game_board_and_nodes(self, frame, starting_setup=None):
        """
        Sets up the game board section.

        :param frame: the frame to draw in
        :param starting_setup: the starting layout of the game
        :return: the game board Frame
        """
        if starting_setup is None:
            starting_setup = layout_arrays.STARTING_LAYOUT
        game_board = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="#7F694C")
        game_board.grid(row=0, column=0)

        arr_len = len(starting_setup)
        self.nodes = [[None for _ in range(arr_len)] for _ in range(arr_len)]
        for row in range(arr_len):
            for column in range(arr_len):
                node_val = starting_setup[row][column]
                if node_val:
                    self.nodes[row][column] = tk.Button(game_board, padx=3, pady=3,
                                                        text=f"{chr(abs(arr_len - row) + 63)}{column}",
                                                        bg=self.PLAYER_COLOR_DICT[node_val],
                                                        fg="pink",
                                                        font=("Consolas", 20))
                    self.nodes[row][column].grid(row=row, column=column * 2 + row + arr_len, columnspan=2)
                    self.nodes[row][column].configure(command=lambda x=row, y=column: self.node_selected(x, y))

        return game_board

    def setup_ai_next_move(self, frame):
        """
        Sets up the section displaying the AI's next move.

        :param frame: the frame to draw in
        :return: None
        """
        ai_next_move_frame = tk.Frame(frame, relief=tk.RAISED, borderwidth=1, bg="#d5a976")
        ai_next_move_frame.grid(row=0, column=0, sticky="ew")

        ai_next_move_label = tk.Label(ai_next_move_frame, text="AI's next move:", bg="#d5a976")
        ai_next_move_label.grid(row=0, column=0, sticky="w")

        self.ai_next_move = tk.Label(ai_next_move_frame, text="Next move here", bg="#d5a976")
        self.ai_next_move.grid(row=1, column=0, sticky="ew")

    def setup_directional_arrows(self, frame):
        """
        Sets up the arrow buttons for directional moves.

        :param frame: the frame to draw in
        :return: None
        """
        arrows_frame = tk.Frame(frame, relief=tk.RAISED, borderwidth=1)
        arrows_frame.grid(row=1, column=0, sticky="n", pady=10)

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

        clear_selection = tk.Button(arrows_frame, text="Clear \n Selection", command=self.clear_selection)
        clear_selection.grid(row=1, column=2, columnspan=2, sticky="nsew")

    def new_game_settings(self):  # might have to mess with `self.` to get values to be returned.
        """
        Sets up the settings window.

        :return: None
        """
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
        """
        Sets the game's settings based on user choices made in the settings window.

        :return: None
        """
        self.settings = Settings(self.layout_var.get(), self.colour_var.get(), self.gamemode_var.get(),
                                 self.move_limit_var.get(), self.time_limit_p1_var.get(), self.time_limit_p2_var.get())
        self.settings_window.destroy()
        self.reset_game()

    def reset_game(self):
        """
        Resets the game to the beginning.

        :return:
        """
        # Top frame: Player Score, Turn Counter, Settings button
        self.game_score, self.turn_counter = self.setup_top_frame()

        # Game Board
        self.game_board = self.setup_game_board_and_nodes(self.center_frame,
                                                          layout_arrays.STARTING_LAYOUT[self.settings.layout])
        # Moves History
        self.history_p1_move, self.history_p1_time, \
            self.history_p2_move, self.history_p2_time, \
            self.history_p1_total_time, self.history_p2_total_time = self.setup_moves_history(self.center_frame)

        return Game(self.settings)

    def node_selected(self, row, column):
        """
        Changes the node colors to indicate selection and adds
        the node to the list of selected nodes.

        :param row: an int
        :param column: an int
        :return: None
        """
        button = self.nodes[row][column]

        if button not in self.selected_nodes:
            button.configure(relief=tk.SUNKEN)
            button.configure(fg="yellow")
            self.selected_nodes.add(button)
        else:
            button.configure(relief=tk.RAISED)
            button.configure(fg="pink")
            self.selected_nodes.remove(button)
        print(f"{button['text']} selected")

    def clear_selection(self):
        """
        Removes node selection coloring, and removes the node
        from the list of selected nodes.

        :return: None
        """
        for button in self.selected_nodes:
            button.configure(relief=tk.RAISED)
            button.configure(fg="pink")
        self.selected_nodes.clear()

    def run_gui(self):
        """
        Starts rendering the main window.

        :return: None
        """
        self.window.mainloop()

    def close_gui(self):
        """
        Stops rendering the main window.

        :return: None
        """
        self.window.destroy()
