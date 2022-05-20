class HTMLElement:
    def __init__(self, html_owner, tag_name):
        self.html_owner = html_owner
        self.tag_name = tag_name


class HTMLContainingElement(HTMLElement):
    def __enter__(self):
        self.html_owner.start_containing_tag(self.tag_name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.html_owner.end_containing_tag(self.tag_name)


class HTMLLineElement(HTMLElement):
    def __init__(self, html_owner, tag_name, text):
        super().__init__(html_owner, tag_name)
        html_owner.start_line_tag(tag_name)
        html_owner.add_text(text)
        html_owner.end_line_tag(tag_name)


class HTML:
    def __init__(self):
        self.page = ""
        self.nesting_level = 0

    def _get_indent_string(self) -> str:
        return '  ' * self.nesting_level

    def start_containing_tag(self, tag_name):
        self.add_text(self._get_indent_string() + f"<{tag_name}>\n")
        self.nesting_level += 1

    def end_containing_tag(self, tag_name):
        self.nesting_level -= 1
        self.add_text(self._get_indent_string() + f"</{tag_name}>\n")

    def start_line_tag(self, tag_name):
        self.add_text(self._get_indent_string() + f"<{tag_name}>")

    def end_line_tag(self, tag_name):
        self.add_text(f"</{tag_name}>\n")

    def add_text(self, text):
        self.page += text

    def body(self) -> HTMLContainingElement:
        return HTMLContainingElement(self, "body")

    def div(self) -> HTMLContainingElement:
        return HTMLContainingElement(self, "div")

    def p(self, text) -> HTMLLineElement:
        return HTMLLineElement(self, "p", text)

    def generate(self) -> str:
        return self.page
