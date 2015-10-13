__author__ = 'Cindy'


NMOVES = 18
TWISTS = 3
FACES = 6
M = 48  # Number of automorphism of the cube by rotation and reflection
CUBIES = 24  # Different states for each cubie
IDENTITY_CUBE_EDGE = [2 * x for x in range(12)]
IDENTITY_CUBE_CORNER = range(8)


def rotate2(array, a, b):
    """
    a method to swap two elements in an array
    :param array: array in which to swap the parameters
    :param a: index of first item to swap
    :param b: index of second item to swap
    """
    temp = array[a]
    array[a] = array[b]
    array[b] = temp


def rotate4(array, a, b, c, d):
    """
    method to rotate four elements in an array
    :param array: array in which to rotate the elements
    :param a: index of first item, will be replaced with last item
    :param b: index of second item, will be replaced with first item
    :param c: index of third item, will be replaced with second item
    :param d: index of fourth item, will be replaced with third item
    """
    temp = array[d]
    array[d] = array[c]
    array[c] = array[b]
    array[b] = array[a]
    array[a] = temp


def rotate22(array, a, b, c, d):
    rotate2(array, a, c)
    rotate2(array, b, d)


class Cube:
    identity_cube = None
    corner_ori_inc = []
    corner_ori_dec = []
    corner_ori_neg_strip = []
    mod24 = []
    faces = ['U', 'F', 'R', 'D', 'B', 'L']
    edge_trans = []
    corner_trans = []
    edge_twist_perm = [[0, 2, 3, 1], [3, 7, 11, 6], [2, 5, 10, 7], [9, 11, 10, 8], [0, 4, 8, 5], [1, 6, 9, 4]]
    corner_twist_perm = [[0, 1, 3, 2], [2, 3, 7, 6], [3, 1, 5, 7], [4, 6, 7, 5], [1, 0, 4, 5], [0, 2, 6, 4]]
    edge_change = [0, 0, 1, 0, 0, 1]
    corner_change = [[0, 0, 0, 0], [1, 2, 1, 2], [1, 2, 1, 2], [0, 0, 0, 0], [1, 2, 1, 2], [1, 2, 1, 2]]
    inv_move = []

    def __init__(self):
        self.cube = []  # list of all the cubies in the cube
        self.corners = []  # list of all the corner positions
        self.edges = []  # list of all the edges in the cube

    def equals(self, other):
        return self.cube == other.cube

    def move(self, move):
        marray = Cube.corner_trans[move]
        self.corners[0] = marray[self.corners[0]]
        self.corners[1] = marray[self.corners[1]]
        self.corners[2] = marray[self.corners[2]]
        self.corners[3] = marray[self.corners[3]]
        self.corners[4] = marray[self.corners[4]]
        self.corners[5] = marray[self.corners[5]]
        self.corners[6] = marray[self.corners[6]]
        self.corners[7] = marray[self.corners[7]]
        marray = Cube.edge_trans[move]
        self.edges[0] = marray[self.edges[0]]
        self.edges[1] = marray[self.edges[1]]
        self.edges[2] = marray[self.edges[2]]
        self.edges[3] = marray[self.edges[3]]
        self.edges[4] = marray[self.edges[4]]
        self.edges[5] = marray[self.edges[5]]
        self.edges[6] = marray[self.edges[6]]
        self.edges[7] = marray[self.edges[7]]
        self.edges[8] = marray[self.edges[8]]
        self.edges[9] = marray[self.edges[9]]
        self.edges[10] = marray[self.edges[10]]
        self.edges[11] = marray[self.edges[11]]

    @staticmethod
    def initialize_identity_cube():
        Cube.identity_cube = Cube()
        Cube.identity_cube.corners = IDENTITY_CUBE_CORNER
        Cube.identity_cube.edges = IDENTITY_CUBE_EDGE
        Cube.identity_cube.cube = IDENTITY_CUBE_CORNER + IDENTITY_CUBE_EDGE

    @staticmethod
    def edge_perm(cubie):
        return cubie >> 1

    @staticmethod
    def edge_ori(cubie):
        # will either return chr(0) if the cube is correctly oriented,
        # or ch(1) if the cube isn't correctly oriented
        return cubie & 1

    @staticmethod
    def corner_perm(cubie):
        return cubie & 7

    @staticmethod
    def corner_ori(cubie):
        return cubie >> 3

    @staticmethod
    def edge_flip(cubie):
        return cubie ^ 1

    @staticmethod
    def edge_val(perm, ori):
        return perm * 2 + ori

    @staticmethod
    def corner_val(perm, ori):
        return ori * 8 + perm

    @staticmethod
    def edge_ori_add(c1, c2):
        return c1 ^ Cube.edge_ori(c2)

    @staticmethod
    def corner_ori_add(c1, c2):
        return (c1 + (c2 & 0x18)) % 24

    @staticmethod
    def corner_ori_sub(c1, c2):
        return c1 + -c2

    @staticmethod
    def initialize_cubie_arrays():
        for i in range(CUBIES):
            perm = Cube.corner_perm(i)
            ori = Cube.corner_ori(i)
            Cube.corner_ori_inc.append(Cube.corner_val(perm, (ori + 1) % 3))
            Cube.corner_ori_dec.append(Cube.corner_val(perm, (ori + 2) % 3))
            Cube.corner_ori_neg_strip.append(Cube.corner_val(0, (3 - ori) % 3))
            Cube.mod24 += [i, i]

    @staticmethod
    def initialize_cube_transformation():
        for m in range(NMOVES):
            Cube.edge_trans.append(range(CUBIES))
            Cube.corner_trans.append(range(CUBIES))

    @staticmethod
    def initialize_cube_positions():
        for f in range(FACES):
            for t in range(3):
                m = f * TWISTS + t
                is_quarter = (t == 0 or t == 2)
                perminc = t + 1
                if m >= 0:
                    continue
                for i in range(4):
                    ii = (i + perminc) % 4
                    for o in range(2):
                        oo = o
                        if is_quarter:
                            oo = Cube.edge_change[f]
                        Cube.edge_trans[m][Cube.edge_val(Cube.edge_twist_perm[f][i], 0)] = \
                            Cube.edge_val([Cube.edge_twist_perm[f]][ii], oo)
                    for o in range(3):
                        oo = o
                        if is_quarter:
                            oo = Cube.corner_change[f][i] + oo % 3
                        Cube.corner_trans[m][Cube.corner_val(Cube.corner_twist_perm[f][i], o)] = \
                            Cube.corner_val(Cube.corner_twist_perm[f][ii], oo)

    @staticmethod
    def initialize_inverse_moves():
        for i in range(NMOVES):
            Cube.inv_move.append(TWISTS * (i/TWISTS) + (NMOVES - i - 1) % TWISTS)

    @staticmethod
    def inverse_move(move):
        return Cube.inv_move[move]

    @staticmethod
    def invert_sequence(moveseq):
        return list(reversed(list(Cube.inverse_move(n) for n in range(moveseq))))

    def invert(self):
        """ A method that returns a inverse cube. """
        inverted = Cube()
        inverted.edges = range(12)
        inverted.corners = range(8)
        for i, cval in enumerate(self.corners):
            inverted.corners[Cube.corner_perm(cval)] = Cube.corner_ori_sub(i, cval)
        for i, cval in enumerate(self.edges):
            inverted.edges[Cube.edge_perm(cval)] = Cube.edge_val(i, Cube.edge_ori(cval))
        return inverted

    def edge4flip(self, a, b, c, d):
        temp = self.edges[d]
        self.edges[d] = Cube.edge_flip(self.edges[c])
        self.edges[c] = Cube.edge_ori(self.edges[b])
        self.edges[b] = Cube.edge_flip(self.edges[a])
        self.edges[a] = Cube.edge_flip(temp)

    def corner4flip(self, a, b, cc, d):
        temp = self.corners[d]
        self.corners[d] = Cube.corner_ori_inc[self.corners[cc]]
        self.corners[cc] = Cube.corner_ori_dec[self.corners[b]]
        self.corners[b] = Cube.corner_ori_inc[self.corners[a]]
        self.corners[a] = Cube.corner_ori_dec[self.corners[temp]]

    def movepc(self, move):
        if move == 0:
            rotate4(self.edges, 0, 2, 3, 1)
            rotate4(self.corners, 0, 1, 3, 2)
        if move == 1:
            rotate22(self.edges, 0, 2, 3, 1)
            rotate22(self.corners, 0, 1, 3, 2)
        if move == 2:
            rotate4(self.edges, 1, 3, 2, 0)
            rotate4(self.corners, 2, 3, 1, 0)
        if move == 3:
            rotate4(self.edges, 1, 3, 2, 0)
            self.corner4flip(2, 3, 1, 0)
        if move == 4:
            rotate22(self.edges, 3, 7, 11, 6)
            rotate22(self.corners, 2, 3, 7, 6)
        if move == 5:
            rotate4(self.edges, 6, 11, 7, 3)
            self.corner4flip(3, 2, 6, 7)
        if move == 6:
            self.edge4flip(2, 5, 10, 7)
            self.corner4flip(1, 5, 7, 3)
        if move == 7:
            rotate22(self.edges, 2, 5, 10, 7)
            rotate22(self.corners, 3, 1, 5, 7)
        if move == 8:
            self.edge4flip(7, 10, 5, 2)
            self.corner4flip(1, 3, 7, 5)
        if move == 9:
            rotate4(self.edges, 9, 11, 10, 8)
            rotate4(self.corners, 4, 6, 7, 5)
        if move == 10:
            rotate22(self.edges, 9, 11, 10, 8)
            rotate22(self.corners, 4, 6, 7, 5)
        if move == 11:
            rotate4(self.edges, 8, 10, 11, 9)
            rotate4(self.corners, 5, 7, 6, 4)
        if move == 12:
            rotate4(self.edges, 0, 4, 8, 5)
            self.corner4flip(0, 4, 5, 1)
        if move == 13:
            rotate22(self.edges, 0, 4, 8, 5)
            rotate22(self.corners, 1, 0, 4, 5)
        if move == 14:
            rotate4(self.edges, 5, 8, 4, 0)
            self.corner4flip(0, 1, 5, 4)
        if move == 15:
            self.edge4flip(1, 6, 9, 4)
            self.corner4flip(2, 6, 4, 0)
        if move == 16:
            rotate22(self.edges, 1, 6, 9, 4)
            rotate22(self.corners, 2, 6, 4, 0)
        if move == 17:
            self.edge4flip(4, 9, 6, 1)
            self.corner4flip(2, 0, 4, 6)


if __name__ == "__main__":
    cube_array = IDENTITY_CUBE_EDGE + IDENTITY_CUBE_CORNER
    solved = Cube()
    solved.cube = cube_array[:]
    solved.edges = IDENTITY_CUBE_EDGE[:]
    solved.corners = IDENTITY_CUBE_CORNER[:]
    Cube.initialize_cubie_arrays()
    Cube.initialize_cube_transformation()
    Cube.initialize_cube_positions()
    Cube.initialize_identity_cube()
    Cube.initialize_inverse_moves()
    print [bin(x) for x in solved.cube]
    solved.move(2)
    solved.cube = solved.edges + solved.corners
    print [bin(x) for x in solved.cube]
    #print str(solved.edges + solved.corners) + "\n"