import random

from ..config.Mines import Config
from .GameBase import GameBase, EnumStatus, state


class Mines(GameBase):
    def __init__(self, config=Config(), debug=False, extra={}):
        super().__init__(config, debug, extra)
        self.count = 0

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

        for i in range(self.config.width):
            for j in range(self.config.height):
                if self.field[i][j] != 'm':
                    cnt = 0
                    for p in self._adjs((i, j)):
                        if self.field[p[0]][p[1]] == 'm':
                            cnt += 1
                    if cnt != 0:
                        self.field[i][j] = str(cnt)

        self.count = self.config.width * self.config.height - self.config.mines

        self.state = EnumStatus.ready

        return (0,)

    @state(EnumStatus.ready, EnumStatus.running, EnumStatus.stopped)
    def plot(self):
        tmp = '\\' + ''.join('{:X}'.format(i)for i in range(self.config.width)) + '\n'
        for j in range(self.config.height):
            tmp += '{:X}'.format(j)
            for i in range(self.config.width):
                tmp += self.view[i][j] or self.field[i][j]
                if self.state is EnumStatus.stopped:
                    if self.field[i][j] == 'm':
                        if self.view[i][j] == 'F':
                            tmp = tmp[:-1]+'x'
                        else:
                            tmp = tmp[:-1]+'m'
            tmp += '\n'

        self.logger.debug(self.dinfo())

        return (
            0,
            tmp)

    @state(EnumStatus.ready, EnumStatus.running)
    def open_(self, pos):
        if self.state is EnumStatus.ready:
            self.state = EnumStatus.running

        if self.view[pos[0]][pos[1]] is None:
            if self.field[pos[0]][pos[1]] not in ['.', 'm']:
                if int(self.field[pos[0]][pos[1]]) == sum(1 if self.view[p[0]][p[1]] == 'F' else 0 for p in self._adjs(pos)):
                    for p in self._adjs(pos):
                        if self.view[p[0]][p[1]] == '#':
                            tmp = self.open_(p)
                            if tmp[0] != 0:
                                return tmp
                else:
                    return (
                        -1,
                        'already opened')
        else:
            if self.view[pos[0]][pos[1]] == 'F':
                return (
                    -1,
                    'flagged')

            elif self.field[pos[0]][pos[1]] == 'm':
                self.state = EnumStatus.stopped

                return (
                    1,
                    'BOOM!')

            else:
                self.logger.debug('scanning:')
                queue = [pos]
                visited = []
                while queue:
                    tmp = queue.pop(0)
                    if str(tmp) in visited:
                        continue
                    self.logger.debug(tmp)
                    visited.append(str(tmp))
                    if self.view[tmp[0]][tmp[1]] is None or (self.view[tmp[0]][tmp[1]] == 'F' and self.field[tmp[0]][tmp[1]] == 'm'):
                            continue
                    self.view[tmp[0]][tmp[1]] = None
                    self.count -= 1
                    if self.field[tmp[0]][tmp[1]] == '.':
                        queue.extend(self._adjs(tmp))

        if self.count == 0:
            self.state = EnumStatus.stopped
            return (
                2,
                'game cleard!')
        else:
            return (0,)

    @state(EnumStatus.running)
    def flag(self, pos):
        if self.view[pos[0]][pos[1]] not in ['#', 'F']:
            return (
                -1,
                'not flaggable')
        if self.view[pos[0]][pos[1]] == '#':
            self.view[pos[0]][pos[1]] = 'F'
        else:
            self.view[pos[0]][pos[1]] = '#'
        return (0,)

    def dinfo(self):
        return 'config: {{{}}}\nstate: {}\n{}'.format(
            str(self.config)[:-1].replace('\n', ', '),
            self.state.name,
            self.dplot()
        )

    def dplot(self):
        tmp = 'field:\n'
        tmp += '\\' + ''.join('{:X}'.format(i)for i in range(self.config.width)) + '\n'
        for j in range(self.config.height):
            tmp += '{:X}'.format(j)
            for i in range(self.config.width):
                tmp += self.field[i][j]
            tmp += '\n'
        tmp += 'view:\n'
        tmp += '\\' + ''.join('{:X}'.format(i)for i in range(self.config.width)) + '\n'
        for j in range(self.config.height):
            tmp += '{:X}'.format(j)
            for i in range(self.config.width):
                tmp += self.view[i][j] or ' '
            tmp += '\n'

        return tmp
