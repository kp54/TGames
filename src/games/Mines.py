import random
import enum
import functools


class Config(enum.Enum):
    width = 16
    height = 8
    mines = 20


class Mines():
    def __init__(self, ex={}):
        self.state = 'initialized'
        self.debug = False

        for k, v in ex.items():
            setattr(self, k, v)

    def _adjs(self, pos):
        directions = [
            [1, 0],
            [1, -1],
            [0, -1],
            [-1, -1],
            [-1, 0],
            [-1, 1],
            [0, 1],
            [1, 1]
        ]

        tmp = []
        for d in directions:
            cur = [pos[0]+d[0], pos[1]+d[1]]
            if cur[0] in range(Config.width.value) and cur[1] in range(Config.height.value):
                tmp.append(cur)

        return tmp

    def _state(status):
        def _state_(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                if self.state in status:
                    return func(self, *args, **kwargs)
                else:
                    return (
                        -1,
                        'sequence error')

            return wrapper
        return _state_

    @_state(['initialized', 'finished'])
    def set_(self):
        self.field = [
            ['.' for i in range(Config.height.value)]
            for i in range(Config.width.value)]
        self.view = [
            ['#' for i in range(Config.height.value)]
            for i in range(Config.width.value)]

        cnt = Config.mines.value
        while cnt != 0:
            x = random.randint(0, Config.width.value - 1)
            y = random.randint(0, Config.height.value - 1)
            if self.field[x][y] == '.':
                self.field[x][y] = 'm'
                cnt -= 1

        self.state = 'setted'

        return (0,)

    @_state(['setted', 'running', 'finished'])
    def plot(self):
        tmp = '\\' + ''.join(
                ['{:X}'.format(i)for i in range(Config.width.value)]
            ) + '\n'
        for j in range(0, Config.height.value):
            tmp += '{:X}'.format(j)
            for i in range(0, Config.width.value):
                tmp += self.view[i][j]
                if self.state == 'finished':
                    if self.field[i][j] == 'm':
                        if self.view[i][j] == 'f':
                            tmp = tmp[:-1] + 'x'
                        else:
                            tmp = tmp[:-1] + 'm'
            tmp += '\n'

        return (
            0,
            tmp)

    @_state(['setted', 'running'])
    def open_(self, pos):
        if self.state == 'setted':
            self.state = 'running'

        if self.view[pos[0]][pos[1]] != '#':
            return (
                -2,
                'already opened')

        elif self.field[pos[0]][pos[1]] == 'm':
            self.state = 'finished'

            return (
                1,
                'BOOM!')

        else:
            self._open_(pos)
            return (0,)

    def _open_(self, pos):
        if self.view[pos[0]][pos[1]] != '#':
            return

        if self.debug:
            print(pos)

        cnt = 0
        tmp = self._adjs(pos)
        for i in tmp:
            if self.field[i[0]][i[1]] == 'm':
                cnt += 1

        if cnt != 0:
            self.view[pos[0]][pos[1]] = str(cnt)
        else:
            self.view[pos[0]][pos[1]] = '.'
            for i in tmp:
                self._open_(i)


def main():
    random.seed()
    game = Mines()
    while True:
        game.set_()

        while True:
            tmp = game.plot()
            print(tmp[1], end='')
            tmp = list(map(int, input('>> ').split(',')))
            tmp = game.open_(tmp)
            if tmp[0] == 1:
                print('BOOM!')
                break

        tmp = game.plot()
        print(tmp[1], end='')

        while True:
            tmp = input('contine?: ')
            if tmp in ['yes', 'no']:
                break

        if tmp == 'no':
            break


if __name__ == '__main__':
    main()
