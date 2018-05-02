import random
import enum
import functools


def clamp(value, min_, max_):
    return sorted(min_, value, max_)[1]


class enumStatus(enum.Enum):
    initialized = enum.auto()
    setted = enum.auto()
    running = enum.auto()
    finished = enum.auto()


class Config():
    def __init__(self, width=16, height=8, mines=15, extra={}):
        self.width = clamp(width, 0, 15)
        self.height = clamp(height, 0, 15)
        self.mines = clamp(mines, 0, int(self.width*self.height*0.9))

        for k, v in extra.items():
            setattr(self, k, v)

    def __str__(self):
        return 'width: {}\nheight: {}\nmines: {}\n'.format(self.width, self.height, self.mines)


class Mines():
    def __init__(self, config=Config(), debug=False, extra={}):
        self.state = enumStatus.initialized
        self.debug = debug
        self.config = config

        for k, v in extra.items():
            setattr(self, k, v)

    def _adjs(self, pos):
        directions = (
            (1, 0),
            (1, -1),
            (0, -1),
            (-1, -1),
            (-1, 0),
            (-1, 1),
            (0, 1),
            (1, 1)
        )

        tmp = []
        for d in directions:
            cur = (pos[0]+d[0], pos[1]+d[1])
            if cur[0] in range(self.config.width) and cur[1] in range(self.config.height):
                tmp.append(cur)

        return tmp

    def _state(*status):
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

    @_state(enumStatus.initialized, enumStatus.finished)
    def set_(self):
        self.field = [
            ['.' for i in range(self.config.height)]
            for i in range(self.config.width)]
        self.view = [
            ['#' for i in range(self.config.height)]
            for i in range(self.config.width)]

        cnt = self.config.mines
        while cnt != 0:
            x = random.randint(0, self.config.width - 1)
            y = random.randint(0, self.config.height - 1)
            if self.field[x][y] == '.':
                self.field[x][y] = 'm'
                cnt -= 1

        self.state = enumStatus.setted

        return (0,)

    @_state(enumStatus.setted, enumStatus.running, enumStatus.finished)
    def plot(self):
        tmp = '\\' + ''.join(
                ['{:X}'.format(i)for i in range(self.config.width)]
            ) + '\n'
        for j in range(self.config.height):
            tmp += '{:X}'.format(j)
            for i in range(self.config.width):
                tmp += self.view[i][j]
                if self.state is enumStatus.finished:
                    if self.field[i][j] == 'm':
                        if self.view[i][j] == 'f':
                            tmp = tmp[:-1] + 'x'
                        else:
                            tmp = tmp[:-1] + 'm'
            tmp += '\n'

        return (
            0,
            tmp)

    @_state(enumStatus.setted, enumStatus.running)
    def open_(self, pos):
        if self.state is enumStatus.setted:
            self.state = enumStatus.running

        if self.view[pos[0]][pos[1]] != '#':
            return (
                -2,
                'already opened')

        elif self.field[pos[0]][pos[1]] == 'm':
            self.state = enumStatus.finished

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

    @_state(enumStatus.initialized, enumStatus.setted, enumStatus.running, enumStatus.finished)
    def dinfo(self):
        return 'config: {{{}}}\nstate: {}\n'.format(
            str(self.config)[:-1].replace('\n', ', '),
            self.state.name
        )

    def __str__(self):
        if self.debug:
            return self.plot()[1] + self.dinfo()
        else:
            return self.plot()[1]


def main():
    random.seed()
    game = Mines(config=Config(mines=10), debug=True)

    while True:
        game.set_()

        while True:
            print(game)
            tmp = list(map(lambda x: int(x, base=16), input('>> ').split(',')))
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
