import pytest
import time
from src.hw1.bash_imitating_functions import *


@pytest.fixture
def temp_file(tmp_path):
    filename = f"{time.time()}.txt"
    temp_dir = tmp_path / "test_bush_imitating_functions"
    temp_dir.mkdir()
    temp_file = temp_dir / filename
    return temp_file


@pytest.mark.parametrize(
    "data, output",
    [
        (
            "qwerty uiop 123\nasd fgh hjk\n456 7 zxc 89",
            "3 10 40",
        ),
        ("", "0 0 0"),
        ("zxc vbn", "1 2 7"),
    ],
)
def test_wc(data, output, temp_file, capfd):
    temp_file.write_text(data)
    wc(temp_file.absolute())
    out, err = capfd.readouterr()
    assert out == "{0} {1}\n".format(output, temp_file.absolute())


@pytest.mark.parametrize(
    "data, output",
    [
        (
            "qwerty uiop 123\nasd fgh hjk\n456 7 zxc 89",
            "   1 qwerty uiop 123\n   2 asd fgh hjk\n   3 456 7 zxc 89\n",
        ),
        ("zxc vbn", "   1 zxc vbn\n"),
    ],
)
def test_nl(data, output, temp_file, capfd):
    temp_file.write_text(data)
    nl(temp_file.absolute())
    out, err = capfd.readouterr()
    assert out == output


@pytest.mark.parametrize(
    "data, output",
    [
        (
            "\n\n\n",
            "   1 \n   2 \n   3 \n\n",
        ),
        ("qwe\n\nrty", "   1 qwe\n   2 \n   3 rty\n"),
    ],
)
def test_nl_empty_lines(data, output, temp_file, capfd):
    temp_file.write_text(data)
    nl(temp_file.absolute())
    out, err = capfd.readouterr()
    assert out == output


@pytest.mark.parametrize(
    "data, lines_number, output",
    [
        ("qw\ner\nty\nui\nop\nas\ndf\ngh\njk\nlz\nxc\ncv\nbn\nm1\n23\n45\n67", 5, "qw\ner\nty\nui\nop\n"),
        (
            "qw\ner\nty\nui\nop\nas\ndf\ngh\njk\nlz\nxc\ncv\nbn\nm1\n23\n45\n67",
            10,
            "qw\ner\nty\nui\nop\nas\ndf\ngh\njk\nlz\n",
        ),
    ],
)
def test_head(data, lines_number, output, temp_file, capfd):
    temp_file.write_text(data)
    head(temp_file.absolute(), lines_number)
    out, err = capfd.readouterr()
    assert out == output


@pytest.mark.parametrize(
    "data, lines_number, output",
    [
        ("qw\ner\nty\nui\nop\nas\ndf\ngh\njk\nlz\nxc\ncv\nbn\nm1\n23\n45\n67", 5, "bn\nm1\n23\n45\n67\n"),
        (
            "qw\ner\nty\nui\nop\nas\ndf\ngh\njk\nlz\nxc\ncv\nbn\nm1\n23\n45\n67",
            10,
            "gh\njk\nlz\nxc\ncv\nbn\nm1\n23\n45\n67\n",
        ),
        (
            "qw\ner\nty\nui\nop\nas\ndf\ngh\njk\nlz\nxc\ncv\nbn\nm1\n23\n45\n67\n",
            10,
            "jk\nlz\nxc\ncv\nbn\nm1\n23\n45\n67\n\n",
        ),
    ],
)
def test_tail(data, lines_number, output, temp_file, capfd):
    temp_file.write_text(data)
    tail(temp_file.absolute(), lines_number)
    out, err = capfd.readouterr()
    assert out == output
