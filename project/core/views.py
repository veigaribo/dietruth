from typing import cast
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from core.models import Roll
from core.forms import RollForm
from core.roll.parse import RollDescriptor
from core.roll.rpc import perform
from core.roll.roll import format_result, make_roll
from core.util import get_session

# Create your views here.


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")


@login_required()
@permission_required("add_roll")
def do_roll(request: HttpRequest) -> HttpResponse:
    form = RollForm(request.POST)

    if form.is_valid():
        descriptor = cast(RollDescriptor, form.cleaned_data["query"])
        result = perform(descriptor)

        roll = make_roll(descriptor, result)
        roll.save()

        return redirect("get_roll", id=roll.id, permanent=True)

    # see ./context_processors.py
    get_session(request)["last_query"] = request.POST["query"]
    current_page = form.cleaned_data["current_page"]
    return redirect(current_page, permanent=True)


def get_roll(request: HttpRequest, id: str) -> HttpResponse:
    roll = get_object_or_404(Roll, pk=id)
    formatted_dice = format_result(roll.result, roll.modifier)

    return render(
        request, "core/get_roll.html", {"roll": roll, "formatted_dice": formatted_dice}
    )
