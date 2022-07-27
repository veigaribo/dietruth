import re
from typing import Optional


class RollDescriptor:
    __slots__ = ["qty", "sides", "modifier", "query"]

    def __init__(self, qty: int, sides: int, modifier: int):
        self.qty = qty
        self.sides = sides
        self.modifier = modifier

    def get_query(self):
        modifier = str(self.modifier) if self.modifier < 0 else f"+{self.modifier}"
        return f"{self.qty}d{self.sides}{modifier}"

    def __str__(self):
        return self.get_query()


class RollResult:
    __slots__ = ["dice", "modifier", "signature", "randomdata"]

    def __init__(
        self,
        dice: list[int],
        modifier: int,
        signature: Optional[str],
        randomdata: Optional[str],
    ):
        self.dice = dice
        self.modifier = modifier
        self.signature = signature
        self.randomdata = randomdata


class RollParseError(ValueError):
    pass


pattern = re.compile(r"^([1-9][0-9]*)?d([1-9][0-9]*)([+-][0-9]+)?$")


def parse(query: str) -> RollDescriptor:
    match = pattern.fullmatch(query.replace(" ", ""))

    if match is None:
        raise RollParseError(f"Invalid query {query}")

    sqty, ssides, smodifier = match.groups()

    try:
        qty = int(sqty or "1")
    except ValueError:
        raise RollParseError(f"Invalid quantity {sqty}")

    try:
        sides = int(ssides)
    except ValueError:
        raise RollParseError(f"Invalid sides {ssides}")

    try:
        modifier = int(smodifier or "+0")
    except ValueError:
        raise RollParseError(f"Invalid modifier {smodifier}")

    return RollDescriptor(qty, sides, modifier)
