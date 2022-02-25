import tkinter as tk

from array import *


class GUI:
    def __init__(self):
        self.node = [[None for row in range(11)] for column in range(11)]
        default_setup = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],  # 0 is not a space
                         [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0],  # 1 is black (player 1)
                         [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],  # 2 is white (player 2)
                         [0, 0, 0, 3, 3, 1, 1, 1, 3, 3, 0],  # 3 is empty
                         [0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                         [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0],
                         [0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
                         [0, 3, 3, 2, 2, 2, 3, 3, 0, 0, 0],
                         [0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0],
                         [0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.window = tk.Tk()
        self.window.title("Abalone AI")
        top_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, background="red")
        center_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, background="blue")
        bottom_frame = tk.Frame(self.window, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, background="yellow")

        self.game_score = tk.Label(top_frame, text="Player 1: 0 \t Player 2: 0")
        self.game_score.grid(row=0, column=0, sticky="n")

        self.turn = tk.Label(top_frame, text="Turn: 1")
        self.turn.grid(row=0, column=1, sticky="n")

        settings_button = tk.Button(top_frame, text="Settings", command=self.new_game_settings)
        settings_button.grid(row=0, column=26, sticky="e")

        self.main_game = tk.Frame(center_frame, relief=tk.RAISED, borderwidth=1, padx=3, pady=3, background="green")
        self.main_game.grid(row=0, column=0)

        for row in range(11):
            for column in range(11):
                if default_setup[row][column]:
                    self.node[row][column] = tk.Button(self.main_game, padx=2, pady=2, text=f"{chr(abs(11-row)+63)}{column}")
                    self.node[row][column].grid(row=row, column=column*2+row+11, columnspan=2)

        self.move_history = tk.Frame(center_frame, relief=tk.RAISED, borderwidth=1, background="orange")
        self.move_history_p1 = tk.Label(self.move_history, text="Player 1")
        self.move_history_p2 = tk.Label(self.move_history, text="Player 2")
        self.move_history_p1_total_time = tk.Label(self.move_history, text="Total time: 0:00")
        self.move_history_p2_total_time = tk.Label(self.move_history, text="Total time: 0:00")
        self.move_history_p1_move = tk.Listbox(self.move_history, borderwidth=1)
        self.move_history_p1_time = tk.Listbox(self.move_history, borderwidth=1)
        self.move_history_p2_move = tk.Listbox(self.move_history, borderwidth=1)
        self.move_history_p2_time = tk.Listbox(self.move_history, borderwidth=1)
        self.move_history_p1_move.insert(0, "Move:")
        self.move_history_p1_time.insert(0, "Time:")
        self.move_history_p2_move.insert(0, "Move:")
        self.move_history_p2_time.insert(0, "Time:")
        self.move_history_p1.grid(row=0, column=0, columnspan=2, sticky="s")
        self.move_history_p2.grid(row=0, column=2, columnspan=2, sticky="s")
        self.move_history_p1_move.grid(row=1, column=0)
        self.move_history_p1_time.grid(row=1, column=1)
        self.move_history_p2_move.grid(row=1, column=2)
        self.move_history_p2_time.grid(row=1, column=3)
        self.move_history_p1_total_time.grid(row=2, column=1)
        self.move_history_p2_total_time.grid(row=2, column=3)
        self.move_history.grid(row=0, column=1)

        self.start = tk.Button(bottom_frame, text="Start")
        self.stop = tk.Button(bottom_frame, text="Stop")
        self.pause = tk.Button(bottom_frame, text="Pause")
        self.reset = tk.Button(bottom_frame, text="Reset")
        self.undo = tk.Button(bottom_frame, text="Undo")

        self.start.grid(row=0, column=0)
        self.stop.grid(row=0, column=1)
        self.pause.grid(row=0, column=2)
        self.reset.grid(row=0, column=3)
        self.undo.grid(row=0, column=4)

        top_frame.grid(row=0, sticky="ew")
        center_frame.grid(row=1, sticky="nsew")
        bottom_frame.grid(row=3, sticky="ew")

    def new_game_settings(self):
        settings_window = tk.Toplevel(self.window)
        toggle_layout = tk.Button(settings_window, text="*")
        toggle_colour = tk.Button(settings_window, text="*")
        toggle_gamemode = tk.Button(settings_window, text="*")
        move_limit = tk.Entry(settings_window, width=10)
        time_limit_p1 = tk.Entry(settings_window, width=10)
        time_limit_p2 = tk.Entry(settings_window, width=10)
        toggle_layout_label = tk.Label(settings_window, text="Default")
        toggle_colour_label = tk.Label(settings_window, text="Player 1 = black, Player 2 = white")
        toggle_gamemode_label = tk.Label(settings_window, text="Human vs Human")
        move_limit_label = tk.Label(settings_window, text="Move limit")
        time_limit_p1_label = tk.Label(settings_window, text="Player 1 time limit")
        time_limit_p2_label = tk.Label(settings_window, text="Player 2 time limit")

        toggle_layout.grid(row=0, column=0)
        toggle_colour.grid(row=1, column=0)
        toggle_gamemode.grid(row=2, column=0)
        move_limit.grid(row=3, column=0)
        time_limit_p1.grid(row=4, column=0)
        time_limit_p2.grid(row=5, column=0)
        toggle_layout_label.grid(row=0, column=1)
        toggle_colour_label.grid(row=1, column=1)
        toggle_gamemode_label.grid(row=2, column=1)
        move_limit_label.grid(row=3, column=1)
        time_limit_p1_label.grid(row=4, column=1)
        time_limit_p2_label.grid(row=5, column=1)

    def run_gui(self):
        self.window.mainloop()

    def close_gui(self):
        self.window.destroy()
