from dataclasses import asdict, dataclass
import json

PLURAL_ARTICLE = "Die"


@dataclass(frozen=True)
class Noun:
    """Class for representing a noun extracted from the text"""

    article: str
    noun: str
    is_plural: bool = False


def parse_articles():
    print("Now parsing")
    nouns: list[Noun] = []

    with open("articles.txt") as seed_file:
        for line in seed_file:
            new_nouns = parse_line(line.strip())
            if not new_nouns:
                continue
            nouns.extend(new_nouns)

    nouns_to_write = [asdict(noun) for noun in nouns]
    with open("nouns.json", "w") as json_file:
        json.dump(nouns_to_write, json_file)

    print(f"Parsed and saved: {len(nouns)} nouns!")


def parse_line(line: str) -> list[Noun] | None:
    if not line:
        return None

    line_parts = line.split("\t")
    parsed_singular_parts = line_parts[1].split(" ")
    parsed_plural_parts = line_parts[2].split(" ")

    singular_noun = Noun(
        article=parsed_singular_parts[0], noun=parsed_singular_parts[1]
    )

    if parsed_plural_parts[0] != PLURAL_ARTICLE:
        return [singular_noun]

    plural_noun = Noun(
        article=parsed_plural_parts[0], noun=parsed_plural_parts[1], is_plural=True
    )

    return [singular_noun, plural_noun]


if __name__ == "__main__":
    parse_articles()
