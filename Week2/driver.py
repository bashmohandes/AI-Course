import sys
from collections import deque
from heapq import heapify, heappush, heappop


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

    def calculate_path(self):
        path = []
        c = self

        while c.move:
            path.append(c.move)
            c = c.parent

        path.reverse()
        return path


class Frontier:
    def __init__(self):
        self.data = deque()
        self.index = {}

    def push(self, c):
        self.data.append(c)
        self.index[c] = len(self.data) - 1

    def pop(self):
        r = self.data.pop()
        self.index.pop(r)
        return r

    def dequeue(self):
        r = self.data.popleft()
        self.index.pop(r)
        return r

    def __contains__(self, item):
        return item in self.index

    def __sizeof__(self):
        return len(self.data)


class Solver:
    def __init__(self, root, frontier):
        self.root = root
        self.frontier = frontier
        self.visited = set()
        self.add(root)

    def solve(self):
        while self.frontier:
            n = self.remove()

            if n.is_goal():
                print n.calculate_path()
                return
            else:
                self.visited.add(n)

            possible_actions = n.actions()
            for ac in self.post_expand(possible_actions):
                if ac in self.visited:
                    continue
                if ac in self.frontier:
                    continue
                else:
                    self.add(ac)

    def add(self, ac):
        raise NotImplementedError()

    def remove(self):
        raise NotImplementedError()

    def post_expand(self, nodes):
        return nodes


class DfsSolver(Solver):
    def __init__(self, root):
        Solver.__init__(self, root, Frontier())

    def add(self, ac):
        self.frontier.push(ac)

    def remove(self):
        return self.frontier.pop()

    def post_expand(self, nodes):
        return reversed(nodes)


class BfsSolver(Solver):
    def __init__(self, root):
        Solver.__init__(self, root, Frontier())

    def add(self, ac):
        self.frontier.push(ac)

    def remove(self):
        return self.frontier.dequeue()


class AStarSolver(Solver):
    def __init__(self, root):
        Solver.__init__(self, root, Frontier())

    def add(self, ac):
        heappush(self.frontier, ac)

    def remove(self):
        return heappop(self.frontier)


Board.GOAL = Board('0,1,2,3,4,5,6,7,8')

method_param = sys.argv[1]
board_param = sys.argv[2]

initial = Board(board_param)
solver = None
if method_param == 'bfs':
    solver = BfsSolver(initial)
elif method_param == 'dfs':
    solver = DfsSolver(initial)
elif method_param == 'ast':
    solver = AStarSolver(initial)
else:
    raise Exception("unsupported")

solver.solve()
