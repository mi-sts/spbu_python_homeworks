def _read_file(filename):
    try:
        file = open(filename)
    except IOError:
        print("No such file or directory")
        return None
    except:
        print("Unexpected error")
        return None

    data = file.read()
    file.close()
    return data


def wc(filename):
    data = _read_file(filename)
    if not data:
        return

    strings_number = data.count("\n")
    words_number = data.count(" ") + strings_number
    symbols_number = len(data)

    print("{0} {1} {2} {3}".format(strings_number, words_number, symbols_number, filename))


def nl(filename):
    data = _read_file(filename)
    if not data:
        return

    strings = data.split("\n")
    print("{0:4} {1}".format(i, strings[i]) for i in range(len(strings)))


def head(filename, lines_number=10):
    if lines_number <= 0:
        print("Incorrect number of lines")
        return

    data = _read_file(filename)
    if not data:
        return

    print("\n".join(data.split("\n")[:lines_number]))


def tail(filename, lines_number=10):
    if lines_number <= 0:
        print("Incorrect number of lines")
        return

    data = _read_file(filename)
    if not data:
        return

    print("\n".join(data.split("\n")[-lines_number:]))
