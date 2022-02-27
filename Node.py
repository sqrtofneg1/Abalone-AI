"""
NAME
    Node

DESCRIPTION:
    This module contains methods/functions/variables that belong and support the Node class that is below.
"""
class Node:
    def __init__(self, state):
        """
        Initialize's data members and constructs a Node object.
        """
        self._state = state

    def get_state(self):
        """
        This method returns the self._state variable
        """
        return self._state

    def set_state(self, state):
        """
        This method sets the  self._state variable to the state parameter
        """
        self._state = state
