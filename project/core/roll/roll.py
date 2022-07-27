from core.roll.parse import RollDescriptor, RollResult
from core.models import Roll


def make_roll(descriptor: RollDescriptor, result: RollResult):
    query = descriptor.get_query()
    result_str = ";".join([str(die) for die in result.dice])

    return Roll(
        query=query,
        result=result_str,
        modifier=result.modifier,
        signature=result.signature,
        randomdata=result.randomdata,
    )


def format_result(result: str, modifier: int) -> list[str]:
    if modifier > 0:
        suffix = lambda n: f"{n}+{modifier} = {n + modifier}"
    elif modifier < 0:
        suffix = lambda n: f"{n}{modifier} = {n + modifier}"
    else:
        suffix = lambda n: str(n)

    items = result.split(";")
    return [suffix(int(item)) for item in items]
