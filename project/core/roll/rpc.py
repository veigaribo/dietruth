import json
from typing import TypedDict
from django.conf import settings
import requests
from .parse import RollDescriptor, RollResult


class RandomOrgSignedRpcParams(TypedDict):
    apiKey: str
    n: int
    length: int
    min: int
    max: int
    replacement: bool


class RandomOrgSignedRpcPayload(TypedDict):
    jsonrpc: str
    method: str
    params: RandomOrgSignedRpcParams
    id: int


def get_method():
    if settings.RANDOM_ORG_SIGN:
        return "generateSignedIntegerSequences"
    else:
        return "generateIntegerSequences"


def make_payload_params(descriptor: RollDescriptor) -> RandomOrgSignedRpcParams:
    return {
        "apiKey": settings.RANDOM_ORG_KEY,
        "n": 1,
        "length": descriptor.qty,
        "min": 1,
        "max": descriptor.sides,
        "replacement": True,
    }


def make_payload(descriptor: RollDescriptor) -> RandomOrgSignedRpcPayload:
    return {
        "jsonrpc": "2.0",
        "method": get_method(),
        "params": make_payload_params(descriptor),
        "id": 1,  # gonna be using HTTP so doesnt really matter
    }


def perform(descriptor: RollDescriptor) -> RollResult:
    payload = make_payload(descriptor)

    response = requests.post(
        f"{settings.RANDOM_ORG_BASE_URL}/json-rpc/4/invoke", json=payload
    ).json()

    dice = response["result"]["random"]["data"][0]
    modifier = descriptor.modifier

    if settings.RANDOM_ORG_SIGN:
        signature = response["result"]["signature"]
        randomdata = json.dumps(response["result"]["random"])

        return RollResult(dice, modifier, signature, randomdata)
    else:
        return RollResult(dice, modifier, None, None)
