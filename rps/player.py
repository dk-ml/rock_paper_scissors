from random import sample
from collections import Counter

from sklearn.linear_model import LogisticRegression

from rps.game import Move


class Player:
    def __init__(self):
        self.game_history = None

    def __repr__(self):
        return f'{self.__class__.__name__}()'

    def update(self, game_history):
        self.game_history = game_history

    def get_move(self):
        raise NotImplementedError()


class RockPlayer(Player):
    def get_move(self):
        return Move.ROCK


class PaperPlayer(Player):
    def get_move(self):
        return Move.PAPER


class ScissorsPlayer(Player):
    def get_move(self):
        return Move.SCISSORS


class RandomPlayer(Player):
    MOVES = [Move.SCISSORS, Move.ROCK, Move.PAPER]

    def get_move(cls):
        return sample(population=cls.MOVES, k=1)[0]


class AIPlayer(Player):
    MOVE_BY_NUM = {0: Move.PAPER, 1: Move.SCISSORS, 2: Move.ROCK}
    NUM_BY_MOVE = {v: k for k, v in MOVE_BY_NUM.items()}
    WINDOW_SIZE = 10

    def get_move(self):
        X, y = self._get_Xy()
        if not X or len(set(y)) == 1:
            return RandomPlayer().get_move()
        model = LogisticRegression(solver='liblinear', multi_class='auto')
        model.fit(X=X, y=y)
        X_pred = self._get_X_pred()
        opponent_next_move = self.MOVE_BY_NUM[model.predict(X=X_pred)[0]]

        return {
            Move.ROCK: Move.PAPER,
            Move.PAPER: Move.SCISSORS,
            Move.SCISSORS: Move.ROCK,
        }[opponent_next_move]

    def _get_Xy(self):
        opponent_moves = [m for _, m in self.game_history]
        X = []
        y = []
        for i in range(len(opponent_moves) - self.WINDOW_SIZE - 1):
            target = self.NUM_BY_MOVE[opponent_moves[i + self.WINDOW_SIZE]]
            y.append(target)
            sub_history = opponent_moves[i : i + self.WINDOW_SIZE]
            features = self._get_features(history=sub_history)
            X.append(features)
        return X, y

    def _get_X_pred(self):
        opponent_moves = [m for _, m in self.game_history]
        sub_history = opponent_moves[-self.WINDOW_SIZE:]
        features = self._get_features(history=sub_history)
        return [features]

    def _get_features(self, history):
        counter = Counter(history)
        prop_rocks = counter[Move.ROCK] / len(history)
        prop_scissors = counter[Move.SCISSORS] / len(history)
        prop_papers = counter[Move.PAPER] / len(history)
        return [prop_rocks, prop_scissors, prop_papers]