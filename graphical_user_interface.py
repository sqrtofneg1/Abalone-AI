import tkinter as tk


class GUI:
    """
    - 0 is not a space
    - 1 is black (player 1)
    - 2 is white (player 2)
    - 3 is empty
    """
    DEFAULT_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
                     [0, 0, 0, 0, 2, 2, 2, 2, 2, 2],
                     [0, 0, 0, 3, 3, 2, 2, 2, 3, 3],
                     [0, 0, 3, 3, 3, 3, 3, 3, 3, 3],
                     [0, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                     [0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                     [0, 3, 3, 1, 1, 1, 3, 3, 0, 0],
                     [0, 1, 1, 1, 1, 1, 1, 0, 0, 0],
                     [0, 1, 1, 1, 1, 1, 0, 0, 0, 0]]

    BELGIAN_DAISY_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 2, 2, 3, 1, 1],
                           [0, 0, 0, 0, 2, 2, 2, 1, 1, 1],
                           [0, 0, 0, 3, 2, 2, 3, 1, 1, 3],
                           [0, 0, 3, 3, 3, 3, 3, 3, 3, 3],
                           [0, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                           [0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                           [0, 3, 1, 1, 3, 2, 2, 3, 0, 0],
                           [0, 1, 1, 1, 2, 2, 2, 0, 0, 0],
                           [0, 1, 1, 3, 2, 2, 0, 0, 0, 0]]

    GERMAN_DAISY_START = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 1, 1, 3, 2, 2],
                          [0, 0, 0, 0, 1, 1, 1, 2, 2, 2],
                          [0, 0, 0, 3, 1, 1, 3, 2, 2, 3],
                          [0, 0, 3, 3, 3, 3, 3, 3, 3, 3],
                          [0, 3, 3, 3, 3, 3, 3, 3, 3, 3],
                          [0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                          [0, 3, 2, 2, 3, 1, 1, 3, 0, 0],
                          [0, 2, 2, 2, 1, 1, 1, 0, 0, 0],
                          [0, 2, 2, 3, 1, 1, 0, 0, 0, 0]]

    PLAYER_COLOR_DICT = {1: "black", 2: "white", 3: "grey"}

    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Abalone AI")

        # Top frame: Player Score, Turn Counter
        self.game_score, self.turn_counter = self.setup_top_frame()

        # Center frame: Game Board, Moves History
        center_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, bg="#7F694C")
        center_frame.grid(row=1, sticky="nsew")
        # Game Board
        self.game_board, self.nodes = self.setup_game_board_and_nodes(center_frame, self.BELGIAN_DAISY_START)
        # Moves History
        self.history_p1_move, self.history_p1_time, \
            self.history_p2_move, self.history_p2_time, \
            self.history_p1_total_time, self.history_p2_total_time = self.setup_moves_history(center_frame)

        # Bottom frame: Start, Pause, Stop, Reset, Undo buttons
        self.setup_bottom_frame()

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
        history_frame.grid(row=0, column=1, sticky="ns")

        history_p1 = tk.Label(history_frame, text="Player 1", pady=pad_y, bg="brown", fg="white")
        history_p1.grid(row=0, column=0, columnspan=2)
        history_p2 = tk.Label(history_frame, text="Player 2", pady=pad_y, bg="brown", fg="white")
        history_p2.grid(row=0, column=2, columnspan=2)

        hist_h = 30
        hist_w = 35, 15
        history_p1_move = tk.Listbox(history_frame, borderwidth=1, height=hist_h, width=hist_w[0])
        history_p1_move.insert(0, "Move:")
        history_p1_move.grid(row=1, column=0)
        history_p1_time = tk.Listbox(history_frame, borderwidth=1, height=hist_h, width=hist_w[1])
        history_p1_time.insert(0, "Time:")
        history_p1_time.grid(row=1, column=1)

        history_p2_move = tk.Listbox(history_frame, borderwidth=1, height=hist_h, width=hist_w[0])
        history_p2_move.insert(0, "Move:")
        history_p2_move.grid(row=1, column=2)
        history_p2_time = tk.Listbox(history_frame, borderwidth=1, height=hist_h, width=hist_w[1])
        history_p2_time.insert(0, "Time:")
        history_p2_time.grid(row=1, column=3)

        history_p1_total_time = tk.Label(history_frame, text="Total time: 0:00", pady=pad_y, bg="brown",
                                         fg="white")
        history_p1_total_time.grid(row=2, column=1)
        history_p2_total_time = tk.Label(history_frame, text="Total time: 0:00", pady=pad_y, bg="brown",
                                         fg="white")
        history_p2_total_time.grid(row=2, column=3)
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

    def new_game_settings(self):
        settings_window = tk.Toplevel(self.window)

        toggle_layout = tk.Button(settings_window, text="*")
        toggle_layout.grid(row=0, column=0)
        toggle_layout_label = tk.Label(settings_window, text="Default")
        toggle_layout_label.grid(row=0, column=1)

        toggle_colour = tk.Button(settings_window, text="*")
        toggle_colour.grid(row=1, column=0)
        toggle_colour_label = tk.Label(settings_window, text="Player 1 = black, Player 2 = white")
        toggle_colour_label.grid(row=1, column=1)

        toggle_gamemode = tk.Button(settings_window, text="*")
        toggle_gamemode.grid(row=2, column=0)
        toggle_gamemode_label = tk.Label(settings_window, text="Human vs Human")
        toggle_gamemode_label.grid(row=2, column=1)

        move_limit = tk.Entry(settings_window, width=10)
        move_limit.grid(row=3, column=0)
        move_limit_label = tk.Label(settings_window, text="Move limit")
        move_limit_label.grid(row=3, column=1)

        time_limit_p1 = tk.Entry(settings_window, width=10)
        time_limit_p1.grid(row=4, column=0)
        time_limit_p1_label = tk.Label(settings_window, text="Player 1 time limit")
        time_limit_p1_label.grid(row=4, column=1)

        time_limit_p2 = tk.Entry(settings_window, width=10)
        time_limit_p2.grid(row=5, column=0)
        time_limit_p2_label = tk.Label(settings_window, text="Player 2 time limit")
        time_limit_p2_label.grid(row=5, column=1)

    def run_gui(self):
        self.window.mainloop()

    def close_gui(self):
        self.window.destroy()
