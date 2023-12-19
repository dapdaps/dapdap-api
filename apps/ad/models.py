from core.base.base_models import BaseDBModel, BaseCreatedUpdatedAtModel, BaseCreatedAtModel
from tortoise import fields


class Ad(BaseDBModel, BaseCreatedUpdatedAtModel):
    category_id = fields.IntField(null=True)
    category = fields.CharField(max_length=50, null=False)
    ad_link = fields.CharField(max_length=200, null=True)
    ad_images = fields.TextField(null=True)

    def __str__(self):
        return self.id

    class Meta:
        table = 'ad'