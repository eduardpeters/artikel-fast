from dataclasses import dataclass


@dataclass(frozen=True)
class Noun:
    """Class for representing a noun extracted from the text"""

    article: str
    noun: str
    is_plural: bool = False


def parse_articles():
    print("Now parsing")


def parse_line(line: str) -> list[Noun] | None:
    if not line:
        return None

    singular_noun = Noun(article="Die", noun="Zeit")
    plural_noun = Noun(article="Die", noun="Zeiten", is_plural=True)

    return [singular_noun, plural_noun]


if __name__ == "__main__":
    parse_articles()
