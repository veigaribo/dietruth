import json
from django.http import HttpRequest
from core.forms import RollForm
from core.util import get_session


def roll_form(request: HttpRequest) -> dict:
    data = {}
    session = get_session(request)

    if "roll_errors" in session:
        data["roll_errors"] = json.loads(session.pop("roll_errors"))
    else:
        data["roll_errors"] = {}

    data["roll_form"] = RollForm()
    return data
