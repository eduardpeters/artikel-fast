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

    def test_no_plurals_dash_line(self):
        line_to_parse = "33. Water	Das Wasser	-"

        expected = [
            Noun(article="Das", noun="Wasser"),
        ]

        result = parse_line(line_to_parse)

        assert result == expected

    def test_no_plurals_line(self):
        line_to_parse = "1993. Frost	Der Frost	(no plural form)"

        expected = [
            Noun(article="Der", noun="Frost"),
        ]

        result = parse_line(line_to_parse)

        assert result == expected

    def test_no_plural_unaccountable_line(self):
        line_to_parse = "2000. Cooking	Das Kochen	(usually uncountable)"

        expected = [
            Noun(article="Das", noun="Kochen"),
        ]

        result = parse_line(line_to_parse)

        assert result == expected
