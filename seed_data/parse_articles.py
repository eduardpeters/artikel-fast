from dataclasses import dataclass


@dataclass
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
    return [line]


if __name__ == "__main__":
    parse_articles()
