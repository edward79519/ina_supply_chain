from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ModelBase(models.Model):
    addtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    is_open = models.BooleanField(default=True)

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


class Inquiry(ModelBase):

    class Status(models.TextChoices):
        ONGOING = '詢價中'
        END = '結案'

    sn = models.CharField(max_length=12)
    startdate = models.DateField()
    enddate = models.DateField()
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='inquirys',
    )
    cate = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='inquirys',
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.PROTECT,
        related_name='inquirys',
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ONGOING,
    )
    remark = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{}_{}_{}".format(self.sn, self.cate.name, self.company.shortname)


class Current(models.Model):
    code = models.CharField(max_length=4)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class ItemQuota(ModelBase):
    itemsn = models.ForeignKey(
        Item,
        on_delete=models.PROTECT,
        related_name='itemquota',
    )
    inquirysn = models.ForeignKey(
        Inquiry,
        on_delete=models.PROTECT,
        related_name='itemquota',
    )
    count = models.IntegerField(default=1)
    price = models.DecimalField(
        max_digits=18,
        decimal_places=4,
        blank=True,
        null=True,
    )
    crnt = models.ForeignKey(
        Current,
        on_delete=models.PROTECT,
        related_name='itemquota',
        blank=True,
        null=True,
    )
    xchgrt = models.DecimalField(
        max_digits=12,
        decimal_places=6,
        blank=True,
        null=True,
    )
    is_new = models.BooleanField(default=False)
    qdate = models.DateField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return "{}_{}".format(self.inquirysn.sn, self.itemsn.name)

    def ntd_price(self):
        if self.price and self.xchgrt:
            return self.price * self.xchgrt
        else:
            return None
