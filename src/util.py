def clamp(value, min_, max_):
    return sorted((min_, value, max_))[1]


def yn(prompt='', *, pattern=(('yes', 'y'), ('no', 'n'))):
    tmp = None
    try:
        while tmp not in pattern[0] + pattern[1]:
            tmp = input(prompt).lower()

    except (KeyboardInterrupt, EOFError):  # on cancelled
        return None

    return tmp in pattern[0]
