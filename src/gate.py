

from collections import deque

class Gate:
    def __init__(self):
        # TODO: create two queues and a cycle pointer 0..3 for [F,R,R,R]
        self._pattern = ["fastpass","regular","regular","regular"]
        self._idx = 0
        self._fast = None  # TODO
        self._reg = None   # TODO

    def arrive(self, line, person_id):
        # TODO: enqueue into the chosen line
        raise NotImplementedError

    def serve(self):
        """
        Return the next person according to the repeating pattern.
        Skip empty lines but still move the cycle pointer correctly.
        Decide error behavior when both lines are empty.
        """
        raise NotImplementedError

    def peek_next_line(self):
        # TODO: compute which line would be served next (consider empties)
        raise NotImplementedError
