import os
from typing import IO, Optional


def _open_file(filename: str) -> Optional[IO]:
    if not os.path.exists(filename):
        return None

    file = open(filename)

    return file


def wc(filename: str) -> None:
    file = _open_file(filename)
    if file is None:
        return

    n_strings = 0
    n_words = 0
    n_symbols = 0

    line = file.readline()
    while line:
        n_strings += 1 if line != "" else 0
        n_words += line.count(" ") + 1
        n_symbols += len(line)
        line = file.readline()
    file.close()

    print(f"{n_strings} {n_words} {n_symbols} {filename}")


def nl(filename: str) -> None:
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


def head(filename: str, n_lines: int = 10) -> None:
    if n_lines <= 0:
        print("Incorrect number of lines")
        return

    file = _open_file(filename)
    if not file:
        return

    output_string = ""
    for i in range(n_lines):
        line = file.readline()
        if not line:
            break

        output_string += line
    file.close()

    print(output_string, end="")


def tail(filename: str, n_lines: int = 10) -> None:
    if n_lines <= 0:
        print("Incorrect number of lines")
        return

    file = _open_file(filename)
    if not file:
        return

    data = file.read()
    file.close()

    print("\n".join(data.split("\n")[-n_lines:]))
