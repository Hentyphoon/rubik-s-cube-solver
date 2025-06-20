import copy
from math import factorial

class Cube:
    def __init__(self, up, down,left, right, front, back):
        self.up = up
        self.dwn = down
        self.lft = left
        self.rght = right
        self.frnt = front
        self.bck = back

    def apply_move(self, move):
        if isinstance(move, tuple):
            face, turns = move
        else:
            if move.endswith("2"):
                face, turns = move[0], 2
            else:
                face, turns = move[0], 1

        turns %= 4
        if turns == 0:
            return self  

        for _ in range(turns):

            for _ in range(turns):
                if face == 'F':
                    self.frnt[0], self.frnt[1], self.frnt[2], self.frnt[3], self.frnt[5], self.frnt[6], self.frnt[7], self.frnt[8] = \
                    self.frnt[6], self.frnt[3], self.frnt[0], self.frnt[7], self.frnt[1], self.frnt[8], self.frnt[5], self.frnt[2]

                    self.up[6], self.up[7], self.up[8], self.rght[0], self.rght[3], self.rght[6], self.dwn[0], self.dwn[1], self.dwn[2], self.lft[2], self.lft[5], self.lft[8] = \
                    self.lft[8], self.lft[5], self.lft[2], self.up[6], self.up[7], self.up[8], self.rght[6], self.rght[3], self.rght[0], self.dwn[2], self.dwn[1], self.dwn[0]

                elif face == 'B':
                    self.bck[0], self.bck[1], self.bck[2], self.bck[3], self.bck[5], self.bck[6], self.bck[7], self.bck[8] = \
                    self.bck[6], self.bck[3], self.bck[0], self.bck[7], self.bck[1], self.bck[8], self.bck[5], self.bck[2]

                    self.up[0], self.up[1], self.up[2], self.lft[0], self.lft[3], self.lft[6], self.dwn[8], self.dwn[7], self.dwn[6], self.rght[2], self.rght[5], self.rght[8] = \
                    self.rght[2], self.rght[5], self.rght[8], self.up[2], self.up[1], self.up[0], self.lft[6], self.lft[3], self.lft[0], self.dwn[6], self.dwn[7], self.dwn[8]

                elif face == 'U':
                    self.up[0], self.up[1], self.up[2], self.up[3], self.up[5], self.up[6], self.up[7], self.up[8] = \
                    self.up[6], self.up[3], self.up[0], self.up[7], self.up[1], self.up[8], self.up[5], self.up[2]

                    self.frnt[0], self.frnt[1], self.frnt[2], self.rght[0], self.rght[1], self.rght[2], self.bck[0], self.bck[1], self.bck[2], self.lft[0], self.lft[1], self.lft[2] = \
                    self.rght[0], self.rght[1], self.rght[2], self.bck[0], self.bck[1], self.bck[2], self.lft[0], self.lft[1], self.lft[2], self.frnt[0], self.frnt[1], self.frnt[2]

                elif face == 'D':
                    self.dwn[0], self.dwn[1], self.dwn[2], self.dwn[3], self.dwn[5], self.dwn[6], self.dwn[7], self.dwn[8] = \
                    self.dwn[6], self.dwn[3], self.dwn[0], self.dwn[7], self.dwn[1], self.dwn[8], self.dwn[5], self.dwn[2]

                    self.frnt[6], self.frnt[7], self.frnt[8], self.lft[6], self.lft[7], self.lft[8], self.bck[6], self.bck[7], self.bck[8], self.rght[6], self.rght[7], self.rght[8] = \
                    self.lft[6], self.lft[7], self.lft[8], self.bck[6], self.bck[7], self.bck[8], self.rght[6], self.rght[7], self.rght[8], self.frnt[6], self.frnt[7], self.frnt[8]

                elif face == 'L':
                    self.lft[0], self.lft[1], self.lft[2], self.lft[3], self.lft[5], self.lft[6], self.lft[7], self.lft[8] = \
                    self.lft[6], self.lft[3], self.lft[0], self.lft[7], self.lft[1], self.lft[8], self.lft[5], self.lft[2]

                    self.up[0], self.up[3], self.up[6], self.frnt[0], self.frnt[3], self.frnt[6], self.dwn[0], self.dwn[3], self.dwn[6], self.bck[8], self.bck[5], self.bck[2] = \
                    self.bck[8], self.bck[5], self.bck[2], self.up[0], self.up[3], self.up[6], self.frnt[0], self.frnt[3], self.frnt[6], self.dwn[0], self.dwn[3], self.dwn[6]

                elif face == 'R':
                    self.rght[0], self.rght[1], self.rght[2], self.rght[3], self.rght[5], self.rght[6], self.rght[7], self.rght[8] = \
                    self.rght[6], self.rght[3], self.rght[0], self.rght[7], self.rght[1], self.rght[8], self.rght[5], self.rght[2]

                    self.up[2], self.up[5], self.up[8], self.bck[6], self.bck[3], self.bck[0], self.dwn[2], self.dwn[5], self.dwn[8], self.frnt[2], self.frnt[5], self.frnt[8] = \
                    self.frnt[2], self.frnt[5], self.frnt[8], self.up[2], self.up[5], self.up[8], self.bck[6], self.bck[3], self.bck[0], self.dwn[2], self.dwn[5], self.dwn[8]

            self.moves_made.append((face, turns))
        return self

    def get_sticker(self, face, idx):
        face_map = {
            'T': self.up,
            'D': self.dwn,
            'F': self.frnt,
            'B': self.bck,
            'L': self.lft,
            'R': self.rght
        }
        return face_map[face][idx]

    def is_g1(self):
        centers = {
            'T': self.up[4],
            'D': self.dwn[4],
            'F': self.frnt[4],
            'B': self.bck[4],
            'L': self.lft[4],
            'R': self.rght[4]
        }

        edges = [
            ('T', 1, 'B', 7),
            ('T', 5, 'R', 1),
            ('T', 3, 'L', 1),
            ('D', 7, 'B', 1),
            ('D', 5, 'R', 7),
            ('D', 3, 'L', 7),
            ('T', 7, 'F', 1),
            ('D', 1, 'F', 7),
            ('F', 5, 'R', 3),
            ('F', 3, 'L', 5),
            ('B', 3, 'R', 5),
            ('B', 5, 'L', 3)
        ]

        for f1, i1, f2, i2 in edges:
            c1 = self.get_sticker(f1, i1)
            c2 = self.get_sticker(f2, i2)

            if f1 in ['T', 'D']:
                if c1 != centers[f1]:
                    return False
            elif f2 in ['T', 'D']:
                if c2 != centers[f2]:
                    return False
            else:
                if c1 != centers[f1]:
                    return False

        return True

    def is_g2(self):
        return self.is_g1() and self._corners_oriented() and self._edges_in_slice()

    def is_g3(self):
        return self.is_g2() and self._parity_even() and self._pieces_in_slice()

    def is_solved(self):
        faces = ['t', 'dwn', 'frnt', 'bck', 'lft', 'rght']

        for face_name in faces:
            face = getattr(self, face_name)
            center_color = face[4]
            if any(sticker != center_color for sticker in face):
                return False
        return True

    def _corners_oriented(self):
        centers = {
            'up': self.up[4],
            'dwn': self.dwn[4],
            'frnt': self.frnt[4],
            'bck': self.bck[4],
            'lft': self.lft[4],
            'rght': self.rght[4]
        }

        corners = [
            ('up', 8),
            ('up', 2),
            ('up', 0),
            ('up', 6),
            ('dwn', 2),
            ('dwn', 8),
            ('dwn', 6),
            ('dwn', 0),
        ]

        for face, idx in corners:
            if getattr(self, face)[idx] != centers[face]:
                return False
        return True
    
    def _edges_in_slice(self):
        centers = {
            'frnt': self.frnt[4],
            'bck': self.bck[4],
            'lft': self.lft[4],
            'rght': self.rght[4]
        }

        edges = [
            ('frnt', 5, 'rght', 3),
            ('frnt', 3, 'lft', 5),
            ('bck', 3, 'rght', 5),
            ('bck', 5, 'lft', 3)
        ]

        for f1, i1, f2, i2 in edges:
            c1 = getattr(self, f1)[i1]
            c2 = getattr(self, f2)[i2]
            if c1 != centers[f1] or c2 != centers[f2]:
                return False
        return True


    def _sorted_tuple(*args):
        return tuple(sorted(args))

    def _permutation_parity(perm):
        arr = list(perm)
        parity = 0
        for i in range(len(arr)):
            while arr[i] != i:
                j = arr[i]
                arr[i], arr[j] = arr[j], arr[i]
                parity ^= 1
        return parity == 0
    
    def _corner_pieces(self):
        corners_positions = [
            [('up', 8), ('frnt', 2), ('rght', 0)],
            [('up', 2), ('rght', 2), ('bck', 0)],
            [('up', 0), ('bck', 2), ('lft', 0)],
            [('up', 6), ('lft', 2), ('frnt', 0)],
            [('dwn', 2), ('frnt', 8), ('rght', 6)],
            [('dwn', 8), ('rght', 8), ('bck', 6)],
            [('dwn', 6), ('bck', 8), ('lft', 6)],
            [('dwn', 0), ('lft', 8), ('frnt', 6)],
        ]

        pieces = []
        for pos in corners_positions:
            stickers = [getattr(self, face)[idx] for face, idx in pos]
            pieces.append(self._sorted_tuple(*stickers))
        return pieces

    def _edge_pieces(self):
        edges_positions = [
            [('up', 1), ('bck', 7)],
            [('up', 5), ('rght', 1)],
            [('up', 3), ('lft', 1)],
            [('dwn', 7), ('bck', 1)],
            [('dwn', 5), ('rght', 7)],
            [('dwn', 3), ('lft', 7)],
            [('up', 7), ('frnt', 1)],
            [('dwn', 1), ('frnt', 7)],
            [('frnt', 5), ('rght', 3)],
            [('frnt', 3), ('lft', 5)],
            [('bck', 3), ('rght', 5)],
            [('bck', 5), ('lft', 3)],
        ]

        pieces = []
        for pos in edges_positions:
            stickers = [getattr(self, face)[idx] for face, idx in pos]
            pieces.append(self._sorted_tuple(*stickers))
        return pieces

    def _parity_even(self):
        solved_corners = sorted([
            ('W', 'R', 'B'),
            ('W', 'B', 'O'),
            ('W', 'O', 'G'),
            ('W', 'G', 'R'),
            ('Y', 'R', 'G'),
            ('Y', 'G', 'O'),
            ('Y', 'O', 'B'),
            ('Y', 'B', 'R'),
        ])
        solved_edges = sorted([
            ('W', 'B'),
            ('W', 'R'),
            ('W', 'O'),
            ('Y', 'B'),
            ('Y', 'R'),
            ('Y', 'O'),
            ('W', 'G'),
            ('Y', 'G'),
            ('R', 'G'),
            ('G', 'O'),
            ('B', 'R'),
            ('B', 'O'),
        ])

        current_corners = self._corner_pieces()
        current_edges = self._edge_pieces()

        corner_indices = [solved_corners.index(c) for c in current_corners]
        edge_indices = [solved_edges.index(e) for e in current_edges]

        corner_parity = self._permutation_parity(corner_indices)
        edge_parity = self._permutation_parity(edge_indices)

        return corner_parity == edge_parity

    def _pieces_in_slice(self):
        centers = {
            'up': self.up[4],
            'dwn': self.dwn[4],
            'frnt': self.frnt[4],
            'bck': self.bck[4],
            'lft': self.lft[4],
            'rght': self.rght[4]
        }

        edges_U_D = {
            self._sorted_tuple(centers['up'], centers['bck']),
            self._sorted_tuple(centers['up'], centers['rght']),
            self._sorted_tuple(centers['up'], centers['lft']),
            self._sorted_tuple(centers['dwn'], centers['bck']),
            self._sorted_tuple(centers['dwn'], centers['rght']),
            self._sorted_tuple(centers['dwn'], centers['lft']),
            self._sorted_tuple(centers['up'], centers['frnt']),
            self._sorted_tuple(centers['dwn'], centers['frnt'])
        }

        edges_M = {
            self._sorted_tuple(centers['frnt'], centers['rght']),
            self._sorted_tuple(centers['frnt'], centers['lft']),
            self._sorted_tuple(centers['bck'], centers['rght']),
            self._sorted_tuple(centers['bck'], centers['lft'])
        }

        corners_U = {
            self._sorted_tuple(centers['up'], centers['frnt'], centers['rght']),
            self._sorted_tuple(centers['up'], centers['rght'], centers['bck']),
            self._sorted_tuple(centers['up'], centers['bck'], centers['lft']),
            self._sorted_tuple(centers['up'], centers['lft'], centers['frnt'])
        }

        corners_D = {
            self._sorted_tuple(centers['dwn'], centers['frnt'], centers['rght']),
            self._sorted_tuple(centers['dwn'], centers['rght'], centers['bck']),
            self._sorted_tuple(centers['dwn'], centers['bck'], centers['lft']),
            self._sorted_tuple(centers['dwn'], centers['lft'], centers['frnt'])
        }

        edges_positions = [
            ('up', 1, 'bck', 7),
            ('up', 5, 'rght', 1),
            ('up', 3, 'lft', 1),
            ('dwn', 7, 'bck', 1),
            ('dwn', 5, 'rght', 7),
            ('dwn', 3, 'lft', 7),
            ('up', 7, 'frnt', 1),
            ('dwn', 1, 'frnt', 7),
            ('frnt', 5, 'rght', 3),
            ('frnt', 3, 'lft', 5),
            ('bck', 3, 'rght', 5),
            ('bck', 5, 'lft', 3)
        ]

        corners_positions = [
            ('up', 8, 'frnt', 2, 'rght', 0),
            ('up', 2, 'rght', 2, 'bck', 0),
            ('up', 0, 'bck', 2, 'lft', 0),
            ('up', 6, 'lft', 2, 'frnt', 0),
            ('dwn', 2, 'frnt', 8, 'rght', 6),
            ('dwn', 8, 'rght', 8, 'bck', 6),
            ('dwn', 6, 'bck', 8, 'lft', 6),
            ('dwn', 0, 'lft', 8, 'frnt', 6)
        ]

        for f1, i1, f2, i2 in edges_positions:
            stickers = self._sorted_tuple(getattr(self, f1)[i1], getattr(self, f2)[i2])
            if f1 in ['up', 'dwn'] or f2 in ['up', 'dwn']:
                if stickers not in edges_U_D:
                    return False
            else:
                if stickers not in edges_M:
                    return False

        for f1, i1, f2, i2, f3, i3 in corners_positions:
            stickers = self._sorted_tuple(getattr(self, f1)[i1], getattr(self, f2)[i2], getattr(self, f3)[i3])
            if f1 == 'up':
                if stickers not in corners_U:
                    return False
            else:
                if stickers not in corners_D:
                    return False

        return True
