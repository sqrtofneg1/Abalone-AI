"""
This module houses the GUI class.
"""
import random
import tkinter as tk

from ai.heuristics import HeuristicsBach, HeuristicsSunmin, HeuristicsMan
from core.move import Direction, Move, MoveType, ChangeMatrix
from core.node import NodeValue, Node
from state_space_gen.state_space_generator import StateSpaceGenerator
from core.game import Game
from gui.settings import *
from layouts import layout_arrays
from ai.search import AlphaBeta


class GUI:
    """
    The game's graphical user interface.
    """

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
        self.selected_buttons = set()

        self.alpha_beta = AlphaBeta(2)
        # HEURISTICS
        self.heuristic1 = HeuristicsBach.evaluate  # for Black
        self.heuristic2 = HeuristicsSunmin.heuristic  # for White

        # Man's Codes
        self.player_1_previous_nodes_undo = None
        self.player_2_previous_nodes_undo = None
        self.setup_options_frame(options_frame)  # Moved here by Man, need self.game & undo moves to be made first

        self.player_1_move_counter = -1
        self.player_2_move_counter = -1

        self.new_game_settings()
        self.set_and_get_settings()

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
        hist_w = 15, 15

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

    def setup_options_frame(self, frame):
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
        undo_btn = tk.Button(frame, text="Undo", padx=btn_pad_x, pady=btn_pad_y, command=self.undo_move)
        undo_btn.grid(row=6, column=0, pady=pad_y)

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
        top_left_arrow.configure(command=lambda direction=Direction.TL: self.apply_move(direction))

        top_right_arrow = tk.Button(arrows_frame, text=" 🡕 ")
        top_right_arrow.configure(font=("Consolas", 20))
        top_right_arrow.grid(row=0, column=3, columnspan=2)
        top_right_arrow.configure(command=lambda direction=Direction.TR: self.apply_move(direction))

        left_arrow = tk.Button(arrows_frame, text="🡐")
        left_arrow.configure(font=("Consolas", 20))
        left_arrow.grid(row=1, column=0, columnspan=2)
        left_arrow.configure(command=lambda direction=Direction.L: self.apply_move(direction))

        right_arrow = tk.Button(arrows_frame, text="🡒")
        right_arrow.configure(font=("Consolas", 20))
        right_arrow.grid(row=1, column=4, columnspan=2)
        right_arrow.configure(command=lambda direction=Direction.R: self.apply_move(direction))

        bottom_left_arrow = tk.Button(arrows_frame, text=" 🡗 ")
        bottom_left_arrow.configure(font=("Consolas", 20))
        bottom_left_arrow.grid(row=2, column=1, columnspan=2)
        bottom_left_arrow.configure(command=lambda direction=Direction.BL: self.apply_move(direction))

        bottom_right_arrow = tk.Button(arrows_frame, text=" 🡖 ")
        bottom_right_arrow.configure(font=("Consolas", 20))
        bottom_right_arrow.grid(row=2, column=3, columnspan=2)
        bottom_right_arrow.configure(command=lambda direction=Direction.BR: self.apply_move(direction))

        clear_selection = tk.Button(arrows_frame, text="Clear \n Selection", command=self.clear_selection)
        clear_selection.grid(row=1, column=2, columnspan=2, sticky="nsew")

    def new_game_settings(self):
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
                                                 value=GameMode.HUMAN_AI.value)
        gamemode_radio_human_ai.grid(row=0, column=0, sticky="w")
        gamemode_radio_human_ai.select()
        gamemode_radio_human_human = tk.Radiobutton(gamemode_frame, text="Human vs Human", variable=self.gamemode_var,
                                                    value=GameMode.HUMAN_HUMAN.value)
        gamemode_radio_human_human.grid(row=1, column=0, sticky="w")
        gamemode_radio_ai_ai = tk.Radiobutton(gamemode_frame, text="AI vs AI", variable=self.gamemode_var,
                                              value=GameMode.AI_AI.value)
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
        self.game = self.reset_game()
        self.random_first_move()
        self.ai_vs_ai()

    def ai_vs_ai(self):
        if self.gamemode_var.get() == GameMode.AI_AI.value:
            while not self.game.is_game_over():
                self.make_ai_move()

    def random_first_move(self):
        if (self.gamemode_var.get() == GameMode.HUMAN_AI.value) and (
                self.game.state.player == 1) and (self.game.turn_counter == 1)\
                and (self.colour_var.get() == 2):
            print("in random first move")
            state_gen = StateSpaceGenerator(self.game.state)
            moves = state_gen.generate_all_valid_moves()
            move = moves[random.randint(0, len(moves) - 1)]
            self.history_p1_move.insert(tk.END, repr(move))

            self.game.apply_move(move)
            self.player_1_previous_nodes_undo = self.game.last_state.board
            self.player_1_move_counter = self.player_1_move_counter + 1
            self.redraw()

    def update_game_status(self):
        self.game.is_game_over()

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

        if button not in self.selected_buttons:
            button.configure(relief=tk.SUNKEN)
            button.configure(fg="yellow")
            self.selected_buttons.add(button)
        else:
            button.configure(relief=tk.RAISED)
            button.configure(fg="pink")
            self.selected_buttons.remove(button)

    def clear_selection(self):
        """
        Clears selected buttons and color changes.

        :return: None
        """
        # print(self.colour_var.get())  #To get the value of a colour White is 2 Black is 1
        for button in self.selected_buttons:
            button.configure(relief=tk.RAISED)
            button.configure(fg="pink")
        self.selected_buttons.clear()

    def get_move_from_gui(self, direction):
        """
        Returns a move derived from the nodes selection and direction selected.

        :param direction: a Direction enum object
        :return: a Move object or None
        """
        # Validation
        selection_size = len(self.selected_buttons)
        if selection_size == 0 or selection_size > 3:
            return None
        nodes = []
        for button in self.selected_buttons:
            text = button['text']
            row = int(Node.get_row_from_alpha(text[0]))
            col = int(text[1])
            nodes.append(self.game.state.get_node(row, col))
        for node in nodes:
            if node.node_value.value is not self.game.state.player:
                return None
        if selection_size == 1:
            for node in nodes:
                result_row = node.row + direction.value[0][0]
                result_column = node.column + direction.value[0][1]
                adj_node = self.game.state.get_node(result_row, result_column)
                if adj_node.node_value.value == NodeValue.EMPTY.value:
                    change_matrix = ChangeMatrix(self.game.state.player,
                                                 [node], [adj_node])
                    return Move(MoveType.Inline, node, node, direction, change_matrix)
        else:
            directions_between_nodes = set()
            for node1 in nodes:
                for node2 in nodes:
                    # now we have 2 or 3 nodes that are all current player's marbles
                    adj_nodes = [(direct, self.game.state.get_node_in_direction_of_node(node1, direct))
                                 for direct in Direction]
                    for adj_node in adj_nodes:
                        if node2 == adj_node[1]:
                            directions_between_nodes.add(adj_node[0])

            # if all the nodes are in a line
            if len(directions_between_nodes) == 2:
                start_and_end_nodes = []
                for direction_between in directions_between_nodes:
                    for node in nodes:
                        if self.game.state.get_node_in_direction_of_node(node, direction_between) not in nodes:
                            start_and_end_nodes.append(node)

                generator = StateSpaceGenerator(self.game.state)
                if selection_size == 2:
                    move = generator.process_two_marble_move(Move(MoveType.Unknown, start_and_end_nodes[0],
                                                                  start_and_end_nodes[1], direction))
                else:
                    move = generator.process_three_marble_move(Move(MoveType.Unknown, start_and_end_nodes[0],
                                                                    start_and_end_nodes[1], direction))
                if move.move_type is not MoveType.Invalid:
                    return move
                else:
                    return None

    def apply_move(self, direction):
        """
        Applies the user's inputted marble selection and direction as a move.

        :param direction: a Direction enum object
        :return: None
        """
        move = self.get_move_from_gui(direction)
        self.clear_selection()
        if move:
            if self.game.state.player == 1:
                self.player_1_make_move(move)
            else:
                self.player_2_make_move(move)
            if self.gamemode_var.get() == GameMode.HUMAN_AI.value:
                self.make_ai_move()
        else:
            print("Error, invalid move.")

    def make_ai_move(self):
        heuristic = self.heuristic1 if self.game.state.player == 1 else self.heuristic2
        ai_move = self.alpha_beta.start_new_search(self.game.state, heuristic)
        if self.game.state.player == 1:
            self.player_1_make_move(ai_move)
        else:
            self.player_2_make_move(ai_move)
        if self.gamemode_var == GameMode.AI_AI.value:
            if not self.game.is_game_over():
                self.make_ai_move()

    def update_turn_counter(self):
        """
        Updates the turn counter to reflect the state change.

        :return: None
        """
        self.turn_counter['text'] = f"Turn: {(self.game.turn_counter + 1) // 2}"
        self.turn_counter.update()

    def update_score(self):
        """
        Updates the score to reflect the state change.

        :return: None
        """
        self.game_score['text'] = \
            f"Player 1: {self.game.state.scores[0]} \t Player 2: {self.game.state.scores[1]}"
        self.game_score.update()

    def update_nodes(self):
        """
        Updates the nodes on the game board to reflect the state change.

        :return: None
        """
        for row in range(11):
            for column in range(11):
                node = self.game.state.get_node(row, column)
                if node.node_value.value is not NodeValue.INVALID.value:
                    # TEST: print row and column
                    # print("row = " + str(row))
                    # print("column = " + str(column))
                    self.nodes[row][column].configure(bg=self.PLAYER_COLOR_DICT[node.node_value.value])
                    self.nodes[row][column].update()

    def redraw(self):
        """
        Updates the UI to reflect the state change.

        :return: None
        """
        self.update_score()
        self.update_turn_counter()
        self.update_nodes()
        self.update_game_status()

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

    def player_1_make_move(self, move):
        self.history_p1_move.insert(tk.END, repr(move))
        self.game.apply_move(move)
        self.player_1_previous_nodes_undo = self.game.last_state.board
        self.player_1_move_counter = self.player_1_move_counter + 1
        self.redraw()

    def player_2_make_move(self, move):
        self.history_p2_move.insert(tk.END, repr(move))
        self.game.apply_move(move)
        self.player_2_previous_nodes_undo = self.game.last_state.board
        self.player_2_move_counter = self.player_2_move_counter + 1
        self.redraw()

    def undo_move(self):
        if self.game.state.player == 1:
            self.game.state.board = self.player_1_previous_nodes_undo
            self.history_p1_move.delete(self.player_1_move_counter)
            self.player_1_move_counter = self.player_1_move_counter - 1
            self.redraw()
        else:
            self.game.state.board = self.player_2_previous_nodes_undo
            self.history_p2_move.delete(self.player_2_move_counter)
            self.player_2_move_counter = self.player_2_move_counter - 1
            self.redraw()
