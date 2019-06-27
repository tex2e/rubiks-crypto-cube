
import numpy as np

# Rubik's Cube
#   ____                  +---+
# |\  A  \                | A |
# | \ ____\  expand   +---+---+---+---+
# |B |    |  ======>  | B | C | D | E |
#  \ | C  |           +---+---+---+---+
#   \|____|               | F |
#                         +---+

# Rotation:
#   ____________                     ____________
#  |\            \                  |\            \
#  |A\            \                 |A\            \
#  | B\            \                | B\            \
#  |D C\____________\               |D C\____________\
#  | E |            |      Row      | E |            |
#  |G F|            |      ====>    |  F|            |
#   \H |            |                \  |            |
#    \I|            |                 \ |  G   H   I |
#     \|____________|                  \|____________|
#
#   ____________                     ____________
#  |\            \                  |\         C  \
#  | \            \                 | \         F  \
#  |  \            \                |  \         I  \
#  |   \____________\               |   \____________\
#  |   |            |      Column   |   |            |
#  |   |  A   B   C |      ====>    |   |  A   B     |
#   \  |  D   E   F |                \  |  D   E     |
#    \ |  G   H   I |                 \ |  G   H     |
#     \|____________|                  \|____________|
#
#   ____________                     ____________
#  |\   A  B  C  \                  |\            \
#  | \   D  E  F  \                 |C\   D  E  F  \
#  |  \   G  H  I  \                |  \   G  H  I  \
#  |   \____________\               |B  \____________\
#  |   |            |      Level    |   |            |
#  |   |            |      ====>    |A  |            |
#   \  |            |                \  |            |
#    \ |            |                 \ |            |
#     \|____________|                  \|____________|

class RubikCube:

    def __init__(self, size):
        self.size = size
        self.A = np.zeros((size,size), dtype=np.int8)
        self.B = np.zeros((size,size), dtype=np.int8)
        self.C = np.zeros((size,size), dtype=np.int8)
        self.D = np.zeros((size,size), dtype=np.int8)
        self.E = np.zeros((size,size), dtype=np.int8)
        self.F = np.zeros((size,size), dtype=np.int8)
        self.faces = [self.A, self.B, self.C, self.D, self.E, self.F]

    def __str__(self):
        current_printoptions = np.get_printoptions()
        np.set_printoptions(formatter={'int': '{: 3d}'.format})

        output = ""
        indent = " " * (1 + self.size * 4)
        for row in self.A:
            output += indent + str(row) + "\n"
        for zipped_row in zip(self.B, self.C, self.D, self.E):
            for row in zipped_row:
                output += str(row)
            output += "\n"
        for row in self.F:
            output += indent + str(row) + "\n"

        np.set_printoptions(current_printoptions)
        return output

    def init_arange(self):
        i = 0
        for face in self.faces:
            for y in range(self.size):
                for x in range(self.size):
                    face[y][x] = i
                    i += 1

    def encrypt(self, key):
        for move in key.split('-'):
            if move[0] == 'R':
                self.rotate_row(int(move[1]))
            if move[0] == 'C':
                self.rotate_column(int(move[1]))
            if move[0] == 'L':
                self.rotate_level(int(move[1]))

    # ex) R1
    #          *  *  *                                 *  *  *
    #          *  *  *                                 *  *  *
    #          *  *  *                                 *  *  *
    # *  *  *  *  *  *  *  *  *  *  *  *      *  *  *  *  *  *  *  *  *  *  *  *
    # *  *  *  *  *  *  *  *  *  *  *  * ==>  *  *  *  *  *  *  *  *  *  *  *  *
    # 1  2  3  4  5  6  7  8  9 10 11 12     10 11 12  1  2  3  4  5  6  7  8  9
    #         13 14 15                                19 16 13
    #         16 17 18                                20 17 14
    #         19 20 21                                21 18 15
    #
    def rotate_row(self, n):
        # B -> C -> D -> E -> B
        if n in (1, 2, 3):
            for i in range(n):
                tmpB = np.copy(self.B[-1])
                self.B[-1] = self.E[-1]
                self.E[-1] = self.D[-1]
                self.D[-1] = self.C[-1]
                self.C[-1] = tmpB
            # rotate F by -90*n
            self.F = np.rot90(self.F, 4 - n)
        elif n in (4, 5, 6):
            for i in range(n - 3):
                tmpB = np.copy(self.B[:-1])
                self.B[:-1] = self.E[:-1]
                self.E[:-1] = self.D[:-1]
                self.D[:-1] = self.C[:-1]
                self.C[:-1] = tmpB
            # rotate A by 90*n
            self.A = np.rot90(self.A, n - 3)

    # ex) C1
    #          *  *  1                                 *  *  4
    #          *  *  2                                 *  *  5
    #          *  *  3                                 *  *  6
    # *  *  *  *  *  4 13 14 15 12  *  *      *  *  *  *  *  7 19 16 13  3  *  *
    # *  *  *  *  *  5 16 17 18 11  *  * ==>  *  *  *  *  *  8 20 17 14  2  *  *
    # *  *  *  *  *  6 19 20 21 10  *  *      *  *  *  *  *  9 21 18 15  1  *  *
    #          *  *  7                                 *  * 10
    #          *  *  8                                 *  * 11
    #          *  *  9                                 *  * 12
    #
    def rotate_column(self, n):
        # A -> E -> F -> C -> A
        if n in (1, 2, 3):
            for i in range(n):
                tmpA = np.copy(self.A[:, -1])
                self.A[:, -1] = self.C[:, -1]
                self.C[:, -1] = self.F[:, -1]
                self.F[:, -1] = np.flip(self.E[:,  0])
                self.E[:,  0] = np.flip(tmpA)
            # rotate D by -90*n
            self.D = np.rot90(self.D, 4 - n)
        elif n in (4, 5, 6):
            for i in range(n - 3):
                tmpA = np.copy(self.A[:, :-1])
                self.A[:, :-1] = self.C[:, :-1]
                self.C[:, :-1] = self.F[:, :-1]
                self.F[:, :-1] = np.flip(self.E[:, 1:])
                self.E[:,  1:] = np.flip(tmpA)
            # rotate B by 90*n
            self.B = np.rot90(self.B, n - 3)

    # ex) L1
    #           1  2  3                                4  5  6
    #           *  *  *                                *  *  *
    #           *  *  *                                *  *  *
    # 12  *  *  *  *  *  *  *  4 13 14 15     3  *  *  *  *  *  *  *  7 19 16 13
    # 11  *  *  *  *  *  *  *  5 16 17 18 ==> 2  *  *  *  *  *  *  *  8 20 17 14
    # 10  *  *  *  *  *  *  *  6 19 20 21     1  *  *  *  *  *  *  *  9 21 18 15
    #           *  *  *                                *  *  *
    #           *  *  *                                *  *  *
    #           9  8  7                               12 11 10
    #
    def rotate_level(self, n):
        # A -> B -> F -> D -> A
        if n in (1, 2, 3):
            for i in range(n):
                tmpA = np.copy(self.A[0])
                self.A[0]     = self.D[:, -1]
                self.D[:, -1] = np.flip(self.F[-1])
                self.F[-1]    = self.B[:, 0]
                self.B[:,  0] = np.flip(tmpA)
            # rotate E by -90*n
            self.E = np.rot90(self.E, 4 - n)
        elif n in (4, 5, 6):
            for i in range(n - 3):
                tmpA = np.copy(self.A[1:])
                self.A[1:]     = np.rot90(self.D[:, :-1])
                self.D[:, :-1] = np.rot90(self.F[:-1])
                self.F[:-1]    = np.rot90(self.B[:, 1:])
                self.B[:,  1:] = np.rot90(tmpA)
            # rotate C by 90*n
            self.C = np.rot90(self.C, n - 3)


if __name__ == '__main__':

    rubikcube = RubikCube(size=3)
    rubikcube.init_arange()
    print(rubikcube)
    # rubikcube.rotate_level(2)
    # print(rubikcube)

    # Example)
    key = 'R3-L2-C4-L6-R5-C1-R3-L4-R1'
    rubikcube.encrypt(key)
    print(rubikcube)
