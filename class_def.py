import copy

class Cube:
    def __init__(self, state):
        self.state = copy.deepcopy(state)

def apply_move(self, move):
    face = move[0]
    times = 1 if len(move) == 1 else 2  # e.g., 'F' vs 'F2'

    for _ in range(times):
        self._rotate(face)

def _rotate(self, face):
    adjacent = {
        'U': [('F', 0), ('R', 0), ('B', 0), ('L', 0)],
        'D': [('F', 2), ('L', 2), ('B', 2), ('R', 2)],
        'F': [('U', 2), ('R', 3), ('D', 0), ('L', 1)],
        'B': [('U', 0), ('L', 3), ('D', 2), ('R', 1)],
        'L': [('U', 3), ('F', 3), ('D', 3), ('B', 1)],
        'R': [('U', 1), ('B', 3), ('D', 1), ('F', 1)],
    }

    # Rotate the face itself
    self.state[face] = self._rotate_face_cw(self.state[face])

    # Rotate the surrounding stickers (simplified)
    cycle = adjacent[face]
    strips = [self._get_edge(f, pos) for f, pos in cycle]
    for i in range(4):
        f, pos = cycle[i]
        self._set_edge(f, pos, strips[(i - 1) % 4])

def _rotate_face_cw(self, face):
    return [face[i] for i in [6, 3, 0, 7, 4, 1, 8, 5, 2]]  # rotate 90° CW

def _get_edge(self, face, pos):
    s = self.state[face]
    if pos == 0: return s[0:3]     # top
    if pos == 1: return [s[i] for i in [2,5,8]]  # right
    if pos == 2: return s[6:9]     # bottom
    if pos == 3: return [s[i] for i in [0,3,6]]  # left

def _set_edge(self, face, pos, vals):
    s = self.state[face]
    if pos == 0: s[0:3] = vals
    if pos == 1: 
        for i, v in zip([2,5,8], vals): s[i] = v
    if pos == 2: s[6:9] = vals
    if pos == 3: 
        for i, v in zip([0,3,6], vals): s[i] = v

def is_g1(self):
    # Check if all edges are oriented
    for (pos1, pos2) in EDGE_POSITIONS:
        c1 = self.state[pos1[0]][pos1[1]]
        c2 = self.state[pos2[0]][pos2[1]]
        if not self._is_edge_oriented(c1, c2):
            return False
    return True

def is_g2(self):
    # G2 requires G1 + corners oriented
    return self.is_g1() and self._are_corners_oriented()

def is_g3(self):
    # G3 requires G2 + parity (simplified)
    return self.is_g2() and self._parity_ok()

def _is_edge_oriented(self, c1, c2):
    # Simplified: assume white/yellow are U/D and always correct
    return c1 in ['W', 'Y'] or c2 in ['W', 'Y']

def _are_corners_oriented(self):
    # Placeholder: assume all are oriented
    return True

def _parity_ok(self):
    # Placeholder: assume parity correct
    return True


    def is_solved(self):
        return all(len(set(face)) == 1 for face in self.state.values())

    def copy(self):
        return Cube(copy.deepcopy(self.state))