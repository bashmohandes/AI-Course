import sys
from collections import deque


class Board:
    def __init__(self, board=None, l=None, e=None, move=None, parent=None):
        if board is not None:
            parts = board.split(',')
            b = []
            for i in range(3):
                b.append([])
                for j in range(3):
                    b[i].append(int(parts[i * 3 + j]))
                    if b[i][j] == 0:
                        self.empty = (i, j)
            self.board = b
        elif l is not None:
            self.board = l
            self.empty = e

        self.hash = self.calculate_hash()
        self.move = move
        self.parent = parent

    def __repr__(self):
        return '\n'.join([str(self.board[i]) for i in range(len(self.board))])

    def __eq__(self, other):
        return self.hash == other.hash

    def __hash__(self):
        return self.hash

    def calculate_hash(self):
        temp = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                temp *= 10
                temp += self.board[i][j]
        return temp

    def actions(self):
        a = []
        if self.empty[0] > 0:
            t = [row[:] for row in self.board]
            e = (self.empty[0] - 1, self.empty[1])
            Board._swap(t, e, self.empty)
            a.append(Board(None, t, e, 'Up', self))

        if self.empty[0] < len(self.board) - 1:
            t = [row[:] for row in self.board]
            e = (self.empty[0] + 1, self.empty[1])
            Board._swap(t, e, self.empty)
            a.append(Board(None, t, e, 'Down', self))

        if self.empty[1] > 0:
            t = [row[:] for row in self.board]
            e = (self.empty[0], self.empty[1] - 1)
            Board._swap(t, e, self.empty)
            a.append(Board(None, t, e, 'Left', self))

        if self.empty[1] < len(self.board) - 1:
            t = [row[:] for row in self.board]
            e = (self.empty[0], self.empty[1] + 1)
            Board._swap(t, e, self.empty)
            a.append(Board(None, t, e, 'Right', self))

        return a

    def is_goal(self):
        return self == Board.GOAL

    @classmethod
    def _swap(cls, board, pos_1, pos_2):
        t = board[pos_1[0]][pos_1[1]]
        board[pos_1[0]][pos_1[1]] = board[pos_2[0]][pos_2[1]]
        board[pos_2[0]][pos_2[1]] = t


def calculate_path(board):
    path = []
    c = board

    while c.move:
        path.append(c.move)
        c = c.parent

    path.reverse()
    return path


def bfs(board):
    frontier = deque([board])
    visited = set()

    while frontier:
        n = frontier.pop()

        if n.is_goal():
            print calculate_path(n)
            return
        else:
            visited.add(n)

        possible_actions = n.actions()
        for ac in possible_actions:
            if ac in visited:
                continue
            if ac in frontier:
                continue
            else:
                frontier.appendleft(ac)


def dfs(board):
    frontier = [board]
    visited = set()

    while frontier:
        n = frontier.pop()
        # print n
        # print
        if n.is_goal():
            print calculate_path(n)
            return
        else:
            visited.add(n)

        possible_actions = n.actions()
        possible_actions.reverse()
        for ac in possible_actions:
            if ac in visited:
                continue
            if ac in frontier:
                continue
            else:
                frontier.append(ac)


def ast(board):
    pass


Board.GOAL = Board('0,1,2,3,4,5,6,7,8')

method_param = sys.argv[1]
board_param = sys.argv[2]

initial = Board(board_param)

if method_param == 'bfs':
    bfs(initial)
elif method_param == 'dfs':
    dfs(initial)
elif method_param == 'ast':
    ast(initial)
else:
    raise Exception("unsupported")
