from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ModelBase(models.Model):
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_valid = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Company(ModelBase):
    sn = models.CharField(max_length=10, unique=True)
    fullname = models.CharField(max_length=50)
    shortname = models.CharField(max_length=20)
    spnsr = models.CharField(max_length=20)
    spnsr_shrtname = models.CharField(max_length=20, blank=True, null=True)
    tel = models.CharField(max_length=20)
    tel_ext = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    remark = models.CharField(max_length=300, blank=True, null=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='companies',
    )

    def __str__(self):
        return "{}_{}_{}".format(self.sn, self.shortname, self.spnsr)


class Category(models.Model):
    sn = models.CharField(max_length=1, unique=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return "{}_{}".format(self.sn, self.name)


class Item(ModelBase):
    sn = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    cate = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='items',
    )
    specmain = models.CharField(max_length=100)
    specsub = models.CharField(max_length=100, blank=True, null=True)
    remark = models.CharField(max_length=250, blank=True, null=True)
    is_inquiry = models.BooleanField(default=True)
    is_new = models.BooleanField(default=True)
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='items',
    )

    def __str__(self):
        return "{}_{}_{}".format(self.sn, self.cate.name, self.name)
