from parse_articles import parse_line


class TestLineParsing:
    def test_empty_line(self):
        line_to_parse = ""
        result = parse_line(line_to_parse)
        assert result is None
