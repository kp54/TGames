import enum
import functools
import logging


class GameBase():
    def __init__(self, config=None, debug=False, extra={}):
        self.state = EnumStatus.stopped
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Initialized')

        for k, v in extra.items():
            setattr(self, k, v)


class EnumStatus(enum.Enum):
    ready = enum.auto()
    running = enum.auto()
    stopped = enum.auto()


def state(*status):
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
