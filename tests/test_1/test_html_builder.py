import pytest
from src.test_1.html_builder import HTML


def test_generate_empty_html():
    html = HTML()
    assert html.generate() == ""


def test_generate_one_line_html():
    html = HTML()
    html.p("One line.")
    assert html.generate() == "<p>One line.</p>\n"


def test_generate_one_containing_tag_html():
    html = HTML()
    with html.body():
        pass

    assert html.generate() == "<body>\n</body>\n"


def test_generate():
    html = HTML()
    with html.body():
        with html.div():
            with html.div():
                html.p("First string.")
                html.p("Second string.")
            with html.div():
                html.p("Third string.")

    assert (
        html.generate()
        == """<body>
  <div>
    <div>
      <p>First string.</p>
      <p>Second string.</p>
    </div>
    <div>
      <p>Third string.</p>
    </div>
  </div>
</body>
"""
    )
