from django.http import HttpRequest
from core.forms import RollForm
from core.util import get_session


def roll_form(request: HttpRequest) -> dict:
    session = get_session(request)
    data = {}

    try:
        data["query"] = session.pop("last_query")
    except KeyError:
        pass

    data["current_page"] = request.build_absolute_uri()
    form = RollForm(data)

    return {"roll_form": form}
