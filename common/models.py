# encoding=utf-8

import uuid
from django.db import models


BoolYesOrNoSelect = [
    (x, x) for x in ["yes", "no"]
]

class BaseModel(models.Model):
    uuid = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True
    )

    class Meta:
        abstract = True

    @property
    def UUID(self):
        return uuid.UUID(hex=self.uuid)

    def generate_uuid(self):
        self.uuid = uuid.uuid4().hex

    def save(self, *args, **kw):
        if not self.uuid:
            self.generate_uuid()
        return super(BaseModel, self).save(
            *args, **kw
        )


class DecField(models.DecimalField):
    def __init__(self, **kw):
        kw.setdefault("max_digits", 65)
        kw.setdefault("decimal_places", 30)
        super(DecField, self).__init__(**kw)


class IdField(models.CharField):
    def __init__(self, **kwargs):
        kwargs.setdefault("max_length", 100)
        super(IdField, self).__init__(**kwargs)


class ApiAuth(BaseModel):
    STATUS_CHOICES = [(x, x) for x in ['UnVerify', 'Verifing', 'Verified']]
    name = models.CharField(
        max_length=64,
        default='',
        verbose_name="接入名称"
    )
    api_token = models.CharField(
        max_length=128,
        default='unknown',
        verbose_name="接入 api Token"
    )
    is_expire = models.CharField(
        max_length=128,
        default="no",
        choices=BoolYesOrNoSelect,
        verbose_name="Token是否过期"
    )
    status = models.CharField(
        max_length=32,
        choices=STATUS_CHOICES,
        default='checking',
        verbose_name="API 审核状态"
    )

    class Meta:
        verbose_name = "API 授权表"
        verbose_name_plural = "API 授权表"

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "name": self.name,
            "api_token": self.api_token,
            "is_expire": self.is_expire,
            "status":self.status,
        }