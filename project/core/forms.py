from typing import cast
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from core.roll.parse import parse, RollParseError, RollDescriptor


MAX_DICE_QTY = cast(int, settings.MAX_DICE_QTY)
MAX_DICE_SIDES = cast(int, settings.MAX_DICE_SIDES)


class InvalidQuery:
    def __init__(self, query: str):
        self.query = query


class RollQueryField(forms.CharField):
    def to_python(self, value: str):
        if value is None:
            return None

        try:
            return parse(value)
        except RollParseError:
            return InvalidQuery(value)

    def validate(self, value: RollDescriptor | None):
        super().validate(value)

        if value is None:
            raise ValidationError(
                "Empty query.",
                code="invalid",
            )

        if isinstance(value, InvalidQuery):
            raise ValidationError(
                "Invalid query: %(value)s",
                code="invalid",
                params={"value": value.query},
            )

        if value.qty > MAX_DICE_QTY:
            raise ValidationError(
                "Too many dice: %(value)d. Maximum allowed is %(max)d",
                code="invalid",
                params={"value": value.qty, "max": settings.MAX_DICE_QTY},
            )

        if value.sides > MAX_DICE_SIDES:
            raise ValidationError(
                "Die too big: %(value)d. Maximum allowed is %(max)d",
                code="invalid",
                params={"value": value.sides, "max": settings.MAX_DICE_SIDES},
            )

    def run_validators(self, value):
        super().run_validators(str(value))


class CurrentPageField(forms.URLField):
    widget = forms.HiddenInput()


class RollForm(forms.Form):
    query = RollQueryField(label="Query", max_length=60)
    description = forms.CharField(max_length=280, required=False)
