from django.db import models
from common.models import BaseModel, Asset


TypeChoice = [(x, x) for x in ['BridgeTransfer', 'BridgeStaking']]


class User(BaseModel):
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='用户名'
    )
    photo = models.ImageField(
        upload_to='symbol/%Y/%m/%d/',
        blank=True,
        null=True
    )
    type = models.CharField(
        max_length=100,
        choices=TypeChoice,
        default="BridgeTransfer",
        verbose_name='交易类别'
    )
    address = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='用户地址'
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class PointsRecord(BaseModel):
    address = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='用户地址'
    )

    class Meta:
        verbose_name = 'PointsRecord'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address
