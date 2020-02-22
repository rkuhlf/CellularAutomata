from itertools import chain


def truncline(text, font, maxwidth):
    full = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    old = None
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        full = len(stext)
        done = 0
    return full, done, stext


def wrap_line(text, font, max_width):
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, max_width)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, max_width):
    lines = chain(*(wrap_line(line, font, max_width) for line in text.splitlines()))
    return list(lines)
