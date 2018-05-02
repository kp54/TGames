from .. import util


class Config():
    def __init__(self, width=16, height=8, mines=15, extra={}):
        self.width = util.clamp(width, 0, 15)
        self.height = util.clamp(height, 0, 15)
        self.mines = util.clamp(mines, 0, int(self.width*self.height*0.9))

        for k, v in extra.items():
            setattr(self, k, v)

    def __str__(self):
        return 'width: {}\nheight: {}\nmines: {}\n'.format(self.width, self.height, self.mines)
