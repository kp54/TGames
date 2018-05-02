import random
import enum
import functools

from ..config.Mines import Config
from .GameBase import GameBase, EnumStatus, state


class Mines(GameBase):
    def __init__(self, config=Config(), debug=False, extra={}):
        super().__init__(config, debug, extra)

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

    @state(EnumStatus.stopped)
    def set_(self):
        self.field = [['.' for i in range(self.config.height)] for i in range(self.config.width)]
        self.view = [['#' for i in range(self.config.height)] for i in range(self.config.width)]

        cnt = self.config.mines
        while cnt != 0:
            x = random.randint(0, self.config.width - 1)
            y = random.randint(0, self.config.height - 1)
            if self.field[x][y] == '.':
                self.field[x][y] = 'm'
                cnt -= 1

        self.state = EnumStatus.ready

        return (0,)

    @state(EnumStatus.ready, EnumStatus.running, EnumStatus.stopped)
    def plot(self):
        tmp = '\\' + ''.join(
                ['{:X}'.format(i)for i in range(self.config.width)]
            ) + '\n'
        for j in range(self.config.height):
            tmp += '{:X}'.format(j)
            for i in range(self.config.width):
                tmp += self.view[i][j]
                if self.state is EnumStatus.stopped:
                    if self.field[i][j] == 'm':
                        if self.view[i][j] == 'f':
                            tmp = tmp[:-1] + 'x'
                        else:
                            tmp = tmp[:-1] + 'm'
            tmp += '\n'

        return (
            0,
            tmp)

    @state(EnumStatus.ready, EnumStatus.running)
    def open_(self, pos):
        if self.state is EnumStatus.ready:
            self.state = EnumStatus.running

        if self.view[pos[0]][pos[1]] != '#':
            return (
                -2,
                'already opened')

        elif self.field[pos[0]][pos[1]] == 'm':
            self.state = EnumStatus.stopped

            return (
                1,
                'BOOM!')

        else:
            if self.debug:
                print('scanning:')
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

    @state(EnumStatus.ready, EnumStatus.running, EnumStatus.stopped)
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
