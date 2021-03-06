"""
This module drives the Abalone-AI program via GUI.
"""
from gui.graphical_user_interface import GUI


def main():
    gui = GUI()
    gui.run_gui()


if __name__ == '__main__':
    main()
