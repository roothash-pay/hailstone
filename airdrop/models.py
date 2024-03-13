from django.db import models
from common.models import BaseModel, Asset


TypeChoice = [(x, x) for x in ['Invite', 'BridgeTransfer', 'BridgeStaking']]


class AirdropUser(BaseModel):
    name = models.CharField(
        default="unknown",
        max_length=100,
        unique=False,
        verbose_name='用户名'
    )
    invite_code = models.CharField(
        default="0000-0000-0000",
        max_length=100,
        unique=True,
        verbose_name='邀请码'
    )
    invite_me_uuid = models.CharField(
        default="0000-0000-0000",
        max_length=100,
        unique=False,
        verbose_name='邀请人'
    )
    photo = models.ImageField(
        upload_to='symbol/%Y/%m/%d/',
        blank=True,
        null=True
    )
    address = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='用户地址'
    )
    email = models.EmailField(
        blank=True,
        null=True
    )
    points = models.PositiveIntegerField(
        default=0,
        verbose_name="积分数量"
    )
    x_twitter = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="x",
    )
    discord = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="discord",
    )
    telegram = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="discord",
    )
    info = models.CharField(
        max_length=100,
        default="",
        blank=True,
        null=True,
        verbose_name="个人介绍",
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
            'photo': str(self.photo),
            'address': self.address,
            'email': self.email,
            'points': self.points,
            'x_twitter': self.x_twitter,
            'discord': self.discord,
            'telegram': self.telegram,
            'info': self.info
        }


class PointsRecord(BaseModel):
    user = models.ForeignKey(
        AirdropUser,
        related_name="airdrop_user",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="收藏的商家",
    )
    address = models.CharField(
        max_length=100,
        unique=False,
        verbose_name='用户地址'
    )
    type = models.CharField(
        max_length=100,
        choices=TypeChoice,
        default="BridgeTransfer",
        verbose_name='交易类别'
    )
    points = models.PositiveIntegerField(
        default=0,
        verbose_name="积分数量"
    )

    class Meta:
        verbose_name = 'PointsRecord'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.address,
            'type': self.type,
            'points': self.points
        }
