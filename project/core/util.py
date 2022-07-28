from typing import cast, Any
from django.contrib.sessions.backends.db import SessionStore
from django.db.models.manager import Manager
from django.http import HttpRequest


def get_session(request: HttpRequest):
    # :c
    request2 = cast(Any, request)
    return cast(SessionStore, request2.session)


def orm(model: Any) -> Manager:
    return model.objects
