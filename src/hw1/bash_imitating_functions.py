import os


def _open_file(filename):
    if not os.path.exists(filename):
        return None

    file = open(filename)

    return file


def wc(filename):
    file = _open_file(filename)
    if file is None:
        return

    strings_number = 0
    words_number = 0
    symbols_number = 0

    line = file.readline()
    while line:
        strings_number += 1 if line != "" else 0
        words_number += line.count(" ") + 1
        symbols_number += len(line)
        line = file.readline()
    file.close()

    print(f"{strings_number} {words_number} {symbols_number} {filename}")


def nl(filename):
    file = _open_file(filename)
    if not file:
        return

    output_string = ""
    for i in range(10):
        line = file.readline()
        if not line:
            break

        output_string += "{0:4} {1}".format(i + 1, line)
    file.close()

    print(output_string)

def head(filename, lines_number=10):
    if lines_number <= 0:
        print("Incorrect number of lines")
        return

    file = _open_file(filename)
    if not file:
        return

    output_string = ""
    for i in range(lines_number):
        line = file.readline()
        if not line:
            break

        output_string += line
    file.close()

    print(output_string, end="")


def tail(filename, lines_number=10):
    if lines_number <= 0:
        print("Incorrect number of lines")
        return

    file = _open_file(filename)
    if not file:
        return

    data = file.read()
    file.close()

    print("\n".join(data.split("\n")[-lines_number:]))
