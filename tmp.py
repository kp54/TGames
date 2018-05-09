import random

import src.util as util
from src.games.Mines import Mines
from src.config.Mines import Config


def main():
    random.seed()
    game = Mines(config=Config(mines=10), debug=True)

    while True:
        game.set_()

        while True:
            print(game.plot()[1], end='')
            c, *tmp = input('>> ').split(',')
            tmp = (*map(lambda x: int(x, base=16), tmp),)
            if c == 'o':
                tmp = game.open_(tmp)
            elif c == 'f':
                tmp = game.flag(tmp)
            if tmp[0] != 0:
                print(tmp[1])
                if 0 < tmp[0]:
                    break
        print(game.plot()[1], end='')

        if not util.yn('continue?: '):
            break


if __name__ == '__main__':
    import sys

    sys.exit(main())
