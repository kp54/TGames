import random

from src.games.Mines import Mines
from src.config.Mines import Config


def main():
    random.seed()
    game = Mines(config=Config(mines=10), debug=True)

    while True:
        game.set_()

        while True:
            print(game, end='')
            tmp = (*map(lambda x: int(x, base=16), input('>> ').split(',')),)
            tmp = game.open_(tmp)
            if tmp[0] == 1:
                print('BOOM!')
                break

        tmp = game.plot()
        print(tmp[1], end='')

        while True:
            tmp = input('contine?: ')
            if tmp in ('yes', 'no'):
                break

        if tmp == 'no':
            break


if __name__ == '__main__':
    main()
