import copy

FACES = ['U', 'D', 'L', 'R', 'F', 'B']
MOVES = [1, 2, 3]

class Cube:
    def __init__(self, state):
        self.state = copy.deepcopy(state)
        self.moves_made = []
        self.record = False

    def move(self, move_tuple):
        face, turns = move_tuple if isinstance(move_tuple, tuple) else (move_tuple[0], 1)
        if self.record:
            self.moves_made.append((face, turns))
        self._apply_move(face, turns)
        return self

    def apply_move(self, move):
        if len(move) == 1:
            face = move
            turns = 1
        else:
            face = move[0]
            turns = int(move[1])
        return self.move((face, turns))

    def copy(self):
        new_cube = Cube(copy.deepcopy(self.state))
        new_cube.moves_made = list(self.moves_made)
        new_cube.record = self.record
        return new_cube

    def is_g1(self):
        return self._edges_oriented()

    def is_g2(self):
        return self._edges_oriented() and self._corners_oriented() and self._edges_in_slice()

    def is_g3(self):
        return self.is_g2() and self._parity_even() and self._pieces_in_slice()

    def is_solved(self):
        return all(len(set(self.state[face])) == 1 for face in FACES)

    def _apply_move(self, face, turns):
        for _ in range(turns):
            self._rotate_face(face)

    def _rotate_face(self, face):
        face_stickers = self.state[face]
        rotated = [
            face_stickers[6], face_stickers[3], face_stickers[0],
            face_stickers[7], face_stickers[4], face_stickers[1],
            face_stickers[8], face_stickers[5], face_stickers[2],
        ]
        self.state[face] = rotated

        adjacent_faces_map = {
            'U': [('B', [2,1,0]), ('R', [2,1,0]), ('F', [2,1,0]), ('L', [2,1,0])],
            'D': [('F', [6,7,8]), ('R', [6,7,8]), ('B', [6,7,8]), ('L', [6,7,8])],
            'F': [('U', [6,7,8]), ('R', [0,3,6]), ('D', [2,1,0]), ('L', [8,5,2])],
            'B': [('U', [2,1,0]), ('L', [0,3,6]), ('D', [6,7,8]), ('R', [8,5,2])],
            'L': [('U', [0,3,6]), ('F', [0,3,6]), ('D', [0,3,6]), ('B', [8,5,2])],
            'R': [('U', [8,5,2]), ('B', [0,3,6]), ('D', [8,5,2]), ('F', [8,5,2])],
        }

        adj = adjacent_faces_map[face]
        temp = [self.state[f][i] for f, idxs in adj for i in idxs]
        rotated_temp = temp[-3:] + temp[:-3]
        for (f, idxs), i in zip(adj, range(0, 12, 3)):
            for j, idx in enumerate(idxs):
                self.state[f][idx] = rotated_temp[i + j]

    def _edges_oriented(self):
        edges = [
            ('U', 7, 'F', 1), ('U', 5, 'R', 1), ('U', 1, 'B', 1), ('U', 3, 'L', 1),
            ('D', 1, 'F', 7), ('D', 5, 'R', 7), ('D', 7, 'B', 7), ('D', 3, 'L', 7),
            ('F', 5, 'R', 3), ('F', 3, 'L', 5), ('B', 5, 'L', 3), ('B', 3, 'R', 5),
        ]
        for (f1, i1, f2, i2) in edges:
            color1 = self.state[f1][i1]
            color2 = self.state[f2][i2]
            if f1 in ['U', 'D']:
                if color1 != self.state[f1][4]:
                    return False
            elif f2 in ['U', 'D']:
                if color2 != self.state[f2][4]:
                    return False
        return True

    def _corners_oriented(self):
        corners = [
            ('U', 8, 'R', 0, 'F', 2), ('U', 2, 'F', 0, 'L', 2), ('U', 0, 'L', 0, 'B', 2), ('U', 6, 'B', 0, 'R', 2),
            ('D', 8, 'F', 8, 'R', 6), ('D', 2, 'R', 8, 'B', 6), ('D', 0, 'B', 8, 'L', 6), ('D', 6, 'L', 8, 'F', 6),
        ]
        for f1, i1, f2, i2, f3, i3 in corners:
            colors = {self.state[f][4] for f in [f1, f2, f3]}
            piece_colors = {self.state[f1][i1], self.state[f2][i2], self.state[f3][i3]}
            if piece_colors != colors:
                return False
        return True

    def _edges_in_slice(self):
        middle_slice_edges = [
            ('F', 3, 'L', 5), ('F', 5, 'R', 3), ('B', 3, 'R', 5), ('B', 5, 'L', 3)
        ]
        for f1, i1, f2, i2 in middle_slice_edges:
            colors = {self.state[f1][i1], self.state[f2][i2]}
            expected_colors = {self.state[f1][4], self.state[f2][4]}
            if colors != expected_colors:
                return False
        return True

    def _parity_even(self):
        corner_positions = [
            ('U', 8, 'R', 0, 'F', 2), ('U', 2, 'F', 0, 'L', 2), ('U', 0, 'L', 0, 'B', 2), ('U', 6, 'B', 0, 'R', 2),
            ('D', 8, 'F', 8, 'R', 6), ('D', 2, 'R', 8, 'B', 6), ('D', 0, 'B', 8, 'L', 6), ('D', 6, 'L', 8, 'F', 6),
        ]

        corner_colors = [frozenset([self.state[f1][i1], self.state[f2][i2], self.state[f3][i3]])
                         for f1, i1, f2, i2, f3, i3 in corner_positions]

        solved_corner_colors = [frozenset([self.state[f][4] for f in faces])
                                for faces in [('U', 'R', 'F'), ('U', 'F', 'L'), ('U', 'L', 'B'), ('U', 'B', 'R'),
                                              ('D', 'F', 'R'), ('D', 'R', 'B'), ('D', 'B', 'L'), ('D', 'L', 'F')]]

        corner_permutation = [solved_corner_colors.index(color_set) for color_set in corner_colors]

        edge_positions = [
            ('U', 7, 'F', 1), ('U', 5, 'R', 1), ('U', 1, 'B', 1), ('U', 3, 'L', 1),
            ('D', 1, 'F', 7), ('D', 5, 'R', 7), ('D', 7, 'B', 7), ('D', 3, 'L', 7),
            ('F', 5, 'R', 3), ('F', 3, 'L', 5), ('B', 5, 'L', 3), ('B', 3, 'R', 5),
        ]

        edge_colors = [frozenset([self.state[f1][i1], self.state[f2][i2]]) for f1, i1, f2, i2 in edge_positions]

        solved_edge_colors = [frozenset([self.state[f][4], self.state[adj][4]])
                              for f, adj in [('U', 'F'), ('U', 'R'), ('U', 'B'), ('U', 'L'),
                                             ('D', 'F'), ('D', 'R'), ('D', 'B'), ('D', 'L'),
                                             ('F', 'R'), ('F', 'L'), ('B', 'L'), ('B', 'R')]]

        edge_permutation = [solved_edge_colors.index(color_set) for color_set in edge_colors]

        def permutation_parity(perm):
            parity = 0
            visited = [False] * len(perm)
            for i in range(len(perm)):
                if not visited[i]:
                    cycle_length = 0
                    j = i
                    while not visited[j]:
                        visited[j] = True
                        j = perm[j]
                        cycle_length += 1
                    if cycle_length > 0:
                        parity += cycle_length - 1
            return parity % 2

        corner_parity = permutation_parity(corner_permutation)
        edge_parity = permutation_parity(edge_permutation)

        return corner_parity == edge_parity

    def _pieces_in_slice(self):
        middle_slice_edges = [
            frozenset([self.state['F'][3], self.state['L'][5]]),
            frozenset([self.state['F'][5], self.state['R'][3]]),
            frozenset([self.state['B'][3], self.state['R'][5]]),
            frozenset([self.state['B'][5], self.state['L'][3]])
        ]

        expected_middle_slice_colors = [
            frozenset([self.state['F'][4], self.state['L'][4]]),
            frozenset([self.state['F'][4], self.state['R'][4]]),
            frozenset([self.state['B'][4], self.state['R'][4]]),
            frozenset([self.state['B'][4], self.state['L'][4]])
        ]

        for edge_colors in middle_slice_edges:
            if edge_colors not in expected_middle_slice_colors:
                return False

        return True
