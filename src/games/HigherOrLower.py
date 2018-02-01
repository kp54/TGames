import random
import enum

random.seed()


class Config(enum.Enum):
    range_ = [0, 8]
    selection = {
        'Higher': ['higher', 'h'],
        'Lower': ['lower', 'l']
    }


class Text(enum.Enum):
    class Normal(enum.Enum):
        pass

    class Shadow(enum.Enum):
        pass


class HigherOrLower():
    def __init__(self, ex={}):
        self.shadow = False
        self.cnt = 0
        self.ans = 4
        for k, v in ex.items():
            setattr(self, k, v)

    def generate(self):
        self.prev = self.ans
        self.ans = None
        while not self.ans:
            tmp = random.randrange(*(Config.range_.value))
            if tmp != self.prev:
                self.ans = tmp
        return (0,)

    def prompt(self):
        return (
            0,
            'Higher or Lower ({}): '.format(self.prev))

    def input_(self, val):
        if val.lower() in Config.selection.value['Higher']:
            self.sel = 'H'
            return (0,)
        elif val.lower() in Config.selection.value['Lower']:
            self.sel = 'L'
            return (0,)
        else:
            return (
                -1,
                'invalid')

    def judge(self):
        if self.prev < self.ans:
            tmp = 'H'
        else:
            tmp = 'L'

        if tmp == self.sel:
            tmp = 'Hit'
            self.cnt += 1
        else:
            tmp = 'Miss'
            self.cnt = 0
        tmp += '\nCombo: {}'.format(self.cnt)

        return (
            0,
            tmp)


def main():
    game = HigherOrLower()
    while True:
        game.generate()
        while True:
            tmp = game.prompt()
            print(tmp[1], end='')
            tmp = game.input_(input())
            if tmp[0] != 0:
                print(tmp[1])
            else:
                break
        tmp = game.judge()
        print(tmp[1])


if __name__ == '__main__':
    main()
