import copy

class Cube:
    def __init__(self, state):
        pass

    def apply_move(self, move):
        pass

    def is_g1(self):
        return self._edges_oriented()

    def is_g2(self):
        return self._edges_oriented() and self._corners_oriented() and self._edges_in_slice()

    def is_g3(self):
        return self.is_g2() and self._parity_even() and self._pieces_in_slice()

