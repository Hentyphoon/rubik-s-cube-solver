import copy

class Cube:
    def __init__(self, state):
        self.state = copy.deepcopy(state)

    def apply_move(self, move):
        pass

    def is_g1(self):
         return self.get_wrong_edge_orientations() == 0

    def is_g2(self):
        return self.get_wrong_corner_orientations() == 0

    def is_g3(self):
        return self.get_edge_permutation_score() == 0
    
    def is_solved(self):
        return all(len(set(face)) == 1 for face in self.state.values())

    def copy(self):
        return Cube(copy.deepcopy(self.state))