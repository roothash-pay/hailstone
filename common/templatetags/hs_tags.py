# encoding=utf-8

from decimal import Decimal

import pytz
from django import template
from django.conf import settings
from common.helpers import d0, dec


register = template.Library()


@register.filter(name="hdatetime")
def repr_datetime(value) -> str:
    if not value:
        return ""
    tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")


@register.filter(name="cn_hdatetime")
def cn_hdatetime(value) -> str:
    if not value:
        return ""
    tz = pytz.timezone(settings.TIME_ZONE)
    return value.astimezone(tz).strftime("%m月%d日 %H:%M")


@register.filter(name="keep_two_decimal_places")
def ktd_places(value):
    if value in ["", None, "None", 0, d0]:
        return "0"
    dec_value = Decimal(value).quantize(Decimal("0.0000"))
    return (
        dec_value.to_integral()
        if dec_value == dec_value.to_integral()
        else dec_value.normalize()
    )


