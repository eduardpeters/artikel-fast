from parse_articles import parse_line, Noun


class TestLineParsing:
    def test_empty_line(self):
        line_to_parse = ""
        result = parse_line(line_to_parse)
        assert result is None

    def test_complete_line(self):
        line_to_parse = "1. Time	Die Zeit	Die Zeiten"

        expected = [
            Noun(article="Die", noun="Zeit"),
            Noun(article="Die", noun="Zeiten", is_plural=True),
        ]

        result = parse_line(line_to_parse)

        assert result == expected
