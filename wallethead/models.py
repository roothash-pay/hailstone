from django.db import models
from django.db.models import UniqueConstraint

from common.models import BaseModel


class Storage(models.Model):
    wallet_id = models.CharField("wallet ID", max_length=128)
    wallet_head = models.CharField("wallet wallethead", max_length=256)
    head_public_key = models.TextField("generate public key")
    head_private_key = models.TextField("generate private key")
    head_ipfs_addr = models.CharField("ipfs address", max_length=128)
    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True
    )
    updated_at = models.DateTimeField(
        auto_now=True, db_index=True
    )

    class Meta:
        verbose_name = 'Head Storage'
        verbose_name_plural = verbose_name
        constraints = [
            models.UniqueConstraint(fields=['wallet_id', 'wallet_head'], name='uniq_wallet_head_id')
        ]

    def __str__(self):
        return self.wallet_id

    def to_dict(self):
        return {
            "wallet_id": self.wallet_id,
            "wallet_head": self.wallet_head,
            "head_ipfs_addr": self.head_ipfs_addr,
            "head_public_key": self.head_public_key,
            "head_private_key": self.head_private_key,
        }